import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

    def load_api_key(self):
        return os.getenv("GEMINI_API_KEY", "")
