import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    MODEL_PROVIDER=os.getenv("MODEL_PROVIDER","gemini")
    GEMINI_MODEL=os.getenv("GEMINI_MODEL","gemini-2.5-flash")

settings=Settings()