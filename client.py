import hashlib
import requests

SERVER = "http://127.0.0.1:5000"
FILE = "API.md"

with open(FILE, "r") as file:
    bin_file = file.read()

# Hash it
file_hash = hashlib.sha256(bin_file.encode()).hexdigest()

# POST REQUEST

req_json = {
    "filename": FILE,
    "file_hex_hash": file_hash,
    "date_expire": None
}

r = requests.post(SERVER+"/api/files", json=req_json)

print(r.text)