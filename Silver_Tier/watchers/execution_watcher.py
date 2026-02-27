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
        
        # Read Handbook for context
        handbook_path = self.vault_path / "Company_Handbook.md.md"
        handbook_content = handbook_path.read_text(encoding="utf-8") if handbook_path.exists() else ""

        # Determine if it's a LinkedIn post or an Email based on the source file or content
        is_linkedin = "linkedin_post" in content or "LINKEDIN_" in action_file.name

        if is_linkedin:
            task_instruction = """
1. Analyze the LinkedIn Idea.
2. Create a 'PLAN' in markdown.
3. Create an 'ACTION_REQUEST' with the EXACT format:
   ---
   type: linkedin_post
   ## Content / Body
   [Your professional LinkedIn post content]
   ---
"""
        else:
            task_instruction = """
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

        prompt = f"""
You are an AI Employee Reasoning Engine. 
Use the following Company Handbook and Content to generate a professional action.

--- COMPANY HANDBOOK ---
{handbook_content}

--- ITEM TO PROCESS ---
{content}

--- TASK ---
{task_instruction}

Respond STRICTLY with the PLAN and ACTION_REQUEST sections.
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
                print(f"[!] CCR returned error or no output. Using fallback.")
                if is_linkedin:
                    ai_output = f"## PLAN\n1. Post LinkedIn idea.\n\n## ACTION_REQUEST\n---\ntype: linkedin_post\n## Content / Body\n{content}\n---"
                else:
                    # Basic parsing for fallback email
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
...
---
"""
                
            print("[✓] CCR reasoning completed.")
            
            # Save Plan
            plan_file = self.plans_path / f"PLAN_{action_file.stem}.md"
            plan_file.write_text(ai_output, encoding="utf-8")
            
            # Extract and save Approval Request if present
            request_part = None
            if "## ACTION_REQUEST" in ai_output:
                request_part = ai_output.split("## ACTION_REQUEST")[1].strip()
            elif "---" in ai_output and ("type: email" in ai_output or "type: linkedin_post" in ai_output):
                # Look for the last markdown block or anything between ---
                parts = ai_output.split("---")
                # Usually it's --- [content] ---, so parts will have 3+ elements
                for i in range(len(parts)-1):
                    if "type: email" in parts[i+1] or "type: linkedin_post" in parts[i+1]:
                        request_part = "---" + parts[i+1] + "---"
                        break
            
            if request_part:
                # Clean markdown blocks if AI added them
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
