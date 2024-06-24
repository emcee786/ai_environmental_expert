
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# from slack_bolt.adapter.flask import SlackRequestHandler
# from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from flask import Flask, request
import requests

from rag import run_rag
from blob_storage import source_container_client


# flask_app = Flask(__name__) 


# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        print("This is your user ID,", response["user_id"])
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")


def save_file_to_azure(file_id):
    slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    response = slack_client.files_info(file=file_id)
    if response['ok']:
        file_info = response['file']
        url_private = file_info['url_private_download']
        
        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
        }
        
        r = requests.get(url_private, headers=headers)
        
        if r.status_code == 200:
            # Upload the file to Azure Blob Storage directly from the response content
            blob_client = source_container_client.get_blob_client(blob=file_info['name'])
            
            # Use the `upload_blob` method correctly with the streamed response content
            blob_client.upload_blob(data=r.raw, overwrite=True)
            print(f'File {file_info["name"]} uploaded to Azure Blob Storage successfully.')
        else:
            print('Failed to upload to Azure Blob storage.')