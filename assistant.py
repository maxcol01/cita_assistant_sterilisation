# IMPORT OF PACKAGES

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import chromadb
import os
import streamlit as st
from typing import Optional
import pandas as pd
from pathlib import Path
# Project setup

# Check for new documents

def get_latest_doc(num_doc: int, db_path: Path) -> Optional[pd.DataFrame] :
    db = pd.read_csv(db_path, header = 0)
    db = db.sort_values(by="date")
    db_new = db.iloc[:num_doc]
    return db_new


# Read documents function (still limited to PDF for POC)
def read_documents(db: pd.DataFrame) -> None:
    # limit to pdf only for this first iteration
    if db.name.str.contains(".pdf"):
        pass
    pass

# Break documents into chunks function
def break_into_chunks():
    pass


# Embed the chunks function
def embed_chunks():
    pass

# Add to the vector store (using Chroma for POC)
def add_to_vector_store():
    pass

# Store the document in vector db

def add_document_to_vector_db(num_doc: int, db_path: Path) -> None:
    new_doc_db  = get_latest_doc(num_doc, db_path)
    print(len(new_doc_db))
    # 1. Read the documents
    documents_list = read_documents(new_doc_db)
    # 2. Break documents into chunks
    # 3. Vectorize the chunks
    # 4. Add chunks to vector db

# Retriever

# Generator