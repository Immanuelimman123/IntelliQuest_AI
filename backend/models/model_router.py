
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings


def get_model():
    provider = settings.MODEL_PROVIDER.lower()

    if provider == "gemini":
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key is missing")

        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            max_retries=2
        )

    raise ValueError(f"Unsupported provider: {provider}")


def generate_response(prompt):
    model = get_model()

    for attempt in range(3):
        try:
            response = model.invoke(prompt)
            content = response.content

            if isinstance(content, str):
                return content

            if isinstance(content, list):
                text_parts = [
                    block["text"]
                    for block in content
                    if isinstance(block, dict)
                    and block.get("type") == "text"
                ]

                return "\n".join(text_parts).strip()

            return str(content)

        except Exception as e:
            error = str(e)

            if "503" not in error and "UNAVAILABLE" not in error:
                raise

            if attempt == 2:
                raise

            wait_time = 2 ** (attempt + 1)
            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
