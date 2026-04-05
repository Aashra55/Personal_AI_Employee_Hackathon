# approval_watcher.py
import os
import shutil
import subprocess
import re
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
        
        success = False
        # Simple parsing logic for the approved action
        if "type: email" in content or "type: email_response" in content:
            success = self._handle_email(content)
        elif "type: linkedin_post" in content:
            success = self._handle_linkedin(content)
        elif "type: facebook_post" in content:
            success = self._handle_social(content, "facebook")
        elif "type: twitter_post" in content:
            success = self._handle_social(content, "twitter")
        elif "type: instagram_post" in content:
            success = self._handle_social(content, "instagram")
        elif "type: odoo_invoice" in content:
            success = self._handle_odoo(content)
        else:
            print(f"[!] Unknown action type in {approved_file.name}")
            success = False
        
        # Move to Executed or Rejected
        if success:
            dest = self.executed_path / approved_file.name
            shutil.move(str(approved_file), str(dest))
            print(f"[✓] Action successful. Moved to Executed: {approved_file.name}")
            return dest
        else:
            rejected_path = self.vault_path / "Approval" / "Rejected"
            rejected_path.mkdir(parents=True, exist_ok=True)
            dest = rejected_path / approved_file.name
            shutil.move(str(approved_file), str(dest))
            print(f"[!] Action failed. Moved to Rejected: {approved_file.name}")
            return dest

    def _extract_body(self, content, start_marker="## Content"):
        # Helper to find body text - handle both "## Content" and "## Content / Body" and "body:"
        markers = [start_marker, "## Content / Body", "body:"]
        body_pos = -1
        
        for m in markers:
            body_pos = content.find(m)
            if body_pos != -1:
                break
            
        if body_pos != -1:
            # Check if there is a line break after the marker
            lines = content[body_pos:].split('\n', 1)
            if len(lines) > 1:
                body = lines[1].strip()
                # Handle YAML style pipe
                if body.startswith("|"):
                    body = body[1:].strip()
                # Clean up potential trailing markdown or horizontal rules
                if "---" in body:
                    body = body.split("---")[0].strip()
                return body
        return None

    def _handle_email(self, content):
        to_match = re.search(r"To: (.*)", content)
        subject_match = re.search(r"Subject: (.*)", content)
        body = self._extract_body(content, "## Content")
        
        if to_match and subject_match and body:
            to = to_match.group(1).strip()
            subject = subject_match.group(1).strip()
            print(f"[*] Sending Email to {to}...")
            # Using VENV python explicitly
            result = subprocess.run([".\\.venv\\Scripts\\python.exe", "mcp_server/send_email_server.py", to, subject, body])
            return result.returncode == 0
        else:
            print("[!] Failed to parse approved email action.")
            return False

    def _handle_linkedin(self, content):
        body = self._extract_body(content, "## Content")
        if body:
            print(f"[*] Posting to LinkedIn...")
            result = subprocess.run([".\\.venv\\Scripts\\python.exe", "mcp_server/linkedin_post_server.py", body])
            return result.returncode == 0
        else:
            print("[!] Failed to parse LinkedIn content.")
            return False

    def _handle_social(self, content, platform):
        body = self._extract_body(content, "## Content")
        if body:
            print(f"[*] Posting to {platform.capitalize()}...")
            result = subprocess.run([".\\.venv\\Scripts\\python.exe", "mcp_server/social_server.py", platform, body])
            return result.returncode == 0
        else:
            print(f"[!] Failed to parse {platform} content.")
            return False

    def _handle_odoo(self, content):
        client = re.search(r"Client: (.*)", content)
        amount = re.search(r"Amount: (.*)", content)
        desc = re.search(r"Desc: (.*)", content)
        
        if client and amount and desc:
            print(f"[*] Creating Odoo Invoice...")
            result = subprocess.run([
                ".\\.venv\\Scripts\\python.exe", "mcp_server/odoo_server.py", "create_invoice",
                client.group(1).strip(),
                amount.group(1).strip(),
                desc.group(1).strip()
            ])
            return result.returncode == 0
        else:
            print("[!] Failed to parse Odoo invoice details.")
            return False

def check_approved_actions():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = ApprovalWatcher(vault_path)
    return watcher.run_once()

if __name__ == "__main__":
    check_approved_actions()
