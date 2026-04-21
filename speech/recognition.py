import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave
import logging

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        self.microphone_missing = False
        
        print("Initializing AURA Voice Engine (using sounddevice)...")
        # Test if sounddevice can see a default input device
        try:
            sd.query_devices(kind='input')
            print("Microphone detected!")
        except Exception as e:
            print(f"Warning: No input device found: {e}")
            self.microphone_missing = True

    def _record_audio(self, duration=5):
        """
        Records audio using sounddevice and returns it as an AudioData object.
        """
        print("Recording...")
        # Record audio
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Convert to WAV format in memory
        byte_io = io.BytesIO()
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2) # 2 bytes for int16
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(recording.tobytes())
        
        byte_io.seek(0)
        
        with sr.AudioFile(byte_io) as source:
            return self.recognizer.record(source)

    def listen(self, fallback_text=None):
        """
        Listens for audio input using sounddevice and returns the recognized text.
        """
        if self.microphone_missing:
            if fallback_text: return fallback_text.lower()
            return ""

        # If a manual text input was provided via GUI, prioritize it
        if fallback_text:
            return fallback_text.lower()

        try:
            # We record a short burst (5 seconds)
            # Future improvement: use a threshold/silence detection
            audio = self._record_audio(duration=4)
            
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Cloud error: {e}")
            return ""
        except Exception as e:
            print(f"Voice error: {e}")
            return ""

# Singleton instance
recognizer = SpeechRecognizer()
