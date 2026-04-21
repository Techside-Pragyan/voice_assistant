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
        self.root.title(f"{ASSISTANT_NAME} - AI Voice Assistant")
        self.root.geometry("400x500")
        self.root.configure(bg="#1e1e2e")  # Dracular-ish background
        self.root.resizable(False, False)

        self._setup_ui()
        self.running = True
        
        # Start assistant thread
        self.assistant_thread = threading.Thread(target=self.run_assistant_logic, daemon=True)
        self.assistant_thread.start()

    def _setup_ui(self):
        # Header
        self.header = tk.Label(
            self.root, 
            text=ASSISTANT_NAME.upper(), 
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e", 
            fg="#cdd6f4"
        )
        self.header.pack(pady=20)

        # Status Indicator Circle
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.circle = self.canvas.create_oval(50, 50, 150, 150, fill="#89b4fa", outline="")
        
        # Status Text
        self.status_label = tk.Label(
            self.root, 
            text="Initializing...", 
            font=("Helvetica", 12),
            bg="#1e1e2e", 
            fg="#a6adc8"
        )
        self.status_label.pack(pady=10)

        # Transcript Area
        self.transcript_label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 10, "italic"),
            bg="#1e1e2e", 
            fg="#9399b2",
            wraplength=350
        )
        self.transcript_label.pack(pady=20)

        # Footer
        footer = tk.Label(
            self.root, 
            text=f"Say '{WAKE_WORD}'", 
            font=("Helvetica", 9),
            bg="#1e1e2e", 
            fg="#6c7086"
        )
        footer.pack(side="bottom", pady=10)

    def update_status(self, text, color="#89b4fa"):
        self.status_label.config(text=text)
        self.canvas.itemconfig(self.circle, fill=color)

    def update_transcript(self, text):
        self.transcript_label.config(text=text)

    def run_assistant_logic(self):
        self.update_status("Offline", "#f38ba8")
        tts.speak(f"{ASSISTANT_NAME} is active.")
        
        active = False
        
        while self.running:
            try:
                if not active:
                    self.update_status(f"Waiting for '{WAKE_WORD}'...", "#89b4fa")
                    query = recognizer.listen()
                    
                    if WAKE_WORD in query:
                        active = True
                        self.update_status("Listening...", "#a6e3a1")
                        tts.speak("Yes, I'm listening.")
                    continue

                self.update_status("Listening...", "#a6e3a1")
                query = recognizer.listen()
                
                if not query:
                    active = False
                    continue

                self.update_transcript(f"User: {query}")
                
                intent, params = intent_engine.get_intent(query)
                self.update_status("Thinking...", "#fab387")
                
                # Execute command
                should_continue = command_handler.execute(intent, params)
                
                if not should_continue:
                    self.root.quit()
                    break
                    
            except Exception as e:
                print(f"Logic Error: {e}")
                self.update_status("Error occurred", "#f38ba8")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    
    # Add a pulse effect to the circle for "Listening" state
    def pulse():
        if app.status_label.cget("text") == "Listening...":
            # Just a simple color flicker for demo
            current_color = app.canvas.itemcget(app.circle, "fill")
            next_color = "#94e2d5" if current_color == "#a6e3a1" else "#a6e3a1"
            app.canvas.itemconfig(app.circle, fill=next_color)
        root.after(500, pulse)
    
    pulse()
    root.mainloop()
