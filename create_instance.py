import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configuration from .env
# Using AUTHENTICATION_API_KEY and SERVER_URL to match your .env file
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
BASE_URL = os.getenv("SERVER_URL", "http://localhost:8080")

def create_instance_with_webhook(instance_name):
    """
    Creates a new Evolution API instance and configures a webhook 
    to point back to our FastAPI bot brain.
    """
    url = f"{BASE_URL}/instance/create"
    
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

    # Configuration matches your pseudocode
    data = {
        "instanceName": instance_name,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS",
        "webhook": {
            "enabled": True,
            "url": "http://host.docker.internal:5000/webhook",
            "byEvents": False,
            "base64": False,
            "events": [
                "MESSAGES_UPSERT",
                "CONNECTION_UPDATE",
                "QRCODE_UPDATED"
            ]
        }
    }

    print(f"🚀 Sending request to create instance: {instance_name}...")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        # Check if requested worked
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ SUCCESS!")
            print(json.dumps(result, indent=2))
            return result
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ ERROR: Could not connect to Evolution API. {e}")
        return None

if __name__ == "__main__":
    # You can change 'fire' to any name you want
    INSTANCE = "fire"
    create_instance_with_webhook(INSTANCE)
    print(f"\n💡 Next steps: If successful, check your Evolution Manager or scan the QR code above.")
