# gmail_watcher.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from watchers.base_watcher import BaseWatcher
from datetime import datetime
from pathlib import Path
import os
import shutil

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=60)
        self.creds = None
        self.done_folder = Path(self.vault_path) / "Done"
        self.done_folder.mkdir(parents=True, exist_ok=True)

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        try:
            results = self.service.users().messages().list(userId='me', q='is:unread').execute()
            messages = results.get('messages', [])
            return [m for m in messages if m['id'] not in self.processed_ids]
        except Exception as e:
            print(f"[!] Error checking Gmail: {e}")
            return []

    def create_action_file(self, message) -> Path:
        msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}

        subject = headers.get('Subject', 'No Subject')
        from_ = headers.get('From', 'Unknown Sender')
        snippet = msg.get('snippet', '')

        content = f'''---
type: email
from: {from_}
subject: {subject}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Email Content
{snippet}
'''
        filepath = self.needs_action / f'EMAIL_{message["id"]}.md'
        filepath.write_text(content, encoding="utf-8")
        self.processed_ids.add(message['id'])
        print(f"[+] Email saved to Needs_Action: {subject}")
        return filepath

def check_gmail():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    creds_path = os.path.join(os.getcwd(), "credentials.json")
    if not os.path.exists(creds_path):
        print(f"[!] Warning: credentials.json not found at {creds_path}")
        return
    watcher = GmailWatcher(vault_path, creds_path)
    items = watcher.check_for_updates()
    for item in items:
        watcher.create_action_file(item)

if __name__ == "__main__":
    check_gmail()
