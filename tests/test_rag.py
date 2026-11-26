
from backend.rag.answer_generator import RAGAnswerGenerator


def main():

    rag = RAGAnswerGenerator()

    questions = [
        "What is a list in Python?",
        "What is machine learning?",
        "What is inheritance in Java?",
        "Explain quantum computing."
    ]

    for question in questions:

        print("\n" + "=" * 55)
        print("Question:", question)

        result = rag.answer_question(
            question,
            top_k=3,
            min_similarity=0.40
        )

        print("\nStatus:", result["status"])
        print("\nAnswer:", result["answer"])

        print("\nSources:")

        for source in result["sources"]:
            print(
                source["filename"],
                "| Page:", source["page"],
                "| Similarity:", source["similarity"]
            )

        print("=" * 55)


if __name__ == "__main__":
    main()
