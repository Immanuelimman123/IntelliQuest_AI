
import json
import re

from backend.models.model_router import generate_response
from backend.evaluation.evaluation_metrics import EvaluationMetrics


class ResponseEvaluator:

    def __init__(self):
        self.metrics = EvaluationMetrics()

    def evaluate_faithfulness(self, answer, context):

        prompt = f"""
You are an AI response evaluation expert.

Evaluate whether the answer is supported by the given context.

Context:
{context}

Generated Answer:
{answer}

Evaluation rules:
1. Check every factual claim in the answer.
2. Identify claims that are unsupported by the context.
3. Give a faithfulness score between 0 and 1.
4. A score of 1 means all claims are supported.
5. A score of 0 means the answer is completely unsupported.
6. Do not use outside knowledge.

Return ONLY valid JSON in this format:

{{
    "faithfulness_score": 0.0,
    "explanation": "Brief explanation",
    "unsupported_claims": []
}}
"""

        response = generate_response(prompt)

        try:
            cleaned_response = re.sub(
                r"```(?:json)?|```",
                "",
                response
            ).strip()

            result = json.loads(cleaned_response)

            score = float(result["faithfulness_score"])

            if not 0 <= score <= 1:
                raise ValueError("Invalid faithfulness score")

            return {
                "faithfulness_score": round(score, 4),
                "explanation": str(result.get("explanation", "")),
                "unsupported_claims": result.get(
                    "unsupported_claims", []
                )
            }

        except (ValueError, TypeError, KeyError, json.JSONDecodeError):

            raise ValueError(
                "Unable to parse the faithfulness evaluation response"
            )

    def evaluate_response(self, question, answer, retrieved_chunks):

        if not retrieved_chunks:
            raise ValueError("No retrieved context available")

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
            if chunk.get("text")
        )

        if not context.strip():
            raise ValueError("Retrieved context is empty")

        semantic_metrics = self.metrics.evaluate_answer(
            question,
            answer,
            retrieved_chunks
        )

        faithfulness = self.evaluate_faithfulness(
            answer,
            context
        )

        return {
            "status": "success",
            "question": question,
            "semantic_metrics": semantic_metrics,
            "faithfulness": faithfulness
        }
