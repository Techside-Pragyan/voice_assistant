import json
import os
from config.settings import BASE_DIR

MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")

class Memory:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {"user_name": "User", "preferences": {}}

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

# Singleton instance
memory = Memory()
