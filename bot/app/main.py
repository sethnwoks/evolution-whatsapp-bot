import requests
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import json
from app.config import API_KEY, BASE_URL, INSTANCE_NAME
from app.handlers import route_message

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

            # Route message to appropriate handler
            reply = route_message(text)
            background_tasks.add_task(post_reply, sender, reply)
            print(f"🚀 Queued reply to {sender}")

    return {"status": "received"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "service": "Evolution Bot Brain",
        "evolution_api": BASE_URL,
        "instance": INSTANCE_NAME
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Evolution Bot Brain",
        "status": "running",
        "webhook_endpoint": "/webhook",
        "health_endpoint": "/health"
    }

@app.post("/")
async def root_webhook(request: Request):
    """Catch webhooks sent to root"""
    data = await request.json()
    print("\n⚠️ WEBHOOK HIT ROOT PATH:")
    print(json.dumps(data, indent=2))
    return {"status": "received", "note": "webhook should be sent to /webhook"}
