import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def post_to_linkedin(content):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.getenv("LINKEDIN_AUTHOR_URN")
    
    if not access_token:
        print("Error: LINKEDIN_ACCESS_TOKEN not found in .env file.")
        return False
    if not author_urn:
        print("Error: LINKEDIN_AUTHOR_URN not found in .env file.")
        return False

    # New LinkedIn Posts API (v2/posts) - Standard for Pages
    url = "https://api.linkedin.com/v2/posts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }

    # Payload format for the new Posts API
    payload = {
        "author": author_urn,
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    target = "Page" if "organization" in author_urn else "Profile"
    print(f"[*] Attempting to post to LinkedIn {target} as: {author_urn} using Posts API...")
    
    if "member" in author_urn:
        print("[!] Warning: 'urn:li:member' is usually not supported by Posts API. Use 'urn:li:person' instead.")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        log_path = os.path.join(os.path.dirname(__file__), "linkedin_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- POST ATTEMPT (v2/posts) ---\n")
            f.write(f"Author: {author_urn}\n")
            f.write(f"Content: {content[:50]}...\n")
            
            if response.status_code in [201, 200]:
                print("[✓] Post successful!")
                f.write(f"Status: SUCCESS (201)\n")
                # LinkedIn returns the URN of the new post in the 'x-linkedin-id' header
                post_id = response.headers.get('x-linkedin-id')
                if post_id:
                    print(f"[!] Post ID: {post_id}")
                return True
            else:
                print(f"[!] Post failed: {response.status_code} - {response.text}")
                f.write(f"Status: FAILED ({response.status_code})\n")
                f.write(f"Response: {response.text}\n")
                
                # If Posts API fails, maybe try ugcPosts as a last resort with the same URN
                print("[*] Retrying with legacy ugcPosts API just in case...")
                return retry_with_ugc(access_token, author_urn, content)

    except Exception as e:
        print(f"[!] Request Error: {e}")
        return False

def retry_with_ugc(access_token, author_urn, content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [201, 200]:
        print("[✓] Legacy Post successful!")
        return True
    else:
        print(f"[!] Legacy Post also failed: {response.status_code}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        content = " ".join(sys.argv[1:])
        post_to_linkedin(content)
    else:
        print("Usage: python linkedin_post_server.py <content>")
