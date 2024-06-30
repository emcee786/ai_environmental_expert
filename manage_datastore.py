from split import split_text
from load import load_documents, TXT_PATH
from vectorstore import save_to_pinecone, file_exists_in_pinecone
from blob_storage import process_pdfs, delete_local_file
from transcribe import transcribe_youtube_video   

# YouTube URL for Wed demo
demo_video = "https://youtu.be/YAMKf0Mkvko?list=PLcJ9Tc_Fo-NYxWlydpIWd_MN1GcJUdwGP"

def generate_datastore():
    #Transcibe video added for Wed demo
    transcribe_youtube_video(demo_video)
    process_pdfs()
    documents = load_documents(TXT_PATH)
    chunks = split_text(documents)
    save_to_pinecone(chunks)







#     for doc in documents:  
#         filepath = doc.metadata['source']
#         if file_exists_in_pinecone(filepath) == False:
#              print("m_d.py: got to if statement")
#              chunks = split_text(doc)
#              save_to_pinecone(chunks)
#              print("m_d.py: got to chunks statement")
#         else:
#              delete_local_file(filepath)


# generate_datastore()