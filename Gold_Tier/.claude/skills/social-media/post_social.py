import sys
import json
import datetime

def post_to_social(platform, content):
    print(f"[*] Posting to {platform}...")
    # Simulated API Call
    log_entry = f"[{datetime.datetime.now()}] {platform.upper()}: {content[:50]}...\n"
    
    with open("../../mcp_server/social_audit.log", "a") as f:
        f.write(log_entry)
        
    return {"status": "posted", "platform": platform, "timestamp": str(datetime.datetime.now())}

if __name__ == "__main__":
    if len(sys.argv) > 2:
        platform = sys.argv[1]
        content = sys.argv[2]
        result = post_to_social(platform, content)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing platform or content"}))
