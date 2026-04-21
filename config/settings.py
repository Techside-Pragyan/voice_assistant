import os
from dotenv import load_dotenv

load_dotenv()

# Assistant Settings
ASSISTANT_NAME = "AURA"
WAKE_WORD = "hey aura"

# API Keys (to be set in .env)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Voice Settings
VOICE_RATE = 200
VOICE_VOLUME = 1.0

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "assistant.log")
