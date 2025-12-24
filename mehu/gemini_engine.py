import google.generativeai as genai

class GeminiEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

    def generate(self, prompt):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"