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



def generate_response(user_input):
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
    
  
   # Retrieve context and source metadata
    retrieval_result = retriever.invoke(user_input)
    
    # Extract and print only the metadata['source'] part
    # sources = [doc.metadata['source'] for doc in retrieval_result]
    # for source in sources:
    #     print(f"metadata={{'source': '{source}'}}")
        
    # context = " ".join([doc.page_content for doc in retrieval_result])
    # source = " ".join(sources)
    
    # context = retrieval_result
    # print("HERES YOUR  CONTEXT: ", retrieval_result)
    # source = " ".join([doc.metadata["source"] for doc in retrieval_result])
    
    
    # # Create the input for the prompt
    # input_data = {
    #     "context": context,
    #     "question": user_input,
    #     "source": source
    # }
    
    setup = RunnableParallel(context=retriever, question=RunnablePassthrough())
    chain = setup | prompt | model | parser
    
    response = chain.invoke(user_input)

    source=RunnablePassthrough()
    # print(f"Response: {response['answer']}")
    # print(f"Source document: {source}")
    
    return response

# def provide_source():
    
