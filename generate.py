import os
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from vectorstore import pinecone
from blobstorage import get_sas_url, archive_container_name

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
    return response
    
def generate_source_pdf(user_input):
    retrieval_result = retriever.invoke(user_input)
    sources = [doc.metadata['source'] for doc in retrieval_result]
    
    ## Need to check for double ups in filenames
    for source in sources:
        source_name = source.lstrip('txts/').rstrip('.txt')+ '.pdf'
        source_url = get_sas_url(source_name, archive_container_name)
        print("generate.py SOURCE_URL: ", source_url)
    
    return source_url


# query = "What problems do mice cause?"
# generate_response(query)
# generate_sources(query)        