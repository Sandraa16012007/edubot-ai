import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def ask(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

# global reference
gemini = None

def init_gemini(api_key):
    global gemini
    gemini = GeminiClient(api_key)

def ask_gemini(prompt):
    global gemini
    if gemini is None:
        raise RuntimeError("Gemini not initialized. Call init_gemini(api_key) first.")
    return gemini.ask(prompt)
