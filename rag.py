import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


from splitter import split_text
from loader import load_documents
from vectorstore import save_to_pinecone
from generate import generate_response

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def run_rag(user_input):
    answer = generate_response(user_input)
    # generate_data_store()
    print("This is your answer: ", answer)
    print("Did that answer your question?")
    return answer


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_pinecone(chunks)


# if __name__ == "__main__":
#     main()