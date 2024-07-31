import google.generativeai as genai


class LLM:
    API_KEY = 'AIzaSyCjbWCrwJTJHPUHvgfrNWFBifKoA_T6GVk'
    # API_KEY = 'AIzaSyAoDS3qbAS2pH4EAKSRbogQm5bjbNaZqqw'
    # API_KEY = 'AIzaSyBtXP_PXADcoS5F5-EctxnMV8yZuaOoBuY' 
    genai.configure(api_key=API_KEY)

    def __init__(self):
        pass

    def getModel(self, config=None):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=config,
        )
        return model
