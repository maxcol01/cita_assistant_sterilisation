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
from datetime import datetime
from pathlib import Path
# Project setup

# Check for new documents

def get_latest_doc(num_doc: int, db_path: Path) -> Optional[pd.DataFrame] :
    db = pd.read_csv(db_path, header = 0)
    db = db.sort_values(by="date")
    db_new = db.iloc[:num_doc]
    return db_new

# Store the document in vector db

def add_document_to_vector_db(num_doc: int, db_path: Path):
    print(type(num_doc))
    print(type(db_path))
    #new_doc_db  = get_latest_doc(num_doc, db_path)

# Retriever

# Generator