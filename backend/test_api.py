import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "Hello AI"}

response = requests.post(url, json=data)
print(response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
try:
    print(response.json())
except ValueError:
    print("Response not JSON:", response.text)

