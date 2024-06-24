from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(document):
    # Ensure the document is wrapped in a list
    if not isinstance(document, list):
        document = [document]
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                   chunk_overlap=500,
                                                   length_function=len,
                                                   add_start_index=True)
    chunks = text_splitter.split_documents(document)
    

    
    return chunks



    # DEBUG Code
    # print("Splitter.py DEBUG code")
    # print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    # document = chunks[4]
    # print(document.page_content)
    # print(document.metadata)
