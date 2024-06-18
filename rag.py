import os

from generate import generate_response, generate_source_url
from manage_datastore import generate_data_store


from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def run_rag(user_input):
    generate_data_store()
    response = generate_response(user_input)
    print("rag.py RESPONSE: ", response)
    source = generate_source_url(user_input)
    print("rag.py SOURCE: ", source)
    
    return response, source





# TEST/DEBUG CODE
def main(user_input):
    run_rag(user_input)

if __name__ == "__main__":
    run_rag("what problems do mice cause?")