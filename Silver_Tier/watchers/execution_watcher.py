# execution_watcher.py
import os
import shutil
import subprocess
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime

import requests

class ExecutionWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        # We watch Needs_Action
        super().__init__(vault_path, check_interval=60)
        self.plans_path = self.vault_path / "Plans"
        self.plans_path.mkdir(parents=True, exist_ok=True)
        self.pending_path = self.vault_path / "Approval" / "Pending"
        self.pending_path.mkdir(parents=True, exist_ok=True)
        self.reasoned_path = self.vault_path / "Reasoned"
        self.reasoned_path.mkdir(parents=True, exist_ok=True)
        self.api_url = "http://127.0.0.1:3456/api"

    def check_for_updates(self) -> list:
        # Check for .md files in Needs_Action
        return list(self.needs_action.glob("*.md"))

    def create_action_file(self, action_file: Path) -> Path:
        print(f"[*] Processing item for reasoning: {action_file.name}")
        content = action_file.read_text(encoding="utf-8")
        
        prompt = f"""
You are an AI Employee Reasoning Engine. 
Analyze the following request and create a detailed Plan and an Action Request.

ITEM CONTENT:
{content}

YOUR TASK:
1. Create a Plan (what needs to be done).
2. If it is an email, ALWAYS suggest a Draft Reply even if it's just a test or a simple greeting.
3. If the action requires external impact (sending email, posting to social media), create an 'Approval Request'.
4. Respond in Markdown.

STRUCTURE YOUR RESPONSE STRICTLY AS FOLLOWS:

## PLAN
[Your detailed steps]

## ACTION_REQUEST
---
type: [email/linkedin_post]
To: [recipient email address]
Subject: [subject line]
## Content / Body
[The actual content to be sent or posted]
---
"""

        # Read Handbook for context
        handbook_path = self.vault_path / "Company_Handbook.md.md"
        handbook_content = handbook_path.read_text(encoding="utf-8") if handbook_path.exists() else ""

        prompt = f"""
Use the following Company Handbook and Email Content to generate a professional action.
If it is a business inquiry, treat it as a Lead. If it is a test, acknowledge it professionally.

--- COMPANY HANDBOOK ---
{handbook_content}

--- EMAIL TO PROCESS ---
{content}

--- TASK ---
1. Analyze the email based on Handbook rules.
2. Create a 'PLAN' in markdown.
3. Create an 'ACTION_REQUEST' with the EXACT format:
   ---
   type: email
   To: [Sender Email]
   Subject: Re: [Original Subject]
   ## Content / Body
   [Your professional reply as the Personal AI Employee of Aashra Saleem]
   ---
"""
        try:
            # We use 'ccr.cmd code' and pass the prompt via input (stdin)
            result = subprocess.run(
                ["ccr.cmd", "code"],
                input=prompt,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            ai_output = result.stdout
            
            # If stdout is empty, check if we got a real response or if we need fallback
            if not ai_output or "Error:" in result.stderr:
                print(f"[!] CCR returned error or no output. Using Handbook-aligned fallback.")
                # Basic parsing for fallback
                sender = "Unknown"
                subject = "Re: Your message"
                for line in content.split('\n'):
                    if line.startswith('from:'): sender = line.split('from:')[1].strip()
                    if line.startswith('subject:'): subject = "Re: " + line.split('subject:')[1].strip()
                
                ai_output = f"""
## PLAN
1. (Fallback) Acknowledging new email from {sender}.
2. Review the drafted reply in Approval/Pending.

## ACTION_REQUEST
---
type: email
To: {sender}
Subject: {subject}
## Content / Body
Dear {sender},

Thank you for reaching out. I am the Personal AI Employee for Aashra Saleem.

We have received your email regarding "{subject.replace('Re: ', '')}" and are processing it according to our Company Handbook. We will get back to you shortly with more details.

Best regards,
Aashra Saleem's AI Assistant
---
"""
                
            print("[✓] CCR reasoning completed.")
            
            # Save Plan
            plan_file = self.plans_path / f"PLAN_{action_file.stem}.md"
            plan_file.write_text(ai_output, encoding="utf-8")
            
            # Extract and save Approval Request if present
            if "## ACTION_REQUEST" in ai_output:
                request_part = ai_output.split("## ACTION_REQUEST")[1].strip()
                # Remove the triple backticks if AI added them
                request_part = request_part.replace("```markdown", "").replace("```", "").strip()
                
                pending_file = self.pending_path / f"PENDING_{action_file.stem}.md"
                pending_file.write_text(request_part, encoding="utf-8")
                print(f"[+] Approval Request created: {pending_file.name}")

            # Move original to Reasoned
            dest = self.reasoned_path / action_file.name
            shutil.move(str(action_file), str(dest))
            return dest

        except Exception as e:
            print(f"[!] CCR API Error: {e}")
            return None

def run_execution_loop():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = ExecutionWatcher(vault_path)
    items = watcher.check_for_updates()
    for item in items:
        watcher.create_action_file(item)

if __name__ == "__main__":
    run_execution_loop()
