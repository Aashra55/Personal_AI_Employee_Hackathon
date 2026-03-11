import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

def diag_x():
    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter keys are missing in .env")
        return

    print("[*] Testing Twitter (X) Credentials...")
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    
    # Check if we can verify credentials
    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    try:
        r = requests.get(url, auth=auth)
        if r.status_code == 200:
            user_data = r.json()
            print(f"[✓] Successfully authenticated as: @{user_data.get('screen_name')}")
            
            # Now test v2 Post Permission
            print("[*] Testing Post Permission (v2 API)...")
            test_url = "https://api.twitter.com/2/tweets"
            # We won't actually post, just check for 403
            r_post = requests.post(test_url, auth=auth, json={"text": "test"})
            if r_post.status_code == 403:
                print(f"\n[!] ERROR 403: {r_post.text}")
                if "Essential" in r_post.text or "Free" not in r_post.text:
                    print("[*] Note: You might need to upgrade to 'Free' tier (it is $0, but you must select it in the portal).")
                print("\n[*] Common Cause: Your App is likely set to 'Read Only'.")
                print("[*] FIX: Go to Twitter Developer Portal -> Project -> App Settings -> User Authentication Settings.")
                print("[*] Change App Permissions from 'Read' to 'Read and Write'.")
                print("[*] IMPORTANT: After changing permissions, you MUST regenerate your Access Token and Secret!")
            elif r_post.status_code == 402:
                print(f"\n[!] ERROR 402: Payment Required - {r_post.text}")
                print("\n[*] CRITICAL FIX: Your App is NOT enrolled in the Free Tier correctly.")
                print("[*] 1. Go to Developer Portal (https://developer.twitter.com/en/portal/dashboard).")
                print("[*] 2. Check if your App is inside a 'Project'. If it is 'Standalone', you must move it to a Project.")
                print("[*] 3. Ensure the Project is named something like 'Free' or you have selected the 'Free' plan ($0/month).")
                print("[*] 4. If you created the App before subscribing to Free, you might need to create a NEW Project, select 'Free', and create a NEW App inside it.")
            else:
                print(f"Response Status: {r_post.status_code}")
                print(f"Response Body: {r_post.text}")
        else:
            print(f"[!] Authentication Failed: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diag_x()
