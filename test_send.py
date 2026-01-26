# Simple script that sends messages via Evolution API
import requests

API_KEY = "B4sR983jKp2mN7xQ"
BASE_URL = "http://localhost:8080"
INSTANCE = "fire"

def send_message(number, text):
    url = f"{BASE_URL}/message/sendText/{INSTANCE}"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    data = {"number": number, "text": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Demo commands
send_message("2348166351104", "Order confirmation: #12345")
send_message("2348166351104", "Your package is on the way!")