import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")

    def load_api_key(self):
        if not self.api_key:
            raise ValueError("API key not found in .env")
        return self.api_key