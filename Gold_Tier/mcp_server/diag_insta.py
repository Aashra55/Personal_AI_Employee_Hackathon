import os
import requests
from dotenv import load_dotenv

load_dotenv()

def diag_instagram():
    token = os.getenv("FB_ACCESS_TOKEN")
    page_id = os.getenv("FB_PAGE_ID")
    
    if not token or not page_id:
        print("Error: FB_ACCESS_TOKEN or FB_PAGE_ID not found in .env")
        return

    print(f"[*] Checking Instagram Business Accounts for Page ID: {page_id}")
    url = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token={token}"
    
    try:
        r = requests.get(url)
        data = r.json()
        print(f"Response: {data}")
        
        insta_account = data.get('instagram_business_account')
        if insta_account:
            print(f"\n[✓] Found Instagram Business Account!")
            print(f"ID: {insta_account.get('id')}")
            print("\nAdd this to your .env as:")
            print(f"INSTA_USER_ID={insta_account.get('id')}")
        else:
            print("\n[!] No Instagram Business Account linked to this Facebook Page.")
            print("[*] Ensure your Instagram Professional account is linked to your Facebook Page.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diag_instagram()
