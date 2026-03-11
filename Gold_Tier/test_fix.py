from watchers.execution_watcher import ExecutionWatcher
import os

def test_instantiation():
    try:
        vault_path = os.path.join(os.getcwd(), "AI_Employee_Vault")
        watcher = ExecutionWatcher(vault_path)
        print("[✓] ExecutionWatcher instantiated successfully.")
        
        # Test if check_for_updates exists
        updates = watcher.check_for_updates()
        print(f"[✓] check_for_updates found {len(updates)} items.")
        return True
    except TypeError as e:
        print(f"[!] Instantiation failed: {e}")
        return False

if __name__ == "__main__":
    test_instantiation()
