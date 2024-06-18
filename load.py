from langchain_community.document_loaders import DirectoryLoader
import os

TXT_PATH = "rag_data/txts"
PDF_PATH =  "rag_data/pdfs"

def load_documents(txt_path):
    loader = DirectoryLoader(txt_path, glob="*.txt")
    documents = loader.load()
    return documents


