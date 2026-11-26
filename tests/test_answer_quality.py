
from backend.rag.answer_generator import RAGAnswerGenerator


def main():

    print("\n========== ANSWER QUALITY TEST ==========")

    rag = RAGAnswerGenerator()

    test_cases = [
        {
            "question": "What is a list in Python?",
            "expected": "success"
        },
        {
            "question": "What is inheritance in Java?",
            "expected": "success"
        },
        {
            "question": "What is quantum computing?",
            "expected": "no_context"
        }
    ]

    passed = 0
    failed = 0

    for index, test in enumerate(test_cases, start=1):

        question = test["question"]

        print(f"\nTest {index}: {question}")

        try:

            result = rag.answer_question(
                question,
                top_k=3,
                min_similarity=0.40
            )

            actual = result["status"]
            expected = test["expected"]

            print("Expected:", expected)
            print("Actual:", actual)

            if actual == expected:
                print("Result: PASS")
                passed += 1
            else:
                print("Result: FAIL")
                failed += 1

            if actual == "success":
                print("\nGenerated Answer:")
                print(result["answer"])

                print("\nSources:")

                for source in result["sources"]:
                    print(
                        source["filename"],
                        "| Page:",
                        source["page"]
                    )

            elif actual == "no_context":
                print("Response:", result["answer"])

        except Exception as e:

            print("Test Error:", str(e))
            failed += 1

    total = passed + failed

    print("\n========== TEST SUMMARY ==========")
    print("Total Tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)

    if total:
        print(
            "Pass Percentage:",
            f"{passed / total * 100:.2f}%"
        )

    print("\n==================================")


if __name__ == "__main__":
    main()
