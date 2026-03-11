import os
import requests
from dotenv import load_dotenv

load_dotenv()

def diag_facebook():
    token = os.getenv("FB_ACCESS_TOKEN")
    if not token:
        print("Error: FB_ACCESS_TOKEN not found in .env")
        return

    print("[*] Checking Token Debugger...")
    # Inspect the token
    url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}"
    try:
        r = requests.get(url)
        data = r.json().get('data', {})
        print(f"--- Token Info ---")
        print(f"Type: {data.get('type')}")
        print(f"App ID: {data.get('app_id')}")
        print(f"Valid: {data.get('is_valid')}")
        print(f"Scopes: {', '.join(data.get('scopes', []))}")
        print(f"Expires: {data.get('data_access_expires_at')}")
        
        if data.get('type') == 'USER':
            print("\n[!] This is a USER token. To post to a Page, you should exchange this for a PAGE token.")
            print("[*] Fetching accounts/pages associated with this token...")
            accounts_url = f"https://graph.facebook.com/me/accounts?access_token={token}"
            acc_r = requests.get(accounts_url)
            print(f"Raw Accounts Response: {acc_r.text}")
            accounts = acc_r.json().get('data', [])
            if not accounts:
                print("[!] No pages found. Ensure the user owns a page and the app has 'pages_read_engagement' and 'pages_show_list'.")
            for acc in accounts:
                print(f"--- Page Found ---")
                print(f"Name: {acc.get('name')}")
                print(f"ID: {acc.get('id')}")
                print(f"Token: {acc.get('access_token')[:15]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diag_facebook()
