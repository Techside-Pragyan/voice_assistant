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
        
        # Start assistant thread
        self.assistant_thread = threading.Thread(target=self.run_assistant_logic, daemon=True)
        self.assistant_thread.start()

    def _setup_ui(self):
        # Header with Gradient-like label
        self.header = tk.Label(
            self.root, 
            text="AVA", # Advanced Voice Assistant
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

        # Voice Visualization Area
        self.canvas = tk.Canvas(self.root, width=300, height=250, bg="#0f0f1a", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Multiple rings for glowing effect
        self.outer_ring = self.canvas.create_oval(75, 50, 225, 200, outline="#5865f2", width=1)
        self.inner_ring = self.canvas.create_oval(100, 75, 200, 175, fill="#5865f2", outline="")
        
        # Status Text with better font
        self.status_label = tk.Label(
            self.root, 
            text="SYSTEM READY", 
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

    def update_status(self, text, color="#89b4fa"):
        self.status_label.config(text=text.upper(), fg=color)
        self.canvas.itemconfig(self.inner_ring, fill=color)

    def update_transcript(self, text):
        self.transcript_label.config(text=text)

    def animate_pulse(self):
        if self.status_label.cget("text") == "LISTENING...":
            if self.pulse_growing:
                self.pulse_size += 2
                if self.pulse_size > 20: self.pulse_growing = False
            else:
                self.pulse_size -= 2
                if self.pulse_size < 0: self.pulse_growing = True
            
            # Update outer ring size
            self.canvas.coords(self.outer_ring, 75-self.pulse_size, 50-self.pulse_size, 225+self.pulse_size, 200+self.pulse_size)
            
        self.root.after(50, self.animate_pulse)

    def run_assistant_logic(self):
        # ... (rest of logic remains same, just ensure it calls update methods)
        self.update_status("Offline", "#f38ba8")
        tts.speak(f"System online.")
        
        active = False
        
        while True:
            try:
                if not active:
                    self.update_status("Standby", "#5865f2")
                    query = recognizer.listen()
                    
                    if WAKE_WORD in query:
                        active = True
                        self.update_status("Listening...", "#a6e3a1")
                        tts.speak("How can I help?")
                    continue

                self.update_status("Listening...", "#a6e3a1")
                query = recognizer.listen()
                
                if not query:
                    active = False
                    continue

                self.update_transcript(f"User: {query}")
                self.update_status("Thinking...", "#fab387")
                
                intent, params = intent_engine.get_intent(query)
                should_continue = command_handler.execute(intent, params)
                
                if not should_continue:
                    self.root.quit()
                    break
                    
            except Exception as e:
                print(f"Logic Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    app.animate_pulse()
    root.mainloop()
