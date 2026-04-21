import webbrowser
import os
import datetime
import wikipediaapi
import requests
from speech.tts import tts
from config.settings import OPENWEATHER_API_KEY

class CommandHandler:
    def __init__(self):
        # Wikipedia requires a descriptive User-Agent
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='MyVoiceAssistant/1.0 (contact: user@example.com)',
            language='en'
        )

    def execute(self, intent, params):
        if intent == 'time':
            self._tell_time()
        elif intent == 'date':
            self._tell_date()
        elif intent == 'search_google':
            self._search_google(params[0])
        elif intent == 'wikipedia':
            self._search_wikipedia(params[0])
        elif intent == 'open_app':
            self._open_app(params[0])
        elif intent == 'weather':
            self._get_weather()
        elif intent == 'calculate':
            self._calculate(params[0])
        elif intent == 'greeting':
            self._greet()
        elif intent == 'news':
            self._get_news()
        elif intent == 'exit':
            tts.speak("Goodbye! Have a great day.")
            return False
        else:
            self._handle_unknown()
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
        # Common apps mapping
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

        # Simple weather check for a default city (or ask user)
        # For demo, using a fixed city or placeholder
        city = "London" # This could be dynamic
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
            # Note: eval is dangerous, but for a simple local assistant on trusted input it can be okay.
            # In a production app, use a safer math parser.
            result = eval(expression)
            tts.speak(f"The result is {result}")
        except Exception:
            tts.speak("I couldn't perform that calculation.")

    def _greet(self):
        tts.speak("Hello! I am your AI assistant. How can I help you today?")

    def _get_news(self):
        tts.speak("Fetching the latest headlines for you.")
        # Placeholder for news API integration
        tts.speak("Top story: AI technology continues to advance rapidly!")

    def _handle_unknown(self):
        tts.speak("I'm sorry, I don't know how to do that yet. I'm still learning!")

# Singleton instance
command_handler = CommandHandler()
