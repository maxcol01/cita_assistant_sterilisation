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

# Project setup

# Check for new documents

# Store the document in vector db

def add_document_to_vector_db():
    with open("test.txt", mode="w") as file:
        file.write("test to see if something happens when calling the function !")

# Retriever

# Generator