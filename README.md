```
# 🤖 Evolution WhatsApp Bot

> A real-time AI assistant for WhatsApp, built on FastAPI, Evolution API, and a RAG-powered knowledge base.
## 📖 Overview

Evolution WhatsApp Bot is a real-time conversational AI system that handles multi-turn WhatsApp interactions with persistent memory, semantic knowledge retrieval, and intelligent human escalation. Built for reliability in production environments with full Docker orchestration on Render.

## ✨ Features

- 🧠 **Contextual AI Responses:** Gemini-powered replies with full conversation memory via Redis session persistence
- 📚 **RAG Knowledge Base:** ChromaDB vector store for semantically grounded, document-aware answers
- 🔄 **Smart Escalation:** n8n sidecar automatically routes complex queries to human agents
- ⚡ **Webhook Architecture:** FastAPI webhook handler processes incoming WhatsApp messages with sub-second routing
- 🛡️ **Production Hardened:** Structured logging, error handling, and environment isolation across dev and prod

## 📦 Technologies

| Layer | Stack |
|---|---|
| API Framework | Python, FastAPI |
| WhatsApp Interface | Evolution API |
| AI Engine | Google Gemini API |
| Knowledge Retrieval | ChromaDB, RAG Pipeline |
| Session Persistence | Redis |
| Storage | PostgreSQL |
| Automation | n8n (escalation sidecar) |
| Infrastructure | Docker, Render |

## 🏗️ Architecture

```

WhatsApp User
     │
     ▼
Evolution API (Webhook)
     │
     ▼
FastAPI Brain
     ├── Redis (Session State)
     ├── ChromaDB (RAG Knowledge Base)
     ├── Gemini API (Response Generation)
     └── n8n Sidecar (Escalation Logic)
     │
     ▼
PostgreSQL (Persistent Storage)
```

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
EVOLUTION_API_URL=your-evolution-api-url
EVOLUTION_API_KEY=your-api-key
GEMINI_API_KEY=your-gemini-key
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgres://user:pass@localhost:5432/db
```

## 🚀 Local Setup (Docker)

```bash
git clone https://github.com/sethnwoks/evolution-whatsapp-bot.git
cd evolution-whatsapp-bot
docker-compose up --build
```

## 🗂️ Repository Structure

```
.
├── bot/                  # Core bot logic and message handlers
├── docker-compose.yml    # Local development orchestration
├── render.yaml           # Production deployment config
├── README.md
└── requirements.txt
```

## 📄 License

Distributed under the MIT License.

---

Built by Seth Nwokolo.
```
