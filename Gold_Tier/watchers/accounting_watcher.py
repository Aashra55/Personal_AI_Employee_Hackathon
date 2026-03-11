# accounting_watcher.py
import os
import shutil
from pathlib import Path
from watchers.base_watcher import BaseWatcher
from datetime import datetime

class AccountingWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=60)
        self.accounting_path = self.vault_path / "Events" / "Accounting"
        self.accounting_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self) -> list:
        return list(self.accounting_path.glob("*.md"))

    def create_action_file(self, req_file: Path) -> Path:
        content = req_file.read_text(encoding="utf-8")
        
        action_content = f'''---
type: odoo_invoice_request
source_file: {req_file.name}
received: {datetime.now().isoformat()}
status: pending
---

## Accounting Request
{content}
'''
        
        filepath = self.needs_action / f'ACCOUNTING_{req_file.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(action_content, encoding="utf-8")
        
        # Move original to Archive
        archive_path = self.vault_path / "Archive" / "Accounting"
        archive_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(req_file), str(archive_path / req_file.name))
        
        print(f"[+] Accounting Request saved to Needs_Action: {req_file.name}")
        return filepath

def check_accounting():
    vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
    watcher = AccountingWatcher(vault_path)
    return watcher.run_once()

if __name__ == "__main__":
    check_accounting()
