import os
from dotenv import load_dotenv

load_dotenv()

# Assistant Settings
ASSISTANT_NAME = "Assistant"
WAKE_WORD = "hey assistant"

# API Keys (to be set in .env)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Voice Settings
VOICE_RATE = 175
VOICE_VOLUME = 1.0

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "assistant.log")
