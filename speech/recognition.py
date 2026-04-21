import speech_recognition as sr
import logging

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone_missing = False
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except (ImportError, Exception) as e:
            print(f"Microphone or PyAudio not found: {e}")
            print("Falling back to text-based input.")
            self.microphone_missing = True

    def listen(self):
        """
        Listens for audio input and returns the recognized text.
        Falls back to text input if microphone is unavailable.
        """
        if self.microphone_missing:
            query = input("\n[System: No Mic] Type your command: ")
            return query.lower()

        with self.microphone as source:
            print("\nListening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Recognizing...")
                query = self.recognizer.recognize_google(audio, language='en-in')
                print(f"User: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return ""

# Singleton instance
recognizer = SpeechRecognizer()
