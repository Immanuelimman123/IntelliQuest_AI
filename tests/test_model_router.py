
from backend.models.model_router import generate_response

try:
    print("Testing IntelliQuest AI Engine...")

    response = generate_response(
        "Introduce yourself as the AI engine of IntelliQuest."
    )

    print("\nGemini Response:")
    print(response)

except Exception as e:
    print("\nModel Test Failed:", str(e))
