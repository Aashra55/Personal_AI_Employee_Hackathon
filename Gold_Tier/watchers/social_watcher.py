# social_watcher.py
import os
import shutil
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime

class SocialWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=60)
        self.events_path = self.vault_path / "Events"
        self.platforms = ["LinkedIn_Ideas", "Facebook_Ideas", "Instagram_Ideas", "Twitter_Ideas"]
        
        for p in self.platforms:
            (self.events_path / p).mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        # Collect all .md files from all platform-specific folders
        all_ideas = []
        for p in self.platforms:
            folder = self.events_path / p
            all_ideas.extend(list(folder.glob("*.md")))
        return all_ideas

    def create_action_file(self, idea_file: Path) -> Path:
        platform_name = idea_file.parent.name.replace("_Ideas", "").lower()
        content = idea_file.read_text(encoding="utf-8")
        
        action_content = f'''---
type: {platform_name}_post
source_file: {idea_file.name}
received: {datetime.now().isoformat()}
status: pending
---

## Post Idea for {platform_name.capitalize()}
{content}
'''
        
        filepath = self.needs_action / f'SOCIAL_{platform_name.upper()}_{idea_file.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(action_content, encoding="utf-8")
        
        # Move original idea to Archive/Social
        archive_path = self.vault_path / "Archive" / "Social_Ideas" / platform_name
        archive_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(idea_file), str(archive_path / idea_file.name))
        
        print(f"[+] Social Idea ({platform_name}) saved to Needs_Action: {idea_file.name}")
        return filepath

def check_social():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = SocialWatcher(vault_path)
    return watcher.run_once()

if __name__ == "__main__":
    check_social()
