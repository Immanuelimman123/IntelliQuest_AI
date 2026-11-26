
from backend.orchestration.rag_graph import RAGWorkflow


def main():

    workflow = RAGWorkflow()

    questions = [
        "What is a list in Python?",
        "What is machine learning?",
        "Explain quantum computing."
    ]

    for question in questions:

        print("\n" + "=" * 55)
        print("Question:", question)

        result = workflow.ask(
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
