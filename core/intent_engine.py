import re

class IntentEngine:
    def __init__(self):
        # Organized by frequency and importance for faster matching
        self.intents = {
            'greeting': [r'^hello', r'^hi', r'^hey', r'good morning'],
            'personality': [r'who (made|created) you', r'meaning of life', r'do you love me', r'are you (real|human)'],
            'time': [r'time'],
            'date': [r'date', r'today'],
            'weather': [r'weather', r'temperature'],
            'system_control': [r'volume (up|down|mute|unmute)', r'brightness (up|down|increase|decrease)', r'shutdown', r'restart', r'sleep'],
            'window_control': [r'close (this |the )?window', r'switch to (.+)', r'maximize (.+)'],
            'take_note': [r'take a note (.+)', r'write down (.+)', r'remember (.+)'],
            'organize_files': [r'organize my files', r'clean my downloads', r'organize downloads'],
            'app_search': [r'open (.+) and (search for|play) (.+)', r'(search|play) (.+) on (.+)', r'^(youtube|spotify|google|amazon) (.+)'],
            'web_search': [r'search the web for (.+)', r'find out (.+)', r'who is (.+)', r'what is the latest (.+)'],
            'timer': [r'set (a )?timer for (\d+) minutes', r'timer (\d+) minutes', r'remind me in (\d+) minutes'],
            'news': [r'what is the news', r'give me (the )?news', r'headlines', r'what\'s happening'],
            'open_app': [r'open (.+)', r'launch (.+)', r'start (.+)'],
            'play_music': [r'play (.+)'],
            'search_google': [r'search for (.+)', r'google (.+)', r'search (.+) on google'],
            'wikipedia': [r'wikipedia (.+)', r'who is (.+)', r'what is (.+)'],
            'calculate': [r'calculate (.+)', r'what is (\d+ [\+\-\*\/] \d+)'],
            'exit': [r'exit', r'stop', r'shutdown', r'bye'],
            'news': [r'news', r'headlines'],
            'lock_pc': [r'lock my pc', r'lock the screen'],
            'joke': [r'joke', r'funny'],
            'screenshot': [r'screenshot', r'take a photo'],
            'volume': [r'volume to (\d+)', r'set volume to (\d+)'],
            'stocks': [r'stock price of (.+)', r'how is (.+) stock'],
            'maps': [r'where is (.+)', r'show me (.+) on map'],
            'change_name': [r'call me (.+)', r'my name is (.+)']
        }
        # Pre-compile regex for speed
        self.compiled_intents = {
            intent: [re.compile(p, re.IGNORECASE) for p in patterns]
            for intent, patterns in self.intents.items()
        }

    def get_intent(self, text):
        text = text.lower().strip()
        if not text: return 'unknown', None
        
        # Fast path for very short queries
        if text in ['hello', 'hi', 'hey']: return 'greeting', None
        if text == 'time': return 'time', None
        
        for intent, patterns in self.compiled_intents.items():
            for pattern in patterns:
                match = pattern.search(text)
                if match:
                    return intent, match.groups()
        return 'unknown', None

# Singleton instance
intent_engine = IntentEngine()
