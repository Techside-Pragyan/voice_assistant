import pyttsx3
from config.settings import VOICE_RATE, VOICE_VOLUME

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._setup_voice()

    def _setup_voice(self):
        voices = self.engine.getProperty('voices')
        # Selecting a female voice if available, otherwise default
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# Singleton instance
tts = TTSManager()
