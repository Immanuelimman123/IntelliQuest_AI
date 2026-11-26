
from backend.models.model_router import generate_response


class ResponseAgent:

    def generate(self, question, analysis, sources):

        if not analysis or not analysis.strip():
            return {
                "status": "failed",
                "answer": "No analysis information is available."
            }

        source_text = "\n".join(
            [
                f"- {source['filename']}, Page {source['page']}"
                for source in sources
            ]
        )

        prompt = f"""
You are IntelliQuest Response Agent.

Create a clear and professional answer using the analysis.

Instructions:
1. Answer the user's question directly.
2. Use simple and understandable language.
3. Organize information with bullet points when appropriate.
4. Do not add unsupported information.
5. Include the provided document sources.

Question:
{question}

Analysis:
{analysis}

Available Sources:
{source_text}

Final Answer:
"""

        try:

            answer = generate_response(prompt)

            return {
                "status": "success",
                "answer": answer,
                "sources": sources
            }

        except Exception as e:

            print("Response Agent Error:", str(e))

            return {
                "status": "failed",
                "answer": None,
                "error": str(e)
            }
