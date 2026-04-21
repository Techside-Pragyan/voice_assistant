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
        self.update_status("Standby", "#5865f2")
        tts.speak(f"System online.")
        
        active = False
        
        import time
        while True:
            try:
                # Check for manual text commands from the GUI
                fallback_text = None
                if self.command_queue:
                    fallback_text = self.command_queue.pop(0)

                if not active:
                    self.update_status("Standby", "#5865f2")
                    query = recognizer.listen(fallback_text=fallback_text)
                    
                    if query and WAKE_WORD in query:
                        active = True
                        self.update_status("Listening...", "#a6e3a1")
                        tts.speak("How can I help?")
                    
                    if not query:
                        time.sleep(0.1) # Prevent high CPU when idle
                    continue

                self.update_status("Listening...", "#a6e3a1")
                query = recognizer.listen(fallback_text=fallback_text)
                
                if not query:
                    if recognizer.microphone_missing:
                        time.sleep(0.1) # Wait for text input
                    else:
                        active = False # Timeout on voice
                    continue

                self.update_transcript(f"User: {query}")
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
