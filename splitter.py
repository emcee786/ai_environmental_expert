from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                   chunk_overlap=500,
                                                   length_function=len,
                                                   add_start_index=True)
    chunks = text_splitter.split_documents(documents)
    
    ## Debug Code
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    document = chunks[4]
    print(document.page_content)
    print(document.metadata)
    
    return chunks


