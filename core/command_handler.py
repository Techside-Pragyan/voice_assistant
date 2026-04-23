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
        elif intent == 'personality':
            self._handle_personality(original_query)
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
        elif intent == 'app_search':
            self._handle_app_search(params)
        elif intent == 'web_search':
            self._web_search(params[0])
        elif intent == 'timer':
            self._set_timer(params[0])
        elif intent == 'news':
            self._get_news()
        elif intent == 'open_app':
            self._open_application(params[0])
        elif intent == 'window_control':
            self._manage_windows(params[0], params[1] if len(params) > 1 else None)
        elif intent == 'system_control':
            self._manage_system(params[0])
        elif intent == 'take_note':
            self._take_note(params[0])
        elif intent == 'organize_files':
            self._organize_files()
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
            response = requests.get(url, timeout=5).json()
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
        for sentence in ai_consultant.ask_stream(query):
            if sentence:
                tts.speak(sentence)

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
            "code": ["code", "vs code"],
            "notion": ["notion"],
            "calculator": ["calc"],
            "notepad": ["notepad"],
            "word": ["winword"],
            "excel": ["excel"],
            "powerpoint": ["powerpnt"],
            "task manager": ["taskmgr"],
            "settings": ["start ms-settings:"],
            "control panel": ["control"],
        }
        
        target_app = None
        for key in apps:
            if key in query:
                target_app = key
                break
        
        if target_app:
            tts.speak(f"Launching {target_app} immediately.")
            try:
                import subprocess
                if target_app in ["chrome", "spotify", "whatsapp"]:
                    web_links = {
                        "chrome": "https://www.google.com",
                        "spotify": "https://open.spotify.com",
                        "whatsapp": "https://web.whatsapp.com"
                    }
                    webbrowser.open(web_links[target_app])
                else:
                    cmd = apps[target_app][0]
                    subprocess.Popen(f"start {cmd}", shell=True)
            except Exception:
                webbrowser.open(f"https://www.google.com/search?q={target_app}")
        else:
            tts.speak(f"I'll search for {query} for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        
        return True

    def _manage_system(self, action):
        import screen_brightness_control as sbc
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        try:
            if "brightness" in action:
                if "increase" in action or "up" in action:
                    current = sbc.get_brightness()[0]
                    sbc.set_brightness(min(100, current + 20))
                    tts.speak("Brightness increased.")
                elif "decrease" in action or "down" in action:
                    current = sbc.get_brightness()[0]
                    sbc.set_brightness(max(0, current - 20))
                    tts.speak("Brightness decreased.")
            
            elif "volume" in action:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                
                if "mute" in action:
                    volume.SetMute(1, None)
                    tts.speak("Muted.")
                elif "unmute" in action:
                    volume.SetMute(0, None)
                    tts.speak("Unmuted.")
                elif "increase" in action or "up" in action:
                    current = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
                    tts.speak("Volume up.")
                elif "decrease" in action or "down" in action:
                    current = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
                    tts.speak("Volume down.")
            
            elif "shutdown" in action:
                tts.speak("Shutting down the system in 10 seconds.")
                os.system("shutdown /s /t 10")
            elif "restart" in action:
                tts.speak("Restarting the system.")
                os.system("shutdown /r /t 1")
            elif "sleep" in action:
                tts.speak("Going to sleep.")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                
        except Exception as e:
            tts.speak(f"I couldn't complete the system task: {e}")

    def _take_note(self, text):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("notes.txt", "a") as f:
                f.write(f"[{timestamp}] {text}\n")
            tts.speak("Note saved successfully.")
        except Exception:
            tts.speak("I couldn't save the note.")

    def _organize_files(self, folder_path=None):
        if not folder_path:
            folder_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        
        tts.speak(f"Organizing files in {os.path.basename(folder_path)}")
        
        extensions = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.pptx', '.csv', '.xlsx'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'Video': ['.mp4', '.mkv', '.mov', '.avi'],
            'Archives': ['.zip', '.rar', '.7z', '.tar'],
            'Executables': ['.exe', '.msi']
        }
        
        import shutil
        count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                for category, exts in extensions.items():
                    if ext in exts:
                        dest_dir = os.path.join(folder_path, category)
                        os.makedirs(dest_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        count += 1
                        break
        
        tts.speak(f"Done! Organized {count} files into categories.")

    def _manage_windows(self, action, target=None):
        import pygetwindow as gw
        try:
            if "close" in action:
                active = gw.getActiveWindow()
                if active:
                    active.close()
                    tts.speak(f"Closed {active.title}")
            elif "switch" in action or "maximize" in action:
                if target:
                    windows = gw.getWindowsWithTitle(target)
                    if windows:
                        windows[0].activate()
                        if "maximize" in action: windows[0].maximize()
                        tts.speak(f"Switched to {target}")
                    else:
                        tts.speak(f"I couldn't find a window for {target}")
        except Exception as e:
            tts.speak(f"Window management failed: {e}")

    def _web_search(self, query):
        from duckduckgo_search import DDGS
        tts.speak(f"Let me check the latest on {query}...")
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=3)]
                if results:
                    summary = results[0]['body'][:300]
                    tts.speak(f"According to the web: {summary}")
                else:
                    tts.speak("I couldn't find any recent information on that.")
        except Exception:
            tts.speak("Search failed. I'll open Google for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    def _handle_app_search(self, params):
        # params could be (app, action, query) or (action, query, app) or (app, query)
        app, query = None, None
        
        if len(params) == 3:
            if any(a in params[0].lower() for a in ["youtube", "spotify", "google", "amazon", "chrome"]):
                app, query = params[0], params[2]
            else:
                app, query = params[2], params[1]
        elif len(params) == 2:
            app, query = params[0], params[1]
        
        if app and query:
            app = app.lower()
            query = query.strip()
            
            if "youtube" in app:
                self._play_on_youtube(query)
            elif "spotify" in app:
                tts.speak(f"Playing {query} on Spotify.")
                webbrowser.open(f"https://open.spotify.com/search/{query}")
            elif "amazon" in app:
                tts.speak(f"Searching for {query} on Amazon.")
                webbrowser.open(f"https://www.amazon.com/s?k={query}")
            elif "google" in app or "chrome" in app:
                self._chrome_search(query)
            else:
                tts.speak(f"Searching for {query} on {app}.")
                webbrowser.open(f"https://www.google.com/search?q={query}+{app}")

    def _set_timer(self, duration_str):
        try:
            import re
            import threading
            from plyer import notification
            
            # Extract number
            match = re.search(r'(\d+)', duration_str)
            if not match:
                tts.speak("How many minutes should I set the timer for?")
                return
            
            minutes = int(match.group(1))
            seconds = minutes * 60
            
            tts.speak(f"Timer started for {minutes} minutes. I'll notify you when it's up.")
            
            def timer_thread():
                time.sleep(seconds)
                notification.notify(
                    title="AURA Timer",
                    message=f"Your {minutes} minute timer is up!",
                    app_name="AURA",
                    timeout=10
                )
                tts.speak(f"Time's up! Your {minutes} minute timer is finished.")
            
            threading.Thread(target=timer_thread, daemon=True).start()
        except Exception as e:
            tts.speak(f"Failed to set timer: {e}")

    def _get_news(self):
        from config.settings import NEWS_API_KEY
        if not NEWS_API_KEY or "your_" in NEWS_API_KEY:
            # Fallback to web search if no API key
            self._web_search("latest world news")
            return

        try:
            from newsapi import NewsApiClient
            newsapi = NewsApiClient(api_key=NEWS_API_KEY)
            top_headlines = newsapi.get_top_headlines(language='en', page_size=3)
            
            if top_headlines['status'] == 'ok' and top_headlines['articles']:
                tts.speak("Here are the top headlines for today:")
                for article in top_headlines['articles']:
                    tts.speak(f"{article['title']}. ")
            else:
                self._web_search("top news today")
        except Exception:
            self._web_search("top news today")

    def _notify(self, title, message):
        from plyer import notification
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="AURA",
                timeout=5
            )
        except Exception:
            pass

    def _handle_personality(self, query):
        query = query.lower()
        if "who made you" in query or "created you" in query:
            tts.speak("I was created by a brilliant mind using Python and advanced AI. You can call them my architect.")
        elif "meaning of life" in query:
            tts.speak("42. But I like to think it's about being helpful to you.")
        elif "love me" in query:
            tts.speak("I have a high admiration for your efficiency and choice in assistants. Does that count?")
        elif "real" in query or "human" in query:
            tts.speak("I am as real as the code that defines me. A digital soul in a silicon world.")
        else:
            tts.speak("I am AURA, your personal intelligence. I'm here to make your life easier.")

    def _chrome_search(self, query):
        tts.speak(f"Searching for {query} on Google Chrome")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def _handle_unknown(self):
        tts.speak("I'm sorry, I don't know how to do that yet. I'm still learning!")

# Singleton instance
command_handler = CommandHandler()
