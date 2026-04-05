# execution_watcher.py
import os
import shutil
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime
from brain_logic.reasoning_skill import ReasoningSkill

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
        self.skill = ReasoningSkill()

    def check_for_updates(self) -> list:
        # Check for .md files in Needs_Action
        return list(self.needs_action.glob("*.md"))

    def create_action_file(self, action_file: Path) -> Path:
        print(f"[*] Activating Reasoning Skill for: {action_file.name}")
        content = action_file.read_text(encoding="utf-8")
        
        # Read Handbook for context
        handbook_path = self.vault_path.parent / "Company_Handbook.md"
        handbook_content = handbook_path.read_text(encoding="utf-8") if handbook_path.exists() else ""

        # Determine task type
        task_type = "email"
        if "SOCIAL_" in action_file.name: task_type = "social"
        if "ACCOUNTING_" in action_file.name: task_type = "accounting"

        try:
            ai_output = self.skill.run_task(content, task_type, handbook_content)
            
            if not ai_output or "API Error" in ai_output or "Quota Exceeded" in ai_output:
                print(f"[!] Reasoning Skill failed or Quota Exceeded. Skipping for now.")
                return None
                
            print("[✓] Skill reasoning completed.")
            
            # Save Plan
            plan_file = self.plans_path / f"PLAN_{action_file.stem}.md"
            plan_file.write_text(ai_output, encoding="utf-8")
            
            # Extract and save Approval Request
            request_part = None
            if "## ACTION_REQUEST" in ai_output:
                request_part = ai_output.split("## ACTION_REQUEST")[1].strip()
            elif "---" in ai_output:
                # Look for the block between --- or until end of file
                parts = ai_output.split("---")
                # Find the first part that looks like a YAML header
                for i in range(1, len(parts)):
                    if "type:" in parts[i]:
                        # Join the rest of the file if there are more parts, or just take this one
                        request_part = "---" + "---".join(parts[i:])
                        break
            
            if request_part:
                # Clean up markdown markers if AI wrapped the whole thing
                request_part = request_part.replace("```markdown", "").replace("```", "").strip()
                # If there was a trailing ``` that we missed
                if request_part.endswith("```"):
                    request_part = request_part[:-3].strip()
                
                pending_file = self.pending_path / f"PENDING_{action_file.stem}.md"
                pending_file.write_text(request_part, encoding="utf-8")
                print(f"[+] Approval Request created: {pending_file.name}")

            # Move original to Reasoned
            dest = self.reasoned_path / action_file.name
            shutil.move(str(action_file), str(dest))
            return dest

        except Exception as e:
            print(f"[!] Reasoning Skill Error: {e}")
            return None

def run_execution_loop():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = ExecutionWatcher(vault_path)
    return watcher.run_once()

if __name__ == "__main__":
    run_execution_loop()
