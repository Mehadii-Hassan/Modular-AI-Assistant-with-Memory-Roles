import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

    def load_api_key(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        return api_key
