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

    def _record_audio(self, max_duration=10, silence_threshold=800, silence_limit=0.8, wait_for_speech=3.0):
        """
        Records audio and stops automatically when silence is detected (Highly Optimized).
        Returns None if no speech is detected within wait_for_speech seconds.
        """
        chunk_size = 1024
        audio_data = []
        
        # Start a stream to check levels
        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
            silent_chunks = 0
            total_chunks = 0
            speech_started = False
            
            # Constants for timing
            limit_chunks = int(silence_limit * self.sample_rate / chunk_size)
            wait_chunks = int(wait_for_speech * self.sample_rate / chunk_size)
            max_chunks = int(max_duration * self.sample_rate / chunk_size)
            
            print("Listening...")
            
            while total_chunks < max_chunks:
                data, overflowed = stream.read(chunk_size)
                rms = np.sqrt(np.mean(data.astype(float)**2))
                
                if not speech_started:
                    # Wait for sound to exceed threshold
                    if rms > silence_threshold:
                        speech_started = True
                        print("Recording started...")
                        audio_data.append(data)
                    elif total_chunks > wait_chunks:
                        # No speech detected within timeout
                        print("No speech detected.")
                        return None
                else:
                    audio_data.append(data)
                    if rms < silence_threshold:
                        silent_chunks += 1
                    else:
                        silent_chunks = 0
                    
                    # Stop if silence limit reached
                    if silent_chunks > limit_chunks:
                        print("End of speech detected.")
                        break
                
                total_chunks += 1

        if not audio_data:
            return None
            
        recording = np.concatenate(audio_data, axis=0)
        
        # Convert to WAV format in memory
        byte_io = io.BytesIO()
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(recording.tobytes())
        
        byte_io.seek(0)
        
        with sr.AudioFile(byte_io) as source:
            return self.recognizer.record(source)

    def listen(self, fallback_text=None):
        """
        Listens for audio input and returns the recognized text.
        Optimized to skip recognition if no audio was captured.
        """
        if self.microphone_missing:
            if fallback_text: return fallback_text.lower()
            return ""

        if fallback_text:
            return fallback_text.lower()

        try:
            # Auto-detect speech and return early if silent
            audio = self._record_audio()
            
            if audio is None:
                return ""
            
            print("Recognizing...")
            # Use a slightly more robust timeout for the request itself
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
