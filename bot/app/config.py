import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (two levels up from this file)
# This works whether .env is in bot/ or project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("AUTHENTICATION_API_KEY")
BASE_URL = os.getenv("SERVER_URL", "http://localhost:8080")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "fire")
