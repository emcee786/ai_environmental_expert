from langchain_community.document_loaders import DirectoryLoader


# DATA_PATH = "rag_ai_expert/txts"

def load_documents(txt_path):
    loader = DirectoryLoader(txt_path, glob="*.txt")
    documents = loader.load()
    return documents

