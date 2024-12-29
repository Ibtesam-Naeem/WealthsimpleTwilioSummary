from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def send_message(body):
    """
    Sends a message using Twilio.

    Args:
        body (str): The message content to be sent.
    """
    # Load credentials from environment variables
    TWILIO_ACCOUNT = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    TARGET_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

    # Validate that all required environment variables are loaded
    if not all([TWILIO_ACCOUNT, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, TARGET_NUMBER]):
        raise ValueError("One or more required environment variables are missing.")

    client = Client(TWILIO_ACCOUNT, TWILIO_AUTH_TOKEN)

    # Sends the message
    message = client.messages.create(
        body=body,
        from_=TWILIO_NUMBER,
        to=TARGET_NUMBER
    )

    # Confirms that the message was sent
    print(f"Message sent with SID: {message.sid}")
