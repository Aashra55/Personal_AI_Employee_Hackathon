import sys
import os
import time
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from watchers.gmail_watcher import check_gmail
from watchers.social_watcher import check_social
from watchers.accounting_watcher import check_accounting
from watchers.execution_watcher import run_execution_loop
from watchers.approval_watcher import check_approved_actions
from watchers.audit_watcher import check_audit

def run_all():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SYSTEM] Starting Automation Cycle...\n")

    cycle_internal_count = 0
    while True:
        cycle_internal_count += 1
        work_done = 0
        
        try:
            print(f"[Cycle {cycle_internal_count}] Checking Weekly Audit Status...")
            work_done += check_audit() or 0
        except Exception as e:
            print(f"[ERROR - Audit] {e}")

        try:
            print(f"[Cycle {cycle_internal_count}] Checking Gmail...")
            work_done += check_gmail() or 0
        except Exception as e:
            print(f"[ERROR - Gmail] {e}")

        try:
            print(f"[Cycle {cycle_internal_count}] Checking Accounting Requests (Odoo)...")
            work_done += check_accounting() or 0
        except Exception as e:
            print(f"[ERROR - Accounting] {e}")

        try:
            print(f"[Cycle {cycle_internal_count}] Checking Social Platforms (FB, IG, X, LinkedIn)...")
            work_done += check_social() or 0
        except Exception as e:
            print(f"[ERROR - Social] {e}")

        try:
            print(f"[Cycle {cycle_internal_count}] Running Reasoning & Execution...")
            work_done += run_execution_loop() or 0
        except Exception as e:
            print(f"[ERROR - Execution] {e}")

        try:
            print(f"[Cycle {cycle_internal_count}] Checking for Human-Approved Actions...")
            work_done += check_approved_actions() or 0
        except Exception as e:
            print(f"[ERROR - Approval] {e}")

        if work_done == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No more immediate work. Sleeping.")
            break
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Work processed in this cycle. Continuing internal loop...")
            time.sleep(2) # Short breathe between internal loops

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SYSTEM] Cycle completed.\n")

if __name__ == "__main__":
    try:
        # Run once or in a loop
        if len(sys.argv) > 1 and sys.argv[1] == "--loop":
            print("[SYSTEM] Running in continuous loop mode (interval: 60s). Press Ctrl+C to stop.")
            while True:
                run_all()
                time.sleep(60)
        else:
            run_all()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutdown requested by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[SYSTEM-CRITICAL] Unexpected error: {e}")
        sys.exit(1)
