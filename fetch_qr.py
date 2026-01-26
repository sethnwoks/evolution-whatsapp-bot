import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
BASE_URL = os.getenv("SERVER_URL", "http://localhost:8080")
INSTANCE = "fire"

def get_fresh_qr():
    """Fetches a fresh QR code for an existing instance."""
    url = f"{BASE_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": API_KEY}
    
    print(f"🔄 Fetching fresh QR code for '{INSTANCE}'...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if "base64" in data:
                print("\n✅ New QR Code generated!")
                print("Step 1: Copy the entire `data:image/png;base64...` string below.")
                print("Step 2: Paste it here: https://codebeautify.org/base64-to-image-converter")
                print("Step 3: Scan the resulting image with WhatsApp (Linked Devices).")
                print("\n" + "="*50)
                print(data["base64"])
                print("="*50 + "\n")
            elif data.get("status") == "CONNECTED" or data.get("instance", {}).get("status") == "open":
                print("🎉 Instance is already CONNECTED! No QR code needed.")
            else:
                print("🤔 Unexpected response format:")
                print(json.dumps(data, indent=2))
        
        elif response.status_code == 404:
            print(f"❌ Error: Instance '{INSTANCE}' not found. Did you create it yet?")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def delete_instance():
    """Deletes the instance so you can start over clean."""
    url = f"{BASE_URL}/instance/delete/{INSTANCE}"
    headers = {"apikey": API_KEY}
    
    print(f"🗑️ Deleting instance '{INSTANCE}'...")
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("✅ Instance deleted successfully. You can now run `create_instance.py` again.")
    else:
        print(f"❌ Failed to delete: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        delete_instance()
    else:
        get_fresh_qr()
        print("\n💡 Tip: Run `python3 fetch_qr.py delete` if you want to wipe it and start again.")
