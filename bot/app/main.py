import requests
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import json
from app.config import API_KEY, BASE_URL, INSTANCE_NAME
from app.handlers import route_message

app = FastAPI(title="Evolution Bot Brain")

def post_reply(number: str, text: str):
    url = f"{BASE_URL}/message/sendText/{INSTANCE_NAME}"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    payload = {"number": number, "text": text}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 201:
            print(f"Failed to reply to {number}: {response.text}")
        else:
            print(f"Replied to {number}")
    except Exception as e:
        print(f"Error sending reply: {e}")

@app.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        if data.get("event") == "messages.upsert":
            msg_data = data.get("data", {})
            message_content = msg_data.get("message", {})
            key_info = msg_data.get("key", {})
            
            # Extract text content
            text = ""
            if message_content.get("conversation"):
                text = message_content["conversation"]
            elif message_content.get("extendedTextMessage"):
                text = message_content["extendedTextMessage"].get("text", "")
            
            text = text.lower().strip()
            
            # Extract sender info
            remote_jid = key_info.get("remoteJid", "")
            sender = remote_jid.split('@')[0]
            from_me = key_info.get("fromMe", False)

            # Ignore own messages
            if not from_me and text:
                print(f"Message from {sender}: {text}")
                reply = route_message(text)
                background_tasks.add_task(post_reply, sender, reply)

    except Exception as e:
        print(f"Webhook Error: {e}")
        return {"status": "error", "message": str(e)}

    return {"status": "received"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Evolution Bot Brain",
        "instance": INSTANCE_NAME
    }

@app.get("/")
async def root():
    return {"status": "running"}


