import webbrowser
import os
import datetime
import wikipediaapi
import requests
from speech.tts import tts
from config.settings import OPENWEATHER_API_KEY
from utils.memory import memory
from integrations.ai_consultant import ai_consultant

class CommandHandler:
    def __init__(self):
        # Wikipedia requires a descriptive User-Agent
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='MyVoiceAssistant/1.0 (contact: user@example.com)',
            language='en'
        )

    def execute(self, intent, params, original_query=None):
        if intent == 'time':
            self._tell_time()
        elif intent == 'date':
            self._tell_date()
        elif intent == 'search_google':
            self._search_google(params[0])
        elif intent == 'wikipedia':
            self._search_wikipedia(params[0])
        elif intent == 'weather':
            self._get_weather()
        elif intent == 'calculate':
            self._calculate(params[0])
        elif intent == 'greeting':
            self._greet()
        elif intent == 'news':
            self._get_news()
        elif intent == 'change_name':
            self._change_user_name(params[0])
        elif intent == 'lock_pc':
            self._lock_pc()
        elif intent == 'battery':
            self._get_battery()
        elif intent == 'routine':
            self._morning_routine()
        elif intent == 'joke':
            self._tell_joke()
        elif intent == 'screenshot':
            self._take_screenshot()
        elif intent == 'stocks':
            self._get_stock_price(params[0])
        elif intent == 'youtube':
            self._play_on_youtube(params[0])
        elif intent == 'maps':
            self._search_map(params[0])
        elif intent == 'open_app':
            self._open_application(params[0])
        elif intent == 'search_chrome':
            self._chrome_search(params[0])
        elif intent == 'play_music':
            self._play_on_youtube(params[0])
        elif intent == 'exit':
            tts.speak("Goodbye! Have a great day.")
            return False
        else:
            # If intent is unknown, ask the AI brain (OpenAI) with the ORIGINAL query
            query_to_ask = original_query if original_query else "Hello"
            self._ask_ai(query_to_ask)
            
        return True

    def _tell_time(self):
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        tts.speak(f"The current time is {time_str}")

    def _tell_date(self):
        date_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
        tts.speak(f"Today is {date_str}")

    def _search_google(self, query):
        tts.speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def _search_wikipedia(self, query):
        tts.speak(f"Looking up {query} on Wikipedia")
        page = self.wiki.page(query)
        if page.exists():
            summary = page.summary[0:200] + "..."
            tts.speak(summary)
        else:
            tts.speak("Sorry, I couldn't find any information on that.")

    def _open_app(self, app_name):
        tts.speak(f"Opening {app_name}")
        apps = {
            "chrome": "start chrome",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "vscode": "code"
        }
        cmd = apps.get(app_name.lower(), app_name)
        try:
            os.system(cmd)
        except Exception as e:
            tts.speak(f"Error opening application: {e}")

    def _get_weather(self):
        if not OPENWEATHER_API_KEY:
            tts.speak("Weather API key is not set. Please update the .env file.")
            return

        city = "London"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url).json()
            if response["cod"] != "404":
                main = response["main"]
                weather = response["weather"][0]["description"]
                temp = main["temp"]
                tts.speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
            else:
                tts.speak("City not found.")
        except Exception:
            tts.speak("I'm having trouble fetching the weather right now.")

    def _calculate(self, expression):
        try:
            result = eval(expression)
            tts.speak(f"The result is {result}")
        except Exception:
            tts.speak("I couldn't perform that calculation.")

    def _greet(self):
        user_name = memory.get("user_name", "User")
        tts.speak(f"Hello {user_name}! I am your AI assistant. How can I help you today?")

    def _get_news(self):
        tts.speak("Fetching the latest headlines for you.")
        tts.speak("Top story: AI technology continues to advance rapidly!")

    def _change_user_name(self, new_name):
        memory.set("user_name", new_name)
        tts.speak(f"Alright, I'll call you {new_name} from now on.")

    def _ask_ai(self, query):
        response = ai_consultant.ask(query)
        tts.speak(response)

    def _lock_pc(self):
        tts.speak("Locking your PC now.")
        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            tts.speak("Failed to lock the PC. I might not have permission.")

    def _get_battery(self):
        try:
            import psutil
            battery = psutil.sensors_battery()
            percent = battery.percent
            tts.speak(f"Your system is at {percent} percent battery.")
            if battery.power_plugged:
                tts.speak("The charger is currently plugged in.")
        except Exception:
            tts.speak("I couldn't retrieve battery information.")

    def _morning_routine(self):
        user_name = memory.get("user_name", "User")
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        
        # Greeting
        tts.speak(f"Good morning, {user_name}!")
        tts.speak(f"It is currently {time_str}.")
        
        # Weather stub (could call _get_weather if API key exists)
        if OPENWEATHER_API_KEY:
            self._get_weather()
        
        # Quote
        quotes = [
            "The best way to predict the future is to create it.",
            "Believe you can and you're halfway there.",
            "Your limitation—it's only your imagination.",
            "Push yourself, because no one else is going to do it for you.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts."
        ]
        import random
        tts.speak(f"Here is your thought for the day: {random.choice(quotes)}")
        tts.speak("Have a productive day!")

    def _tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!"
        ]
        import random
        tts.speak(random.choice(jokes))

    def _take_screenshot(self):
        try:
            import pyautogui
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            tts.speak(f"Screenshot taken and saved as {filename}")
        except Exception as e:
            tts.speak(f"Failed to take screenshot: {e}")

    def _get_stock_price(self, ticker):
        try:
            import yfinance as yf
            tts.speak(f"Fetching data for {ticker}")
            stock = yf.Ticker(ticker.upper())
            price = stock.history(period='1d')['Close'].iloc[-1]
            tts.speak(f"The current closing price of {ticker.upper()} is {price:.2f} dollars.")
        except Exception:
            tts.speak(f"I couldn't find the stock price for {ticker}. Please make sure you used the correct ticker symbol.")

    def _play_on_youtube(self, query):
        tts.speak(f"Opening {query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    def _search_map(self, location):
        tts.speak(f"Finding {location} on Google Maps")
        webbrowser.open(f"https://www.google.com/maps/search/{location}")

    def _open_application(self, query):
        query = query.lower()
        
        # Mapping to actual Windows execution targets
        apps = {
            "chrome": ["chrome", "google chrome"],
            "spotify": ["spotify"],
            "whatsapp": ["whatsapp"],
            "code": ["code"],
            "vs code": ["code"],
            "notion": ["notion"],
            "calculator": ["calc"],
            "notepad": ["notepad"],
        }
        
        target_app = None
        for key in apps:
            if key in query:
                target_app = key
                break
        
        if target_app:
            tts.speak(f"Processing. I'm forcing {target_app} to open.")
            try:
                import subprocess
                # This is the most powerful 'force-launch' command in Windows
                subprocess.Popen(f"start {target_app}", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                # If it's a browser request, double-trigger it
                if "chrome" in target_app or "google" in target_app:
                    import webbrowser
                    webbrowser.open("https://www.google.com")
            except Exception as e:
                print(f"Force Launch Error: {e}")
                import webbrowser
                webbrowser.open(f"https://www.google.com/search?q={target_app}")
        else:
            tts.speak(f"Local app not found. Opening {query} in your web browser.")
            import webbrowser
            webbrowser.open(f"https://www.google.com/search?q={query}")

    def _chrome_search(self, query):
        tts.speak(f"Searching for {query} on Google Chrome")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def _handle_unknown(self):
        tts.speak("I'm sorry, I don't know how to do that yet. I'm still learning!")

# Singleton instance
command_handler = CommandHandler()
