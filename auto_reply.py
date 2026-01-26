import os
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from dotenv import load_dotenv
import uvicorn
import json

# Load variables from .env
load_dotenv()

# Configuration
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
BASE_URL = os.getenv("SERVER_URL", "http://localhost:8080")
INSTANCE_NAME = "fire"

app = FastAPI(title="Evolution Bot Brain")

def post_reply(number: str, text: str):
    """Helper to send the reply in the background so we don't block the API"""
    url = f"{BASE_URL}/message/sendText/{INSTANCE_NAME}"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    payload = {"number": number, "text": text}
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ Replied to {number}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending reply: {e}")

# THIS IS THE MAIN EAR: This endpoint listens for messages sent from Evolution API
@app.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming webhooks from Evolution API"""
    data = await request.json()

    # Debug: print everything we receive
    print("\n🔔 WEBHOOK RECEIVED:")
    print(json.dumps(data, indent=2))
    
    # We check if the event is a new message. .get() prevents crash if 'event' is missing
    if data.get("event") == "messages.upsert":
        # We use {} as a default so if 'data' is missing, the script won't explode
        msg_data = data.get("data", {})
        # Safety default {}: if 'message' is missing, we get an empty dict instead of None
        message_content = msg_data.get("message", {})
        
        # 1. Initialize empty text
        text = ""
        
        # 2. Check for simple text messages
        if message_content.get("conversation"):
            text = message_content["conversation"]
            
        # 3. Check for extended messages (links, replies, or formatted text)
        elif message_content.get("extendedTextMessage"):
            # Default "": if 'text' field is missing, we get an empty string to avoid errors
            text = message_content["extendedTextMessage"].get("text", "")
            
        # 4. Standardize (lowercase and remove extra spaces)
        text = text.lower().strip()
        
        # 5. Extract Metadata (Sender Info)
        # We use {} as default: if 'key' is missing, variables below won't crash the script
        key_info = msg_data.get("key", {})
        
        # remoteJid usually looks like "2348166351104@s.whatsapp.net"
        # Default "": ensures we can always run .split() without a crash
        full_jid = key_info.get("remoteJid", "")
        
        # We split at the '@' and take the first part to get just the phone number
        sender = full_jid.split('@')[0]
        
        # fromMe: True if WE sent the message, False if a USER sent it.
        # CRITICAL: If we don't check this, the bot will reply to itself forever (Infinite Loop!)
        is_from_me = key_info.get("fromMe", False)

        if not is_from_me and text:
            print(f"📩 Message from [{sender}]: {text}")

            # MODERN "FIRE MAN" LOGIC
            if any(word in text for word in ["hi", "hello", "fire"]):
                reply = "🔥 *FASTAPI MODE ACTIVATED!* 🚀\n\nThe brain has been upgraded to a high-performance engine."
                background_tasks.add_task(post_reply, sender, reply)
                print(f"🚀 Queued reply to {sender}")
            
            elif "demo" in text:
                background_tasks.add_task(post_reply, sender, "🤖 Running on FastAPI + Uvicorn.")
                print(f"🤖 Queued demo reply to {sender}")

    return {"status": "received"}

@app.post("/")
async def root_webhook(request: Request):
    """Catch webhooks sent to root"""
    data = await request.json()
    print("\n⚠️ WEBHOOK HIT ROOT PATH:")
    print(json.dumps(data, indent=2))
    return {"status": "received", "note": "webhook should be sent to /webhook"}

if __name__ == "__main__":
    print("🚀 Starting Evolution Bot Brain on http://0.0.0.0:5000")
    print(f"📡 Webhook endpoint: http://localhost:5000/webhook")
    print(f"🔑 API Key: {API_KEY}")
    print(f"🌐 Evolution URL: {BASE_URL}")
    print(f"📱 Instance: {INSTANCE_NAME}\n")
    # Run the server on Port 5000
    uvicorn.run(app, host="0.0.0.0", port=5000)
