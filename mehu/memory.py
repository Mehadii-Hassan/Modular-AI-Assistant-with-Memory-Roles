import json
import os

class Memory:
    FILE = "memory.json"

    def __init__(self):
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f:
                json.dump([], f)

    def add(self, role, message):
        history = self.get_history()
        history.append({"role": role, "content": message})
        with open(self.FILE, "w") as f:
            json.dump(history, f, indent=2)

    def get_history(self):
        try:
            with open(self.FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def clear(self):
        with open(self.FILE, "w") as f:
            json.dump([], f)
