# run_watcher.py
from gmail_watcher import GmailWatcher

VAULT_PATH = "AI_Employee_Vault"          # Tumhara Obsidian vault
CREDENTIALS_PATH = "E:\\Personal_AI_Employee_Hackathon\\credentials.json"     # Gmail API OAuth token

watcher = GmailWatcher(VAULT_PATH, CREDENTIALS_PATH)
watcher.run()
