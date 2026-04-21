import sys
import time
from speech.recognition import recognizer
from speech.tts import tts
from core.intent_engine import intent_engine
from core.command_handler import command_handler
from config.settings import WAKE_WORD, ASSISTANT_NAME

def run_assistant():
    tts.speak(f"{ASSISTANT_NAME} is online and ready.")
    
    active = False
    
    while True:
        try:
            # If not active, listen for the wake word
            if not active:
                print(f"Waiting for wake word: '{WAKE_WORD}'...")
                query = recognizer.listen()
                
                if WAKE_WORD in query:
                    active = True
                    tts.speak("How can I help you?")
                continue

            # If active, listen for commands
            query = recognizer.listen()
            
            if not query:
                # If no speech detected for a while, go back to wake word mode
                active = False
                continue

            # Process the command
            intent, params = intent_engine.get_intent(query)
            
            # Execute command
            should_continue = command_handler.execute(intent, params)
            
            if not should_continue:
                break
                
        except KeyboardInterrupt:
            print("\nStopping assistant...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        import tkinter as tk
        from gui.app import VoiceAssistantGUI
        root = tk.Tk()
        app = VoiceAssistantGUI(root)
        root.mainloop()
    else:
        run_assistant()
