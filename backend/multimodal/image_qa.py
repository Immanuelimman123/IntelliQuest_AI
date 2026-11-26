
import base64

from langchain_core.messages import HumanMessage
from backend.models.model_router import get_model


class ImageQuestionAnswering:

    def __init__(self):
        self.model = get_model()

    def answer_image_question(self, image_bytes, mime_type, question):

        if not image_bytes:
            raise ValueError("Please provide an image")

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise ValueError("Unsupported image format")

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"""
You are IntelliQuest, an intelligent visual AI assistant.

Analyze the uploaded image carefully and answer the user's question.

Instructions:
1. Use only information visible in the image.
2. Explain clearly and accurately.
3. Do not invent missing visual details.
4. If something is unclear, mention it.
5. Use simple, professional language.

User Question:
{question}
"""
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }
                }
            ]
        )

        response = self.model.invoke([message])

        content = response.content

        if isinstance(content, list):

            answer = "\n".join(
                block["text"]
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
            )

        else:
            answer = str(content)

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }
