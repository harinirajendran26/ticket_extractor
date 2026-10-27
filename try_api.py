import requests

BASE = "http://127.0.0.1:8000"
TICKET = {"text": "Hi, could you tell me the status of order OD123?"}

r = requests.post(f"{BASE}/login", json={"customer_id": "C1", "password": "pass1"})
print("login:", r.status_code)
token = r.json()["token"]

r = requests.post(f"{BASE}/tickets", json=TICKET, headers={"Authorization": f"Bearer {token}"}, timeout=120)
print("real token:", r.status_code, r.text)

r = requests.post(f"{BASE}/tickets", json=TICKET, headers={"Authorization": "Bearer made-up-token"})
print("fake token:", r.status_code, r.text)

r = requests.post(f"{BASE}/tickets", json=TICKET)
print("no token:  ", r.status_code, r.text)