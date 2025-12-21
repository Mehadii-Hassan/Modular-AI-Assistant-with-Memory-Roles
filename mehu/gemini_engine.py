import google.generativeai as genai

class GeminiEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def stream(self, prompt):
        try:
            response = self.model.generate_content(
                prompt,
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"\n❌ Gemini Error: {str(e)}"
