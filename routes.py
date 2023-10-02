from flask import Flask
from gmail_api import read_emails, read_threads, send_email, reply_to_email, get_message_text
from responser import generate_resp
from calendar_api import fetch_free_time
from services import get_services
import os
import pickle
import base64
import time
from email.mime.text import MIMEText
import base64
import re

app = Flask(__name__)
# Extract emails from respective files
with open('assistant_email.txt', 'r') as f:
    assistant_email = f.readline().strip()

# Print the extracted emails
print("ASSISTANT EMAIL: {}".format(assistant_email))


def mark_email_as_read(gmail_service, email_id):
    gmail_service.users().messages().modify(
        userId='me',
        id=email_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

def mark_thread_as_read(gmail_service, thread_id):
    gmail_service.users().threads().modify(
        userId='me',
        id=thread_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()


def create_raw_email(to, sender, subject, message_text, bcc=None):
    """Create a raw email with the given details."""

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if bcc:
        message['bcc'] = bcc

    return base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

def extract_email_address(email_string):
    """
    Extract the email address from the email string.
    """
    match = re.search(r'<(.*?)>', email_string)
    return match.group(1) if match else email_string

def get_emails(message, assistant_email):
    """
    Extract the owner's and client's email from the message.
    """
    # Extract the 'From', 'To', 'Cc', and 'Bcc' headers from the message
    from_email_list = [header['value'] for header in message['payload']['headers'] if header['name'].lower() == 'from']
    to_email_list = [header['value'] for header in message['payload']['headers'] if header['name'].lower() == 'to']
    cc_email_list = [header['value'] for header in message['payload']['headers'] if header['name'].lower() == 'cc']
    bcc_email_list = [header['value'] for header in message['payload']['headers'] if header['name'].lower() == 'bcc']

    all_emails = from_email_list + to_email_list + cc_email_list + bcc_email_list

    # Identify owner's email
    owner_emails = [email for email in all_emails if "elysiuminnovations" in email]
    owner_email = owner_emails[0] if owner_emails else None

    if not owner_email:
        return None, None

    # Identify client's email
    client_emails = [email for email in all_emails if email != owner_email and email != assistant_email]
    client_email = client_emails[0] if client_emails else None

    if not owner_email or not client_email:
        raise ValueError("One or more email headers are missing or invalid.")

    return owner_email, client_email



@app.route('/')
def index():
    # Check if the service objects are saved in the current directory
    
    if os.path.exists('gmail_service.pkl'):
        # Load the service objects from disk
        with open('gmail_service.pkl', 'rb') as f:
            gmail_service = pickle.load(f)
    else:
        # Generate the service objects using your existing function
        gmail_service = get_services()

        # Save the service objects to disk
        with open('gmail_service.pkl', 'wb') as f:
            pickle.dump(gmail_service, f)

    while True:
        new_threads = read_threads(gmail_service)
        new_emails = read_emails(gmail_service)
        thread_ = False

        # If there are new threads
        for thread in new_threads:
            # Fetch all messages in the thread
            full_thread = gmail_service.users().threads().get(userId='me', id=thread['id']).execute()
            messages = full_thread.get('messages', [])

            # If the thread has only one message, treat it as a normal email and continue to the next iteration
            if len(messages) == 1:
                continue

            thread_ = True

            # Format the complete messages with order and context
            formatted_messages = []

            for index, message in enumerate(messages):
                # Extract the complete message content
                msg = get_message_text(message)
                formatted_messages.append(f"Message {index + 1}: {msg}")

            # Join the formatted messages with a separator for clarity
            concatenated_messages = '\n\n'.join(formatted_messages)

            # Generate a response using the concatenated messages
            owner_email, client_email = get_emails(messages[0], assistant_email)

            if not owner_email or not client_email:
                print("NOT FROM ORGANIZATION")
                mark_thread_as_read(gmail_service, thread['id'])
                continue

            owner_email = extract_email_address(owner_email)
            client_email = extract_email_address(client_email)
            print("OWNER EMAIL: {}".format(owner_email))
            print("CLIENT EMAIL: {}".format(client_email))
            body_reply, subject_reply = generate_resp(concatenated_messages, client_email, owner_email, fetch_free_time(owner_email))

            # Send the response via email
            send_email(
                gmail_service,
                to_email=client_email,
                subject=subject_reply,
                body=body_reply,
                bcc_email=owner_email
            )
            
            # Mark the thread as read
            mark_thread_as_read(gmail_service, thread['id'])

            print("SENT RESPONSE")

        # Handle new emails (including threads with a single message)
        if thread_:
            continue
        for email in new_emails:
            # Extract the complete message content
            msg = gmail_service.users().messages().get(userId='me', id=email['id']).execute()
            decoded_message = get_message_text(msg)

            # Generate a response using the email message
            owner_email, client_email = get_emails(msg, assistant_email)

            if not owner_email or not client_email:
                print("NOT FROM ORGANIZATION")
                mark_email_as_read(gmail_service, email['id'])
                continue

            owner_email = extract_email_address(owner_email)
            client_email = extract_email_address(client_email)
            print("OWNER EMAIL: {}".format(owner_email))
            print("CLIENT EMAIL: {}".format(client_email))
            body_reply, subject_reply = generate_resp(decoded_message, client_email, owner_email, fetch_free_time(owner_email))

            # Send the response via email
            send_email(
                gmail_service,
                to_email=client_email,
                subject=subject_reply,
                body=body_reply,
                bcc_email=owner_email
            )
            
            # Mark the email as read
            mark_email_as_read(gmail_service, email['id'])

            print("SENT RESPONSE")

    return "Check your server console."

if __name__ == '__main__':
    app.run(debug=True)
