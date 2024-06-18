import os
import pandas as pd
from split import split_text
from load import load_documents, TXT_PATH, PDF_PATH
from vectorstore import save_to_pinecone, file_exists_in_pinecone
from blobstorage import process_pdfs, delete_local_file
    

def generate_data_store():
    process_pdfs()
    documents = load_documents(TXT_PATH)
    for doc in documents:  
        filepath = doc.metadata['source']
        if file_exists_in_pinecone(filepath) == False:
             chunks = split_text(doc)
             save_to_pinecone(chunks)
        else:
             delete_local_file(filepath)


generate_data_store()