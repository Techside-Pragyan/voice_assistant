import tkinter as tk
from tkinter import ttk
import threading
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
        
        # Load Anime Avatar
        try:
            from PIL import Image, ImageTk
            import os
            # Image path from previous generation
            img_path = r"C:\Users\pragy\.gemini\antigravity\brain\dc4f1202-b66c-4ee0-aaa1-3a79ddd3634f\anime_girl_assistant_avatar_1776784986376.png"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((250, 250), Image.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(img)
                self.avatar_display = self.canvas.create_image(150, 125, image=self.avatar_img)
            else:
                self.avatar_display = self.canvas.create_oval(75, 50, 225, 200, fill="#bb9af7", outline="")
        except Exception as e:
            print(f"Image load error: {e}")
            self.avatar_display = self.canvas.create_oval(75, 50, 225, 200, fill="#bb9af7", outline="")
        
        # Glow Effect Ring (Vibrant Purple/Blue)
        self.glow_ring = self.canvas.create_oval(25, 10, 275, 260, outline="#bb9af7", width=2)
        
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
        if self.status_label.cget("text") == "RECORDING...":
            if self.pulse_growing:
                self.pulse_size += 3
                if self.pulse_size > 15: self.pulse_growing = False
            else:
                self.pulse_size -= 3
                if self.pulse_size < 0: self.pulse_growing = True
            
            # Update glow ring size around the avatar
            self.canvas.coords(self.glow_ring, 25-self.pulse_size, 10-self.pulse_size, 275+self.pulse_size, 260+self.pulse_size)
        else:
            # Reset to normal size if not recording
            self.canvas.coords(self.glow_ring, 25, 10, 275, 260)
            
        self.root.after(50, self.animate_pulse)

    def run_assistant_logic(self):
        self.update_status("Standby", "#5865f2")
        tts.speak(f"AURA system is online.")
        
        active = False
        last_active_time = 0
        
        import time
        while True:
            try:
                fallback_text = None
                if self.command_queue:
                    fallback_text = self.command_queue.pop(0)

                # Status updates
                current_status = "Standby" if not active else "Recording..."
                self.update_status(current_status, "#5865f2" if not active else "#f38ba8")

                query = recognizer.listen(fallback_text=fallback_text)
                
                if not query:
                    # If we have been active but no one spoke for 10 seconds, go to standby
                    if active and (time.time() - last_active_time > 10):
                        active = False
                        self.update_status("Standby", "#5865f2")
                    time.sleep(0.1)
                    continue

                self.update_transcript(f"User: {query}")

                # Check for wake word (Broadening for common mishearings)
                wake_words = ["aura", "ora", "aiora", "hiora", "ahura"]
                wake_word_detected = any(word in query.lower() for word in wake_words)

                if wake_word_detected:
                    active = True
                    last_active_time = time.time()
                    
                    # Try to remove the wake word from the query
                    clean_query = query.lower()
                    for word in wake_words:
                        clean_query = clean_query.replace(word, "")
                    clean_query = clean_query.replace("hey", "").replace("hi", "").strip()
                    
                    if not clean_query:
                        tts.speak("Yes? I'm listening.")
                        continue
                    else:
                        query = clean_query

                if active:
                    # Stay awake for 30 seconds
                    last_active_time = time.time()
                    
                    if not query:
                        continue

                    self.update_status("Thinking...", "#fab387")
                    intent, params = intent_engine.get_intent(query)
                    should_continue = command_handler.execute(intent, params)
                    
                    if not should_continue:
                        self.root.after(1000, self.root.quit)
                        break
                
            except Exception as e:
                print(f"Logic Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    app.animate_pulse()
    root.mainloop()
