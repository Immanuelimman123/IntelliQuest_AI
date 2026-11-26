
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.vector_store import VectorStore


def main():

    print("\n========== INTELLIQUEST RETRIEVAL QUALITY TEST ==========")

    embedding_engine = EmbeddingEngine()
    vector_store = VectorStore()

    test_cases = [
        {
            "question": "What is a list in Python?",
            "expected": "relevant"
        },
        {
            "question": "Explain inheritance in Java.",
            "expected": "relevant"
        },
        {
            "question": "What is machine learning?",
            "expected": "relevant"
        },
        {
            "question": "Explain quantum computing.",
            "expected": "irrelevant"
        }
    ]

    passed = 0
    failed = 0

    for index, test in enumerate(test_cases, start=1):

        question = test["question"]
        expected = test["expected"]

        print(f"\nTest {index}: {question}")

        try:

            query_embedding = (
                embedding_engine.generate_query_embedding(question)
            )

            results = vector_store.search(
                query_embedding,
                top_k=3,
                min_similarity=0.40
            )

            if expected == "relevant":

                if results:

                    print("Expected: Relevant")
                    print("Actual: Relevant")
                    print("Top similarity:", round(
                        results[0]["similarity"], 4
                    ))

                    print("Sources:")

                    for result in results:
                        print(
                            "-", result["metadata"]["source"],
                            "| Page:", result["metadata"]["page"],
                            "| Similarity:",
                            round(result["similarity"], 4)
                        )

                    print("Result: PASS")
                    passed += 1

                else:

                    print("Expected: Relevant")
                    print("Actual: No relevant results")
                    print("Result: FAIL")
                    failed += 1

            else:

                if not results:

                    print("Expected: Irrelevant")
                    print("Actual: No relevant results")
                    print("Result: PASS")
                    passed += 1

                else:

                    print("Expected: Irrelevant")
                    print("Actual: Relevant results found")

                    for result in results:
                        print(
                            "-", result["metadata"]["source"],
                            "| Similarity:",
                            round(result["similarity"], 4)
                        )

                    print("Result: FAIL")
                    failed += 1

        except Exception as e:

            print("Test Error:", str(e))
            failed += 1

    total = passed + failed

    print("\n========== TEST SUMMARY ==========")
    print("Total Tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)

    if total:
        print("Pass Percentage:", f"{(passed / total) * 100:.2f}%")

    print("\n==================================")


if __name__ == "__main__":
    main()
