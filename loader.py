from langchain_community.document_loaders import DirectoryLoader

DATA_PATH = "rag_slackbot/data/"

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents

