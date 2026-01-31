import requests
import urllib.parse
import os
import time

# Path that we expect the file to be at
file_path = os.path.abspath("organization.yaml")
print(f"Checking for file at: {file_path}")
if not os.path.exists(file_path):
    print("Warning: File does not exist locally!")
else:
    print("File exists locally.")

encoded_path = urllib.parse.quote(file_path)
url = f"http://localhost:5000/?load={encoded_path}"

print(f"Requesting: {url}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if "CEO" in response.text:
        print("SUCCESS: Found 'CEO' in the response. Backend is serving the file correctly.")
    else:
        print("FAILURE: 'CEO' NOT found in the response.")
        if "root:" in response.text:
            print("Found 'root:' - likely serving default YAML.")
        else:
            print("Unknown response content.")
except Exception as e:
    print(f"Request failed: {e}")
