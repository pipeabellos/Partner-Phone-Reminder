import time
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Your Account SID from twilio.com/console
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

# The phone number you want to validate
phone_to_validate = os.environ.get("PHONE_TO_VALIDATE")
# The recipient's phone number
recipients_phone = os.environ.get("RECEPIENTS_PHONE")

twilio_sender_phone = os.environ.get("TWILIO_SENDER_PHONE")

# Read the initial values for the delay and number of correct answers from the .env file
delay = int(os.environ.get("DELAY"))
num_correct = int(os.environ.get("NUM_CORRECT"))

while True:
    # Send the initial SMS message asking for the recipient's partner's phone number
    message = client.messages.create(
        to=recipients_phone,
        from_=twilio_sender_phone,
        body="Please reply with your partner's phone number"
    )

    message_date_created = message.date_created

    # Keep checking for a response every second until one is received
    while True:
        # Get a list of messages received after the initial message was sent
        messages = client.messages.list(
            date_sent_after=message_date_created,
            from_=recipients_phone
        )
        #print(messages)

        # Check if any new messages have been received
        #print(len(messages))
        if len(messages) > 0:
            message = client.messages(messages[0].sid).fetch()
            #print(message.to)
            if message.direction == "inbound":
                # Get the latest message
                latest_message = messages[0]
                # Validate the phone number
                if latest_message.body == phone_to_validate:
                     # Increment the number of times the recipient has entered the correct phone number
                    num_correct += 1

                    # Calculate the delay using a spaced repetition algorithm
                    # This is just an example and you can modify it to suit your needs
                    delay = 2 ** (num_correct - 1)  # The delay increases exponentially

                    # Save the new values of delay and num_correct to the .env file
                    with open(".env", "w") as f:
                        f.write("DELAY={}\n".format(delay))
                        f.write("NUM_CORRECT={}\n".format(num_correct))

                    # Send a successful response message
                    client.messages.create(
                        to=recipients_phone,
                        from_=twilio_sender_phone,
                        body="Great! That's the correct phone number. "
                         "I'll check back in {} days to make sure it's still correct.".format(delay)
                    )
                    # Wait the calculated amount of time before sending the next message
                    time.sleep(delay * 24 * 60 * 60)  # The delay is in days, so convert it to seconds
                    break
                else:
                    # Send a non-successful response message
                    message = client.messages.create(
                        to=recipients_phone,
                        from_=twilio_sender_phone,
                        body="Sorry, that's not the correct phone number. "
                            "Please try again!"
                    )

                    message_date_created = message.date_created

        # Wait one second before checking again
        time.sleep(1)
