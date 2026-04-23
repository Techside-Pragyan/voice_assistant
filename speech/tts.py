import pyttsx3
import threading
import queue
import time
from config.settings import VOICE_RATE, VOICE_VOLUME

class TTSManager:
    def __init__(self):
        self.queue = queue.Queue()
        self.gui_callback = None
        self.is_speaking = False
        self._stop_event = threading.Event()
        
        # Start the TTS worker thread
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    def _worker(self):
        # Initialize engine in the worker thread to avoid COM issues on Windows
        self.engine = pyttsx3.init()
        self._setup_voice()
        
        while not self._stop_event.is_set():
            try:
                text = self.queue.get(timeout=0.1)
                if text:
                    self.is_speaking = True
                    if self.gui_callback:
                        self.gui_callback(f"AURA: {text}")
                    
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS Worker Error: {e}")
                time.sleep(1)

    def _setup_voice(self):
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            # Increased rate for faster response
            self.engine.setProperty('rate', 240) # Slightly faster
            self.engine.setProperty('volume', VOICE_VOLUME)
        except Exception as e:
            print(f"Error setting up voice: {e}")

    def speak(self, text):
        if not text: return
        # Add to queue for async processing
        self.queue.put(text)

    def stop(self):
        self._stop_event.set()
        self.queue.put(None) # Wake up worker to stop

# Singleton instance
tts = TTSManager()

