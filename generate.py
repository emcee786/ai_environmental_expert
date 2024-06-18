import os
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from vectorstore import pinecone
from blobstorage import get_sas_url, archive_container_name, txt_container_name


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
    
def generate_source_url(user_input):
    retrieval_result = retriever.invoke(user_input)
    sources = [doc.metadata['source'] for doc in retrieval_result]
    unique_urls = []
     
    for i, source in enumerate(sources):
        # Check if the current source has appeared earlier in the list
        if source in sources[:i]:
            continue  # Skip if it's a duplicate
        
        source_key = source.lstrip('rag_data/txts/')
               
        if source_key.startswith('vid_'):
            source_name = source_key
            source_url = get_sas_url(source_name, txt_container_name)
        else:
            source_name = source_key.rstrip('.txt')+'.pdf'
            source_url = get_sas_url(source_name, archive_container_name)
            print("generate.py SOURCE_URL: ", source_url)
            
        unique_urls.append(source_url)
        print(len(unique_urls))
        
    return source_url
    
    
# def check_exists(string):
#     exists = False
#     retrieval_result = retriever.invoke(string)
#     sources = [doc.metadata['source'] for doc in retrieval_result]
#     for source in sources:
#         if source == string:
#             exists = True
#             print(f"file {string} EXISTS")
#             return exists
#         else:
#             print(f"file {string} does not exist in pinecone")
#             return exists
            
    
# check_exists('rag_data/txts/nz_potatoes.txt')