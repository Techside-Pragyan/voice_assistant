import pyttsx3
from config.settings import VOICE_RATE, VOICE_VOLUME

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._setup_voice()
        self.gui_callback = None
        self.is_speaking = False

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    def _setup_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Increased rate for faster response
        self.engine.setProperty('rate', 225) 
        self.engine.setProperty('volume', VOICE_VOLUME)

    def speak(self, text):
        if not text: return
        self.is_speaking = True
        if self.gui_callback:
            self.gui_callback(f"AURA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

# Singleton instance
tts = TTSManager()
