# gmail_watcher.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from base_watcher import BaseWatcher
from datetime import datetime
from pathlib import Path
import os
import subprocess
import shutil

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=60)

        self.creds = None

        # Create Done folder properly (THIS was missing)
        self.done_folder = Path(self.vault_path) / "done"
        self.done_folder.mkdir(parents=True, exist_ok=True)

        # Load token if exists
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "token.json", SCOPES
            )

        # If no valid creds → run login flow
        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)
        self.processed_ids = set()

    def check_for_updates(self) -> list:
        results = self.service.users().messages().list(
            userId='me', q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        return [m for m in messages if m['id'] not in self.processed_ids]

    def create_action_file(self, message) -> Path:
        msg = self.service.users().messages().get(
            userId='me', id=message['id']
        ).execute()

        headers = {
            h['name']: h['value']
            for h in msg['payload']['headers']
        }

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

        print(f"[+] Email saved: {subject}")

        # Process with CCR and move to Done
        ai_output = self.trigger_ccr_skill(subject, snippet, from_)

        if ai_output:
            self.finalize_email(filepath, ai_output)

        return filepath

    def trigger_ccr_skill(self, subject, body, sender):
        prompt = f"""
You are an AI Employee operating inside an Obsidian vault.

Your task:
- Analyze the email
- Decide the proper action
- Draft a reply if needed
- Respond strictly in structured Markdown

From: {sender}
Subject: {subject}
Body: {body}

Provide:
## Decision
## Action
## Draft Reply (if required)
"""

        try:
            result = subprocess.run(
                ["ccr.cmd", "code"],
                shell=True,
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )

            print("[✓] CCR processed successfully")
            return result.stdout

        except subprocess.CalledProcessError as e:
            print(f"[!] CCR Error: {e}")
            return None

    def finalize_email(self, filepath: Path, ai_output: str):
        # Append AI output
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("\n\n---\n\n")
            f.write("## AI Processing Result\n\n")
            f.write(ai_output)

        # Move to Done folder
        done_path = self.done_folder / filepath.name
        shutil.move(str(filepath), done_path)

        print(f"[✓] Email processed and moved to Done: {filepath.name}")