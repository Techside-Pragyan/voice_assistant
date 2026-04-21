import logging
from config.settings import LOG_FILE

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("VoiceAssistant")

def log_command(command, status):
    logger.info(f"Command: {command} | Status: {status}")

def clean_text(text):
    """
    Strips unnecessary words from the command.
    """
    # Potential stop words to remove
    stop_words = ["please", "can you", "could you", "tell me", "hey", "assistant"]
    for word in stop_words:
        text = text.replace(word, "").strip()
    return text
