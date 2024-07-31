import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLM:
    API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=API_KEY)

    def __init__(self):
        pass

    def getModel(self, config=None):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=config,
        )
        return model
