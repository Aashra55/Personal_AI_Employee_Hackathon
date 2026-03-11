import os
import datetime
from pathlib import Path
from watchers.base_watcher import BaseWatcher

class AuditWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=3600) # Once per hour
        self.reports_path = self.vault_path / "Archive" / "Reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        # 1. Check if it is Monday (0)
        today = datetime.datetime.now()
        if today.weekday() != 0: # 0 is Monday
             return []
        
        # 2. Check if a report was already generated today
        date_str = today.strftime("%Y%m%d")
        report_file = self.reports_path / f"CEO_BRIEFING_{date_str}.md"
        
        if report_file.exists():
            return []
        
        # If Monday and no report today, we need to generate it
        # Returning a list with a dummy item to trigger create_action_file
        return ["generate_now"]

    def create_action_file(self, dummy) -> Path:
        print("[*] Weekly Audit Triggered (Monday Morning)...")
        import subprocess
        subprocess.run([".\\.venv\\Scripts\\python.exe", "mcp_server/report_generator.py"])
        
        # We don't really create a Needs_Action file here, 
        # as it happens automatically in report_generator.
        # But we must return a Path to satisfy the BaseWatcher interface.
        return self.reports_path / f"CEO_BRIEFING_{datetime.datetime.now().strftime('%Y%m%d')}.md"

def check_audit():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = AuditWatcher(vault_path)
    return watcher.run_once()

if __name__ == "__main__":
    check_audit()
