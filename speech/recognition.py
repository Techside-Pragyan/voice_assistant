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

    def _record_audio(self, max_duration=8, silence_threshold=600, silence_limit=0.45, wait_for_speech=1.5):
        """
        Ultra-fast audio recording. Optimized for near-instant response.
        """
        chunk_size = 1024
        audio_data = []
        
        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
            silent_chunks = 0
            total_chunks = 0
            speech_started = False
            
            # Pre-calculate limits for speed
            limit_chunks = int(silence_limit * self.sample_rate / chunk_size)
            wait_chunks = int(wait_for_speech * self.sample_rate / chunk_size)
            max_chunks = int(max_duration * self.sample_rate / chunk_size)
            
            while total_chunks < max_chunks:
                data, _ = stream.read(chunk_size)
                # Use max amplitude instead of RMS for raw speed
                amplitude = np.max(np.abs(data))
                
                if not speech_started:
                    if amplitude > silence_threshold:
                        speech_started = True
                        audio_data.append(data)
                    elif total_chunks > wait_chunks:
                        return None
                else:
                    audio_data.append(data)
                    if amplitude < silence_threshold:
                        silent_chunks += 1
                    else:
                        silent_chunks = 0
                    
                    if silent_chunks > limit_chunks:
                        break
                
                total_chunks += 1

        if not audio_data: return None
        recording = np.concatenate(audio_data, axis=0)
        
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
        if self.microphone_missing or fallback_text:
            return (fallback_text or "").lower()

        try:
            audio = self._record_audio()
            if not audio: return ""
            
            # Using recognize_google with show_all=False for slightly faster processing
            return self.recognizer.recognize_google(audio, language='en-in').lower()
        except:
            return ""

# Singleton instance
recognizer = SpeechRecognizer()
