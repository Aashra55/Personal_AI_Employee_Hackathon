import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(to, subject, body):
    service = get_gmail_service()
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    try:
        message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        print(f"Message Id: {message['id']}")
        
        # Add logging
        log_path = os.path.join(os.path.dirname(__file__), "email_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            from datetime import datetime
            f.write(f"[{datetime.now()}] SENT: To={to}, Subject={subject}, ID={message['id']}\n")
            
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # This can be used as a CLI tool as well
    import sys
    if len(sys.argv) > 3:
        to = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        send_email(to, subject, body)
    else:
        print("Usage: python send_email_server.py <to> <subject> <body>")
