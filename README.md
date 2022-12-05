# **Phone Validation Script created by chatgpt**

This Python script sends an SMS message to a specific number asking the recipient to write down his/her partner's phone number. The script then checks if the response received is the same as the phone number to be validated.

## **Requirements**

- Python 3.6 or higher
- Twilio account and credentials

## **Installation**

1. Install the required Python packages by running the following command:

```
pip install -r requirements.txt

```

1. Create a file called **`.env`** in the root directory of the project and add the following environment variables:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
RECEPIENTS_PHONE=the_phone_number_of_the_recipient
TWILIO_SENDER_PHONE=your_twilio_sender_phone
PHONE_TO_VALIDATE=the_phone_you_want_to_remember
DELAY=0
NUM_CORRECT=0

```

## **Usage**

To run the script, use the following command:

```
python main.py

```

The script will ask for the phone number to be validated and the recipient's phone number. It will then send an SMS message to the recipient asking for the input of the partner's phone number. The script will keep checking for a response every second until one is received. If the response is the same as the phone number to be validated, the script will send a successful response message. Otherwise, it will send a non-successful response message and keep checking for another response.

## **Customization**

The script uses a simple spaced repetition algorithm to delay the next message. You can customize this algorithm to suit your needs by modifying the **`delay`** and **`num_correct`** variables in the **`main.py`** file.

## **License**

This project is licensed under the MIT License. See the **`LICENSE`** file for details.