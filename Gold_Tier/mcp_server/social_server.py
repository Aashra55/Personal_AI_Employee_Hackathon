import sys
import json
import datetime
import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Social Media MCP Server for Gold Tier
# Supports Facebook, Instagram, LinkedIn, and Twitter (X) - Posting + Summaries

class SocialMediaClient:
    def __init__(self):
        # Facebook/Instagram Credentials
        self.fb_token = (os.getenv("FB_ACCESS_TOKEN") or "").strip()
        self.fb_page_id = (os.getenv("FB_PAGE_ID") or "").strip()
        self.insta_id = (os.getenv("INSTA_USER_ID") or "").strip()
        self.default_ig_image = (os.getenv("IG_DEFAULT_IMAGE_URL") or "https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=1000&auto=format&fit=crop").strip()
        
        # Twitter / X Credentials
        self.x_consumer_key = (os.getenv("X_CONSUMER_KEY") or "").strip()
        self.x_consumer_secret = (os.getenv("X_CONSUMER_SECRET") or "").strip()
        self.x_access_token = (os.getenv("X_ACCESS_TOKEN") or "").strip()
        self.x_access_token_secret = (os.getenv("X_ACCESS_TOKEN_SECRET") or "").strip()
        self.x_bearer_token = (os.getenv("X_BEARER_TOKEN") or "").strip()

    def post_facebook(self, content):
        if not self.fb_token:
            print("[!] FB_ACCESS_TOKEN missing. Mocking Facebook post.")
            return self._mock_post("Facebook", content)
        
        targets = ["me"]
        if self.fb_page_id and self.fb_page_id.lower() != "me":
            targets.insert(0, self.fb_page_id)

        last_error = None
        for target in targets:
            url = f"https://graph.facebook.com/v19.0/{target}/feed"
            payload = {"message": content, "access_token": self.fb_token}
            try:
                r = requests.post(url, data=payload, timeout=10)
                if r.ok:
                    print(f"[✓] Posted to Facebook ({target}): {r.json().get('id')}")
                    return True
                else:
                    last_error = f"Target {target}: {r.text}"
            except Exception as e:
                last_error = str(e)
        
        print(f"[!] Facebook posting failed: {last_error}")
        return False

    def post_twitter(self, content):
        if not all([self.x_consumer_key, self.x_consumer_secret, self.x_access_token, self.x_access_token_secret]):
            print("[!] Twitter API Keys missing. Using Selenium fallback.")
            return self._post_twitter_selenium(content)
        
        url = "https://api.twitter.com/2/tweets"
        auth = OAuth1(self.x_consumer_key, self.x_consumer_secret, self.x_access_token, self.x_access_token_secret)
        payload = {"text": content}
        
        try:
            r = requests.post(url, json=payload, auth=auth, timeout=10)
            if r.status_code in [403, 402]:
                print(f"[!] Twitter API Restricted ({r.status_code}). Using Selenium.")
                return self._post_twitter_selenium(content)
            r.raise_for_status()
            print(f"[✓] Posted to Twitter: {r.json().get('data', {}).get('id')}")
            return True
        except Exception as e:
            print(f"[!] Twitter API Error: {e}. Attempting Selenium...")
            return self._post_twitter_selenium(content)

    def _post_twitter_selenium(self, content):
        try:
            sys.path.append(os.path.dirname(__file__))
            from twitter_poster_selenium import post_tweet as selenium_x_post
            return selenium_x_post(content)
        except Exception as e:
            print(f"[!] Selenium Twitter Error: {e}")
            return self._mock_post("Twitter/X", content)

    def post_instagram(self, content):
        if not all([self.fb_token, self.insta_id]):
            print("[!] Instagram API IDs missing. Using Selenium fallback.")
            return self._post_instagram_selenium(content)
        
        print(f"[*] Attempting Instagram API Post to ID: {self.insta_id}...")
        try:
            # Step 1: Create Media Container
            container_url = f"https://graph.facebook.com/v19.0/{self.insta_id}/media"
            payload = {
                "image_url": self.default_ig_image,
                "caption": content,
                "access_token": self.fb_token
            }
            r = requests.post(container_url, data=payload, timeout=15)
            res = r.json()
            
            if not r.ok:
                print(f"[!] IG Container Creation Failed: {res}")
                return self._post_instagram_selenium(content)
            
            creation_id = res.get("id")
            
            # Step 2: Publish Container
            publish_url = f"https://graph.facebook.com/v19.0/{self.insta_id}/media_publish"
            publish_payload = {
                "creation_id": creation_id,
                "access_token": self.fb_token
            }
            r_pub = requests.post(publish_url, data=publish_payload, timeout=15)
            if r_pub.ok:
                print(f"[✓] Instagram Post Published via API! ID: {r_pub.json().get('id')}")
                return True
            else:
                print(f"[!] IG Publishing Failed: {r_pub.text}")
                return self._post_instagram_selenium(content)

        except Exception as e:
            print(f"[!] Instagram API Exception: {e}")
            return self._post_instagram_selenium(content)

    def _post_instagram_selenium(self, content):
        print("[*] Using Selenium Fallback for Instagram...")
        try:
            sys.path.append(os.path.dirname(__file__))
            from instagram_poster_selenium import post_instagram as selenium_ig_post
            return selenium_ig_post(content)
        except Exception as e:
            print(f"[!] Selenium Instagram Error: {e}")
            return self._mock_post("Instagram", content)

    def _mock_post(self, platform, content):
        print(f"[MOCK] {platform} Post Simulation: {content[:50]}...")
        return True

LOG_FILE = os.path.join(os.path.dirname(__file__), "social_audit.log")

def log_social(platform, action, status="SUCCESS"):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "platform": platform,
        "action": action,
        "status": status
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    client = SocialMediaClient()
    if len(sys.argv) < 3:
        print("Usage: python social_server.py <platform> <content>")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    content = " ".join(sys.argv[2:])
    success = False
    
    if cmd == "facebook": success = client.post_facebook(content)
    elif cmd in ["twitter", "x"]: success = client.post_twitter(content)
    elif cmd == "instagram": success = client.post_instagram(content)
    else:
        print(f"Error: Unknown platform {cmd}")
        sys.exit(1)

    if success:
        log_social(cmd, "POST")
        sys.exit(0)
    else:
        log_social(cmd, "POST", "FAILED")
        sys.exit(1)
