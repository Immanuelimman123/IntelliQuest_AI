
from google import genai
from config import settings


def main():
    print("Testing Gemini 3.5 Flash-Lite...")

    if not settings.GOOGLE_API_KEY:
        print("API key not loaded from .env")
        return

    try:
        client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Reply with only: IntelliQuest is working!"
        )

        print("\nGemini Response:")
        print(response.text)

    except Exception as e:
        print("\nGemini Test Failed:")
        print(type(e).__name__)
        print(str(e))


if __name__ == "__main__":
    main()
