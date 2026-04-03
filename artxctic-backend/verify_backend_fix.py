import urllib.request
import urllib.error
import json
import time
import sys
import threading
from datetime import datetime, timedelta, timezone

# Install 'python-jose' if not present, but here we assume environment has dependencies.
# If 'jose' is missing, this script will fail. The user's environment seems to have it based on previous successful runs.
try:
    from jose import jwt
except ImportError:
    print("Error: 'python-jose' library is missing. Please install it with 'pip install python-jose'")
    sys.exit(1)

# Configuration
API_BASE = "http://localhost:8000/api/v1"
SECRET_KEY = "your-super-secret-key-change-this-in-production-min-32-chars"
ALGORITHM = "HS256"
USER_ID = "280172431551893504" # From check_users.py output

def create_access_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": USER_ID, "exp": expire, "type": "access"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def make_request(url, method="GET", data=None, cookie=None):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        if cookie:
            req.add_header("Cookie", cookie)
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            response_body = resp.read().decode('utf-8')
            return status, json.loads(response_body)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 0, str(e)

def verify():
    print("Generating access token...")
    token = create_access_token()
    cookie = f"access_token={token}"
    
    print("Submitting generation request...")
    submit_url = f"{API_BASE}/generate/image"
    payload = {
        "prompt": "test verification image presigned",
        "aspect_ratio": "16:9", # Test non-square aspect ratio
        "model": "flux-schnell"
    }
    
    status, body = make_request(submit_url, method="POST", data=payload, cookie=cookie)
    print(f"Submit Status: {status}")
    
    if status not in [200, 201, 202]:
        print(f"Submit Failed: {body}")
        return

    job_id = body.get("job_id")
    print(f"Job ID: {job_id}")
    
    # Polling loop
    print("Polling status...")
    for i in range(30):
        status_url = f"{API_BASE}/generate/status/{job_id}"
        status_code, data = make_request(status_url, cookie=cookie)
        
        if status_code == 200:
            job_status = data.get("status")
            print(f"Poll {i+1}: Status {job_status}")
            
            if job_status == "completed":
                print("Generation SUCCESS!")
                media = data.get('media', {})
                print(f"Media ID: {media.get('id')}")
                print(f"Aspect Ratio: {media.get('aspect_ratio')}")
                print(f"Full Media URL: {media.get('url')}")
                return
            elif job_status == "failed":
                print(f"Generation FAILED: {data.get('error_message')}")
                return
        else:
            print(f"Poll Failed: {status_code} - {data}")
            
        time.sleep(2)
    
    print("Verification Timed Out")

if __name__ == "__main__":
    verify()
