import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request


from rag import run_rag
from manage_datastore import generate_datastore
from slack_functions import save_file_to_azure, get_bot_user_id


flask_app = Flask(__name__) 


# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]


# Initialize the Slack app
slack_app = App(token=SLACK_BOT_TOKEN)
handler = SlackRequestHandler(slack_app)

# Load environment variables from .env file
load_dotenv(find_dotenv())


@slack_app.event("file_shared")
def handle_files(body, say, logger):
    logger.info(body)
    event = body.get("event", {})
    file_id = event.get("file_id")
    if file_id:
        say(text="Thanks, I'll save that to Azure now.")
        save_file_to_azure(file_id)

@slack_app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    
    text = text.replace(mention, "").strip()
    
    say("Sure thing, happy to help!")
    response, source = run_rag(text)
    print("SLACKBOT should say: ", response)
        # Create the source link text
    source_link = f"<{source}|Source>"
    
    say(response)
    say(source_link)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Run the Flask app
if __name__ == "__main__":
    get_bot_user_id()
    generate_datastore()
    flask_app.run(port=4040)
    
