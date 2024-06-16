import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


from splitter import split_text
from loader import load_documents
from vectorstore import save_to_pinecone
from generate import generate_response, generate_source_pdf
from blobstorage import process_pdfs

from dotenv import load_dotenv

load_dotenv()

txt_path = 'txts'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")



def run_rag(user_input):
    response = generate_response(user_input)
    print("rag.py RESPONSE: ", response)
    source = generate_source_pdf(user_input)
    print("rag.py SOURCE: ", source)
    generate_data_store()
    return response, source


def generate_data_store():
    process_pdfs()
    documents = load_documents(txt_path)
    chunks = split_text(documents)
    save_to_pinecone(chunks)


# # TEST/DEBUG CODE
# def main(user_input):
#     run_rag(user_input)

# if __name__ == "__main__":
#     run_rag("what problems do mice cause?")