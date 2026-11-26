
from backend.rag.answer_generator import RAGAnswerGenerator
from backend.evaluation.response_evaluator import ResponseEvaluator


def main():

    print("\n========== INTELLIQUEST RESPONSE EVALUATION ==========")

    question = "What is a list in Python?"

    print("\nQuestion:", question)

    try:

        rag = RAGAnswerGenerator()

        result = rag.answer_question(
            question,
            top_k=3,
            min_similarity=0.40
        )

        if result["status"] != "success":

            print("\nRAG Error:", result["status"])
            print(result.get("answer", result.get("message")))
            return

        print("\n========== GENERATED ANSWER ==========")
        print(result["answer"])

        evaluator = ResponseEvaluator()

        evaluation = evaluator.evaluate_response(
            question,
            result["answer"],
            result["retrieved_chunks"]
        )

        print("\n========== EVALUATION RESULTS ==========")

        print("\nSemantic Metrics:")

        for metric, score in evaluation["semantic_metrics"].items():
            print(f"{metric}: {score}")

        print("\nFaithfulness:")
        print(
            "Score:",
            evaluation["faithfulness"]["faithfulness_score"]
        )

        print(
            "Explanation:",
            evaluation["faithfulness"]["explanation"]
        )

        print(
            "Unsupported Claims:",
            evaluation["faithfulness"]["unsupported_claims"]
        )

        print("\nEvaluation Status:", evaluation["status"])

    except Exception as e:

        print("\nEvaluation Error:", str(e))

    print("\n======================================================")


if __name__ == "__main__":
    main()
