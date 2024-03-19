import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_creds():
    creds = None

    if os.path.exists("../token.json"):
        creds = Credentials.from_authorized_user_file("../token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\Mob\\PycharmProjects\\testProject\\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("../token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_service(creds: Credentials):
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_messages(service):
    results = service.users().messages().list(userId="me").execute()
    messages = results.get('messages', [])
    return messages


def get_texts(messages, service, no_messages=1, buffer_size=500):

    no_texts = 0
    texts = []

    for message in messages[:no_messages]:
        msg_id = message['id']
        msg = service.users().messages().get(userId="me", id=msg_id, format='full').execute()

        headers = msg['payload']['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')

        # Check if the email has parts (multipart)
        parts = msg['payload'].get('parts', [])
        body = ""

        if parts:
            # Get plain text parts only
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('UTF-8')
                    break
        else:
            # For emails with no parts (plain text emails)
            body_data = msg['payload']['body']['data']
            body = urlsafe_b64decode(body_data.encode('ASCII')).decode('UTF-8')

        text = body[:buffer_size].replace(chr(8204), ' ').strip()  # remove weird character from the end of string

        texts.append(subject + text)
        no_texts += 1

    return texts, no_texts


def get_all_texts(no_messages: int):

    creds = get_creds()
    service = get_service(creds)
    messages = get_messages(service)
    texts, no_texts = get_texts(messages, service, no_messages)

    return texts, no_texts
