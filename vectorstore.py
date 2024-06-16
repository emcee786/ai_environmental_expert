import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

embeddings = OpenAIEmbeddings()
index_name = "nzrag"
pinecone = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def save_to_pinecone(chunks):
    PineconeVectorStore.from_documents(
    chunks, embeddings, index_name=index_name
)   
    #debug code
    print("vectorestore.py - SAVED")
