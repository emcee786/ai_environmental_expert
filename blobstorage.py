import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import requests
import fitz  

from dotenv import load_dotenv
load_dotenv()

# Ensure the 'pdfs' directory exists
pdf_path = 'rag_ai_expert/pdfs'
txt_path = 'txts'

#azure blob credentials
account_name = 'rcouncilnz'
account_key = os.environ["AZURE_BLOB_ACC_KEY"]
source_container_name = 'new-pdfs'
txt_container_name ='txt-files'
archive_container_name = 'archive'

#create a client to interact with blob storage
connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#use the client to connect to the container
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
source_container_client = blob_service_client.get_container_client(source_container_name)
text_container_client = blob_service_client.get_container_client(txt_container_name)
archive_container_client = blob_service_client.get_container_client(archive_container_name)

def get_sas_url(blob_name, container_name):
    #generate a shared access signature for files and load them into Python
        sas_i = generate_blob_sas(account_name = account_name,
                                container_name = container_name,
                                blob_name = blob_name,
                                account_key=account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.now() + timedelta(hours=1))
        sas_url = 'https://' + account_name+'.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas_i
        
        return sas_url
    
def download_pdf(blob_name):
    #download pdf files to local directory
    sas_url = get_sas_url(blob_name, source_container_name)
    response = requests.get(sas_url)
    pdf_path = os.path.join('pdfs', blob_name)
    with open(pdf_path, 'wb') as f:
        f.write(response.content)
    return pdf_path


def extract_text_from_pdf(pdf_path, txt_path):
    #extract text from pdf file and save to local directory.
    pdf_document = fitz.open(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            txt_file.write(text)  # Write the text to the file
            txt_file.write("\n" + "-"*80 + "\n")  # Add a separator between pages
    print(f"Text extracted and saved to {txt_path}")


    
def upload_txt_to_blob(txt_path, blob_name):
    # upload newly created txt files to txt storage container in Azure 
    blob_client = text_container_client.get_blob_client(blob_name)
    with open(txt_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Text file {txt_path} uploaded to Azure Blob Storage")

def move_pdf_to_archive(blob_name):
    source_blob = source_container_client.get_blob_client(blob_name)
    archive_blob = archive_container_client.get_blob_client(blob_name)

    # Copy the blob to the archive container
    copy_status = archive_blob.start_copy_from_url(source_blob.url)
    print(f"Copy status for {blob_name}: {copy_status}")

    # Delete the blob from the source container after copying
    source_blob.delete_blob()
    print(f"PDF file {blob_name} moved to Azure Blob Storage container {archive_container_name}")

def process_pdfs():
    for blob in source_container_client.list_blobs():
        blob_name = blob.name
        if blob_name.endswith('.pdf'):
            print(f"Processing {blob_name}...")
            pdf_path = download_pdf(blob_name)
            txt_name = blob_name.replace('.pdf', '.txt')
            text_path = os.path.join(txt_path, txt_name)
            extract_text_from_pdf(pdf_path, text_path)
            # Optionally upload text back to Azure Blob Storage
            upload_txt_to_blob(text_path, txt_name)
             # Move the original PDF to the archive container
            move_pdf_to_archive(blob_name)




# TEST CODE
# process_pdfs()


