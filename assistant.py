# IMPORT OF PACKAGES

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import chromadb
import os
import streamlit as st
from typing import Optional, List
import pandas as pd
from pathlib import Path
import tiktoken
from config import OPEN_AI_API_KEY
from prompt import prompt_template

# Models setup
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "my_db_sterilisation"

# Initialize embeddings
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Initialize Tokenizer for splitter
tokenizer = tiktoken.get_encoding("o200k_harmony")

def length_token(text: str) -> int:
    return len(tokenizer.encode(text))

# Document splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
    length_function=length_token,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Project setup

# Check for new documents

def get_latest_doc(num_doc: int, db_path: Path) -> Optional[pd.DataFrame] :
    db = pd.read_csv(db_path, header = 0)
    db = db.sort_values(by="date", ascending=False)
    db_new = db.iloc[:num_doc]
    return db_new


# Read documents function
def read_documents(db: pd.DataFrame) -> List:
    all_documents = []
    for doc_path in db.location:
        if os.path.exists(doc_path) and doc_path.lower().endswith(".pdf"):
            loader = PyMuPDFLoader(doc_path)
            all_documents.extend(loader.load())
    return all_documents

# Break documents into chunks function
def break_into_chunks(documents: List):
    return splitter.split_documents(documents)

# Store the document in vector db

def add_documents_to_vector_db(db_path: Path, num_doc: int = None) -> None:
    db = pd.read_csv(db_path, header=0)
    if num_doc:
        db = db.sort_values(by="date", ascending=False).iloc[:num_doc]
    
    # 1. Read the documents
    documents = read_documents(db)
    if not documents:
        print("No documents found.")
        return

    # 2. Break documents into chunks
    chunks = break_into_chunks(documents)
    
    # 3. Add to vector store
    # We use the LangChain wrapper for easier integration
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME
    )
    print(f"Added {len(chunks)} chunks to {COLLECTION_NAME}")

def get_rag_chain():
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    prompt = PromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    def format_docs(docs):
        return "\n\n".join(
            f"[Source: {os.path.basename(doc.metadata['source'])}, page {doc.metadata.get('page', '?')}]\n{doc.page_content}"
            for doc in docs
        )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
