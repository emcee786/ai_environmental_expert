import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

embeddings = OpenAIEmbeddings()
index_name = "aiexpnz"
pinecone = PineconeVectorStore(index_name=index_name, embedding=embeddings)

vectorstore = pinecone
retriever = vectorstore.as_retriever()

def save_to_pinecone(chunks):
    PineconeVectorStore.from_documents(
    chunks, embeddings, index_name=index_name
)   


def file_exists_in_pinecone(filepath):
    exists = False
    retrieval_result = retriever.invoke(filepath)
    sources = [doc.metadata['source'] for doc in retrieval_result]
    for source in sources:
        if source == filepath:
            exists = True
            print(f"file {filepath} EXISTS")
            return exists
        else:
            print(f"file {filepath} does not exist in pinecone")
            return exists
            
    
# file_exists_in_pinecone('rag_data/txts/nz_potatoes.txt')