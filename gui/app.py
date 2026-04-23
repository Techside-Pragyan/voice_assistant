import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import random
from speech.recognition import recognizer
from speech.tts import tts
from core.intent_engine import intent_engine
from core.command_handler import command_handler
from config.settings import WAKE_WORD, ASSISTANT_NAME

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{ASSISTANT_NAME}")
        self.root.geometry("400x550")
        self.root.configure(bg="#0f0f1a") # Deeper dark background
        self.root.resizable(False, False)

        self._setup_ui()
        self.pulse_size = 0
        self.pulse_growing = True
        
        # Connect TTS to GUI for visual feedback
        tts.set_gui_callback(self.update_transcript)
        
        # Start assistant thread
        self.assistant_thread = threading.Thread(target=self.run_assistant_logic, daemon=True)
        self.assistant_thread.start()

    def _setup_ui(self):
        # Header with Gradient-like label
        self.header = tk.Label(
            self.root, 
            text="AURA", # Artificial User Responsive Agent
            font=("Inter", 24, "bold"),
            bg="#0f0f1a", 
            fg="#5865f2" # Vibrant Blue
        )
        self.header.pack(pady=(30, 10))

        self.subtitle = tk.Label(
            self.root,
            text="Personal Intelligence",
            font=("Inter", 10),
            bg="#0f0f1a",
            fg="#6c7086"
        )
        self.subtitle.pack()

        # Voice Visualization & Avatar Area
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="#0f0f1a", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Load 3D Live Avatar (Snapchat Style Frames)
        try:
            from PIL import Image, ImageTk
            import os
            # Paths
            path_closed = r"C:\Users\pragy\.gemini\antigravity\brain\dc4f1202-b66c-4ee0-aaa1-3a79ddd3634f\3d_avatar_closed_mouth_1776787113809.png"
            path_open = r"C:\Users\pragy\.gemini\antigravity\brain\dc4f1202-b66c-4ee0-aaa1-3a79ddd3634f\3d_avatar_open_mouth_1776787155269.png"
            
            self.frames = []
            for p in [path_closed, path_open]:
                img = Image.open(p).resize((300, 300), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(img))
            
            self.avatar_display = self.canvas.create_image(150, 150, image=self.frames[0])
            self.voice_frame_counter = 0
        except Exception as e:
            print(f"Image load error: {e}")
            self.avatar_display = self.canvas.create_oval(75, 50, 225, 200, fill="#FFFC00", outline="")
        
        # Glow Effect Ring (Snapchat Gold)
        self.glow_ring = self.canvas.create_oval(10, 5, 290, 290, outline="#FFFC00", width=3)
        
        # Status Text with better font
        self.status_label = tk.Label(
            self.root, 
            text="SYSTEM ONLINE", 
            font=("Inter", 10, "bold"),
            bg="#0f0f1a", 
            fg="#a6e3a1"
        )
        self.status_label.pack(pady=10)

        # Transcript Area with scrolling capability
        self.transcript_frame = tk.Frame(self.root, bg="#181825", padx=15, pady=10)
        self.transcript_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.transcript_label = tk.Label(
            self.transcript_frame, 
            text="Greeting...", 
            font=("Inter", 10),
            bg="#181825", 
            fg="#cdd6f4",
            wraplength=320,
            justify="left"
        )
        self.transcript_label.pack(anchor="w")

        # Fallback Text Input (at the bottom)
        self.input_frame = tk.Frame(self.root, bg="#0f0f1a")
        self.input_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 20))
        
        self.user_input = tk.Entry(
            self.input_frame, 
            bg="#181825", 
            fg="#cdd6f4", 
            insertbackground="white",
            borderwidth=0,
            font=("Inter", 10)
        )
        self.user_input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.send_text_command())

        self.send_btn = tk.Button(
            self.input_frame,
            text="➤",
            command=self.send_text_command,
            bg="#5865f2",
            fg="white",
            borderwidth=0,
            padx=10
        )
        self.send_btn.pack(side="right")
        
        # Queue for passing text commands to the logic thread
        self.command_queue = []

    def send_text_command(self):
        text = self.user_input.get()
        if text:
            self.command_queue.append(text)
            self.user_input.delete(0, tk.END)

    def update_status(self, text, color="#89b4fa"):
        self.status_label.config(text=text.upper(), fg=color)
        self.canvas.itemconfig(self.glow_ring, outline=color)

    def update_transcript(self, text):
        self.transcript_label.config(text=text)

    def animate_pulse(self):
        # 1. Floating & Breathing Logic
        t = time.time()
        # Substantially bigger floating for 'Live' feel
        float_y = math.sin(t * 3) * 8
        jitter_x, jitter_y = 0, 0
        
        # 2. Status & Talking Logic
        current_text = self.status_label.cget("text")
        is_talking = "SPEAKING" in current_text or tts.is_speaking
        
        if is_talking:
            jitter_x = random.randint(-3, 3)
            jitter_y = random.randint(-3, 3)
            self.update_status("Speaking...", "#a6e3a1")
        
        # 3. Avatar Move (Safely handle if image or oval)
        try:
            self.canvas.coords(self.avatar_display, 150 + jitter_x, 150 + float_y + jitter_y)
            if hasattr(self, 'frames') and len(self.frames) > 1:
                # Active Lip Sync
                if is_talking:
                    self.voice_frame_counter += 1
                    frame_idx = (self.voice_frame_counter // 2) % 2
                    self.canvas.itemconfig(self.avatar_display, image=self.frames[frame_idx])
                else:
                    self.canvas.itemconfig(self.avatar_display, image=self.frames[0])
                    self.voice_frame_counter = 0
        except Exception:
            pass # Prevent total crash if animation fails

        # 4. Glow Ring Logic (Brighter & More Pulsing)
        is_active = is_talking or current_text in ["LISTENING...", "RECORDING...", "THINKING..."]
        
        if is_active:
            if self.pulse_growing:
                self.pulse_size += 5
                if self.pulse_size > 25: self.pulse_growing = False
            else:
                self.pulse_size -= 5
                if self.pulse_size < 0: self.pulse_growing = True
            
            # Glow Color based on state
            glow_color = "#bb9af7" # Default Active
            if "SPEAKING" in current_text: glow_color = "#a6e3a1"
            if "THINKING" in current_text: glow_color = "#fab387"
            
            self.canvas.itemconfig(self.glow_ring, width=5, outline=glow_color)
            self.canvas.coords(self.glow_ring, 25-self.pulse_size, 10-self.pulse_size, 275+self.pulse_size, 260+self.pulse_size)
        else:
            self.pulse_size = 0
            self.canvas.itemconfig(self.glow_ring, width=2, outline="#5865f2")
            self.canvas.coords(self.glow_ring, 25, 10, 275, 260)
            
        self.root.after(50, self.animate_pulse)

    def run_assistant_logic(self):
        self.update_status("Standby", "#5865f2")
        tts.speak(f"Hello! I'm AURA. I'm so happy to talk with you.")
        
        # Start voice listener in background
        threading.Thread(target=self.voice_listener_loop, daemon=True).start()
        
        active = False
        last_active_time = time.time()
        
        while True:
            try:
                # Check for commands (voice or text)
                if not self.command_queue:
                    if active and (time.time() - last_active_time > 30):
                        active = False
                        self.update_status("Standby", "#5865f2")
                    time.sleep(0.05) # Faster polling
                    continue

                query = self.command_queue.pop(0)
                if not query: continue

                self.update_transcript(f"User: {query}")
                last_active_time = time.time()

                # Process
                self.process_command(query, active)
                active = True 
                
            except Exception as e:
                time.sleep(0.5)

    def voice_listener_loop(self):
        while True:
            try:
                if tts.is_speaking:
                    time.sleep(0.1) # Faster check
                    continue
                
                query = recognizer.listen()
                if query:
                    self.command_queue.append(query)
                else:
                    time.sleep(0.05) # Faster loop
            except Exception as e:
                time.sleep(0.5)

    def process_command(self, query, was_active):
        direct_keywords = ["open", "start", "launch", "play", "what", "how", "tell", "show", "search"]
        is_direct = any(word in query.lower() for word in direct_keywords)
        wake_words = ["aura", "ora", "aiora", "hiora", "ahura"]
        wake_word_detected = any(word in query.lower() for word in wake_words)

        if wake_word_detected or is_direct or was_active:
            clean_query = query.lower()
            for word in wake_words:
                clean_query = clean_query.replace(word, "")
            clean_query = clean_query.replace("hey", "").replace("hi", "").strip()
            
            if not clean_query and wake_word_detected:
                tts.speak("I'm listening! What can I do for you?")
                return

            # Only show "Thinking..." for potentially slow operations
            slow_intents = ["unknown", "wikipedia", "weather", "news", "stocks"]
            intent, params = intent_engine.get_intent(clean_query if clean_query else query)
            
            if intent in slow_intents:
                self.update_status("Thinking...", "#fab387")
            
            should_continue = command_handler.execute(intent, params, original_query=clean_query if clean_query else query)
            
            self.update_status("Listening..." if should_continue else "Shutting down", "#bb9af7")
            if not should_continue:
                self.root.after(1000, self.root.quit)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    app.animate_pulse()
    root.mainloop()
