import json
import os

class Memory:
    def __init__(self, file_path="conversation.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def add(self, role, message):
        history = self.get_history()
        history.append({"role": role, "message": message})
        with open(self.file_path, "w") as f:
            json.dump(history, f, indent=2)

    def get_history(self):
        with open(self.file_path, "r") as f:
            return json.load(f)
