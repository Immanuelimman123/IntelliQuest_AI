
from pathlib import Path
import mimetypes

from backend.multimodal.image_qa import ImageQuestionAnswering


def main():

    print("\n========== INTELLIQUEST IMAGE QA ==========")

    image_path = Path(input("Enter image path: ").strip().strip('"'))

    if not image_path.exists():
        print("Error: Image file not found.")
        return

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
        print("Error: Use JPG, PNG or WEBP images.")
        return

    image_bytes = image_path.read_bytes()

    question = input("\nAsk a question about the image: ")

    try:
        image_qa = ImageQuestionAnswering()

        result = image_qa.answer_image_question(
            image_bytes,
            mime_type,
            question
        )

        print("\n========== AI RESPONSE ==========")
        print("Status:", result["status"])
        print("Question:", result["question"])
        print("Answer:", result["answer"])

    except Exception as e:
        print("\nImage QA Error:", str(e))

    print("\n=================================")


if __name__ == "__main__":
    main()
