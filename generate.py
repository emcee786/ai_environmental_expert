import os
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from vectorstore import pinecone

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
parser = StrOutputParser()
template = """
    Answer the question based on the context below. If you can't 
    answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    
    """
prompt = ChatPromptTemplate.from_template(template)
vectorstore = pinecone
retriever = vectorstore.as_retriever()
setup = RunnableParallel(context=retriever, question=RunnablePassthrough())
chain = setup | prompt | model | parser

def generate_response(user_input):
    response = chain.invoke(user_input)
    retrieval_result = retriever.invoke(user_input)
    sources = [doc.metadata['source'] for doc in retrieval_result]
    source_str = ', '.join(sources)
    
    response_with_source = response + "\nSources: " + source_str
    # print(f"Response: {response['answer']}")
    # print(f"Source document: {source}")
    print(type(response_with_source))
    return response_with_source
