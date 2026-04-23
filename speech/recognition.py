import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave
import logging

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300 # More sensitive
        self.recognizer.dynamic_energy_threshold = False # Faster start
        self.sample_rate = 16000
        self.microphone_missing = False
        
        print("Initializing AURA Voice Engine (Optimized)...")
        try:
            sd.query_devices(kind='input')
        except Exception as e:
            print(f"Warning: No input device found: {e}")
            self.microphone_missing = True

    def _record_audio(self, max_duration=7, silence_threshold=500, silence_limit=0.3, wait_for_speech=0.8):
        """
        Hyper-optimized audio recording. 
        - Lower silence limit (0.35s) for instant cutoff after speaking.
        - Lower wait_for_speech (1.2s) to stop listening faster if no speech.
        """
        chunk_size = 512 # Smaller chunks for finer control
        audio_data = []
        
        try:
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
        except Exception:
            return None

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
            
            # Using recognize_google with show_all=False
            # Google is generally the fastest cloud-based choice for short phrases
            text = self.recognizer.recognize_google(audio, language='en-in')
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""

# Singleton instance
recognizer = SpeechRecognizer()

