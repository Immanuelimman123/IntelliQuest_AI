
from backend.models.model_router import generate_response


class AnalysisAgent:

    def analyze(self, question, research):

        if not research or not research.strip():
            return {
                "status": "no_context",
                "analysis": "No research information available."
            }

        prompt = f"""
You are IntelliQuest Analysis Agent.

Analyze the research information provided below.

Instructions:
1. Identify the information relevant to the question.
2. Extract important facts.
3. Remove repeated information.
4. Do not invent facts.
5. Preserve source filenames and page numbers.
6. Present findings clearly using bullet points.

User Question:
{question}

Research Information:
{research}

Provide your analysis:
"""

        try:

            analysis = generate_response(prompt)

            return {
                "status": "success",
                "analysis": analysis
            }

        except Exception as e:

            print("Analysis Agent Error:", str(e))

            return {
                "status": "failed",
                "analysis": None,
                "error": str(e)
            }
