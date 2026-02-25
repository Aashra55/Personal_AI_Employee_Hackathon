# linkedin_watcher.py
import os
import shutil
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime

class LinkedInWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=60)
        self.ideas_path = self.vault_path / "Events" / "LinkedIn_Ideas"
        self.ideas_path.mkdir(parents=True, exist_ok=True)
        self.executed_path = self.vault_path / "Executed"
        self.executed_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        # Check for .md files in LinkedIn_Ideas
        return list(self.ideas_path.glob("*.md"))

    def create_action_file(self, idea_file: Path) -> Path:
        # Instead of a simple creation, this one might trigger directly or move to Needs_Action
        # Based on Silver Tier, we create a Plan first.
        # But let's follow the base watcher pattern: create an action file in Needs_Action.
        
        content = idea_file.read_text(encoding="utf-8")
        
        action_content = f'''---
type: linkedin_post
source_file: {idea_file.name}
received: {datetime.now().isoformat()}
status: pending
---

## Post Idea
{content}
'''
        
        filepath = self.needs_action / f'LINKEDIN_{idea_file.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(action_content, encoding="utf-8")
        
        # Move original idea to Archive/Ideas
        archive_path = self.vault_path / "Archive" / "LinkedIn_Ideas"
        archive_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(idea_file), str(archive_path / idea_file.name))
        
        print(f"[+] LinkedIn Post Idea saved to Needs_Action: {idea_file.name}")
        return filepath

def check_linkedin():
    # Helper for run_system.py
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = LinkedInWatcher(vault_path)
    # Run one cycle manually
    items = watcher.check_for_updates()
    for item in items:
        watcher.create_action_file(item)

if __name__ == "__main__":
    check_linkedin()
