import re

class IntentEngine:
    def __init__(self):
        self.intents = {
            'time': [r'time', r'what time'],
            'date': [r'date', r'today\'s date', r'what day'],
            'search_google': [r'search for (.+)', r'google (.+)', r'search (.+) on google'],
            'wikipedia': [r'wikipedia (.+)', r'who is (.+)', r'what is (.+)'],
            'open_app': [r'open (.+)', r'launch (.+)'],
            'weather': [r'weather', r'temperature'],
            'calculate': [r'calculate (.+)', r'what is (\d+ [\+\-\*\/] \d+)'],
            'exit': [r'exit', r'stop', r'shutdown', r'bye'],
            'greeting': [r'hello', r'hi', r'hey'],
            'news': [r'news', r'headlines'],
            'change_name': [r'call me (.+)', r'my name is (.+)', r'change my name to (.+)']
        }

    def get_intent(self, text):
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    # Return intent and any captured groups (parameters)
                    return intent, match.groups()
        return 'unknown', None

# Singleton instance
intent_engine = IntentEngine()
