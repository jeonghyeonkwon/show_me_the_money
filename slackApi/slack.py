from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from setting import settings

client = WebClient(token=settings.slack_token)


def sendMessage(message: str):
    try:
        response = client.chat_postMessage(channel="#coin", text=message)
        print("Message sent successfully!")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
