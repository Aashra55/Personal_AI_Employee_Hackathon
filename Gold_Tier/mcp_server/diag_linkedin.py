import os
import requests
from dotenv import load_dotenv

load_dotenv()

def diagnose():
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    headers = {
        'Authorization': f'Bearer {token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    print("--- DIAGNOSING NEW TOKEN ---")
    
    # Method 1: v2/me (Basic Profile)
    print("\n[1] Trying /v2/me...")
    res = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    if res.status_code == 200:
        print(f"SUCCESS! ID: {res.json().get('id')}")
    else:
        print(f"FAILED: {res.status_code} - {res.text}")

    # Method 2: userinfo (OIDC)
    print("\n[2] Trying /v2/userinfo...")
    res = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    if res.status_code == 200:
        sub = res.json().get('sub')
        print(f"SUCCESS! Sub: {sub}")
        print(f"\n[!] YOUR AUTHOR URN SHOULD BE: urn:li:person:{sub}")
    else:
        print(f"FAILED: {res.status_code} - {res.text}")

if __name__ == "__main__":
    diagnose()
