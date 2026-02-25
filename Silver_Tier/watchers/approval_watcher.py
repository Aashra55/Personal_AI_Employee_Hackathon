# approval_watcher.py
import os
import shutil
import subprocess
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime

class ApprovalWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=30)
        self.approved_path = self.vault_path / "Approval" / "Approved"
        self.approved_path.mkdir(parents=True, exist_ok=True)
        self.executed_path = self.vault_path / "Executed"
        self.executed_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        return list(self.approved_path.glob("*.md"))

    def create_action_file(self, approved_file: Path) -> Path:
        print(f"[*] Executing approved action: {approved_file.name}")
        content = approved_file.read_text(encoding="utf-8")
        
        # Simple parsing logic for the approved action
        # We expect the AI to have formatted it properly
        
        if "type: email" in content:
            self._handle_email(content)
        elif "type: linkedin_post" in content:
            self._handle_linkedin(content)
        
        # Move to Executed
        dest = self.executed_path / approved_file.name
        shutil.move(str(approved_file), str(dest))
        return dest

    def _handle_email(self, content):
        import re
        # More robust regex parsing
        to_match = re.search(r"To: (.*)", content)
        subject_match = re.search(r"Subject: (.*)", content)
        body_start_marker = "## Content / Body"
        body_pos = content.find(body_start_marker)
        
        if to_match and subject_match and body_pos != -1:
            to = to_match.group(1).strip()
            subject = subject_match.group(1).strip()
            # Everything after the marker is the body
            body = content[body_pos + len(body_start_marker):].strip()
            
            # Clean up potential markdown formatting from AI
            body = body.replace("---", "").strip()
            
            print(f"[*] Sending Email to {to}...")
            subprocess.run(["python", "mcp_server/send_email_server.py", to, subject, body])
        else:
            print("[!] Failed to parse approved email action. Check formatting.")

    def _handle_linkedin(self, content):
        body_start = content.find("## Content") + 10
        if body_start > 9:
            post_content = content[body_start:].strip()
            print(f"Posting to LinkedIn...")
            subprocess.run(["python", "mcp_server/linkedin_post_server.py", post_content])

def check_approved_actions():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = ApprovalWatcher(vault_path)
    items = watcher.check_for_updates()
    for item in items:
        watcher.create_action_file(item)

if __name__ == "__main__":
    check_approved_actions()
