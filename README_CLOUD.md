# WhatsApp Chatbot System 🚀

This project is a cloud-native **WhatsApp Automation Suite** designed to handle customer interactions 24/7 using AI. It leverages the **Evolution API** for WhatsApp connectivity and offers two "brain" options for logic: a visual workflow engine (**n8n**) and a high-performance code-based backend (**FastAPI**).

---

## 🏗️ Architecture

The system is composed of three microservices deployed via `render.yaml`:

1.  **Evolution API Engine (`evo-engine`):**
    *   **Role:** The "Body." Handles the connection to WhatsApp Web (QR Code scanning) and sends/receives messages.
    *   **Tech:** NodeJS, Docker.
    *   **Port:** `8080`.

2.  **Visual Logic Engine (`n8n-brain`):**
    *   **Role:** The "Visual Brain." Processes messages using a drag-and-drop workflow. Connects to **Google Gemini AI** for intelligent responses.
    *   **Tech:** n8n Workflow Automation.
    *   **Port:** `5678`.

3.  **Code Logic Engine (`evo-bot`):**
    *   **Role:** The "Code Brain." A lightweight, high-speed Python microservice for handling high-volume traffic or custom logic.
    *   **Tech:** Python, FastAPI, Uvicorn.
    *   **Port:** `8000`.

---

## 🚀 Deployment Guide (Render)

This project uses **Infrastructure as Code (IaC)**. The entire stack is defined in `render.yaml`.

### 1. Setup on Render
1.  Create a new **Blueprint** on Render.
2.  Connect this GitHub repository.
3.  Render will automatically detect `render.yaml` and spin up all three services.

### 2. Environment Variables
The following variables are automatically handled by the Blueprint but can be customized in the dashboard:
*   `AUTHENTICATION_API_KEY`: Secure key for API communication.
*   `INSTANCE_NAME`: Default instance name (e.g., `fire`).
*   `N8N_ENCRYPTION_KEY`: Security key for n8n credentials.

---

## 🔌 Connection & Usage

### Step 1: Connect WhatsApp
1.  Open the **Evolution Manager** (URL provided by Render).
2.  Navigate to **Instance > QRCode**.
3.  Scan the QR Code with your WhatsApp mobile app.

### Step 2: Choose Your Brain 🧠

You can switch between the **Visual Brain (n8n)** and the **Code Brain (FastAPI)** by changing the Webhook URL in the Evolution Manager.

#### **Option A: Use n8n (Visual AI)**
*   **Webhook URL:** `https://[YOUR-N8N-URL]/webhook/whatsapp`
*   **Features:**
    *   Visual flow builder.
    *   Google Gemini AI integration.
    *   Message filtering (e.g., ignore own messages).

#### **Option B: Use FastAPI (High Performance)**
*   **Webhook URL:** `https://[YOUR-FASTAPI-URL]/webhook`
*   **Features:**
    *   Ultra-low latency.
    *   Custom Python logic (`bot/app/main.py`).
    *   Scalable for high loads.

---

## 🛠️ Local Development

To run the Python bot key locally for testing:

```bash
cd bot
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📝 Troubleshooting

*   **Bot replying to itself?** Ensure your n8n workflow has a **Filter Node** checking that `fromMe` is `False`.
*   **502 Bad Gateway (n8n)?** restart the service in Render (Free Tier RAM limit).
*   **WhatsApp Disconnected?** Re-scan the QR code in the Evolution Manager.
