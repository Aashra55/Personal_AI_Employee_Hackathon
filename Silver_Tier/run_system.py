import sys
import os
import time
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from watchers.gmail_watcher import check_gmail
from watchers.linkedin_watcher import check_linkedin
from watchers.execution_watcher import run_execution_loop
from watchers.approval_watcher import check_approved_actions

def run_all():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SYSTEM] Starting Automation Cycle...\n")

    try:
        print("[1] Checking Gmail for new messages...")
        check_gmail()
    except Exception as e:
        print(f"[ERROR - Gmail] {e}")

    try:
        print("[2] Checking LinkedIn Ideas folder...")
        check_linkedin()
    except Exception as e:
        print(f"[ERROR - LinkedIn] {e}")

    try:
        print("[3] Running Reasoning & Execution Loop...")
        run_execution_loop()
    except Exception as e:
        print(f"[ERROR - Execution] {e}")

    try:
        print("[4] Checking for Human-Approved Actions...")
        check_approved_actions()
    except Exception as e:
        print(f"[ERROR - Approval] {e}")

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SYSTEM] Cycle completed.\n")

if __name__ == "__main__":
    # Run once or in a loop
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        print("[SYSTEM] Running in continuous loop mode (interval: 60s)")
        while True:
            run_all()
            time.sleep(60)
    else:
        run_all()
