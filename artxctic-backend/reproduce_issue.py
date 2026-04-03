import urllib.request
import urllib.error
import json
import os
import time

API_KEY = "d40de4f8-319c-4e0b-bd16-c55489896b16:74c6809859eb6c5672173cc88fb37cd7"
MODEL = "fal-ai/flux/dev"
BASE_URL = "https://queue.fal.run"

HEADERS = {
    "Authorization": f"Key {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Python-urllib/3.8"
}

def make_request(url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, headers=HEADERS, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            response_body = resp.read().decode('utf-8')
            return status, response_body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def test():
    print("Submitting request...")
    submit_url = f"{BASE_URL}/{MODEL}"
    payload = {
        "prompt": "test image",
        "image_size": {"width": 1024, "height": 1024},
        "num_images": 1
    }
    
    status, body = make_request(submit_url, method="POST", data=payload)
    print(f"Submit Status: {status}")
    if status not in [200, 201]:
        print(f"Submit Error: {body}")
        return

    data = json.loads(body)
    request_id = data.get("request_id")
    print(f"Request ID: {request_id}")
    print(f"Full Submit Response Keys: {list(data.keys())}")
    
    if "status_url" in data:
        print(f"Found status_url in response: {data['status_url']}")
    
    # Test endpoints
    endpoints = [
        f"{BASE_URL}/{MODEL}/requests/{request_id}/status",
        f"{BASE_URL}/{MODEL}/requests/{request_id}",
        f"{BASE_URL}/requests/{request_id}/status",
        f"{BASE_URL}/requests/{request_id}",
    ]

    for url in endpoints:
        print(f"\nTesting GET {url}")
        status, body = make_request(url)
        print(f"Status: {status}")
        if status == 200:
            print("Success!")
        else:
            print(f"Error Body: {body}")

if __name__ == "__main__":
    test()
