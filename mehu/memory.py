import json
import os

class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._save([])

    def _load(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, role, message):
        history = self._load()
        history.append({"role": role, "content": message})
        self._save(history)

    def get_history(self, raw=False):
        history = self._load()
        if raw:
            return history
        return "\n".join(f"{m['role']}: {m['content']}" for m in history)

    def clear(self):
        self._save([])