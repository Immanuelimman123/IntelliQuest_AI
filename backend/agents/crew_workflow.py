
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

from config import settings
from backend.agents.research_agent import ResearchAgent


@tool("Search IntelliQuest Knowledge Base")
def search_knowledge_base(question: str) -> str:
    """Search uploaded PDF documents and retrieve relevant information with source filenames and page numbers."""

    research_agent = ResearchAgent()

    result = research_agent.research(
        question,
        top_k=5,
        min_similarity=0.40
    )

    if result["status"] != "success":
        return "No sufficiently relevant information was found in the uploaded documents."

    return result["research"]


class IntelliQuestCrew:

    def __init__(self):

        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key is missing")

        self.llm = LLM(
            model=f"gemini/{settings.GEMINI_MODEL}",
            api_key=settings.GOOGLE_API_KEY
        )

        self.research_agent = Agent(
            role="Research Specialist",
            goal="Retrieve accurate information from the uploaded documents.",
            backstory="You are an expert document researcher who finds relevant evidence and preserves source references.",
            tools=[search_knowledge_base],
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        self.analysis_agent = Agent(
            role="Research Analyst",
            goal="Analyze retrieved information and identify important facts.",
            backstory="You are an analytical expert who organizes evidence without introducing unsupported facts.",
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        self.response_agent = Agent(
            role="Knowledge Assistant",
            goal="Generate a clear, accurate, source-supported final answer.",
            backstory="You are a professional AI assistant who explains technical concepts in simple language.",
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        self.research_task = Task(
            description="""
            Research the following question: {question}

            Use the Search IntelliQuest Knowledge Base tool.
            Retrieve relevant information from uploaded documents.
            Preserve exact source filenames and page numbers.
            Do not invent information.

            If no relevant information is found, clearly state that.
            """,
            expected_output="Relevant research findings with source filenames and page numbers, or a clear no-context message.",
            agent=self.research_agent
        )

        self.analysis_task = Task(
            description="""
            Analyze the research findings for this question: {question}

            Identify important facts and organize them logically.
            Remove repeated information.
            Preserve source filenames and page numbers.
            Do not introduce facts that are not present in the research.
            If the research contains no relevant information, state that.
            """,
            expected_output="A concise analysis based only on the retrieved research.",
            agent=self.analysis_agent,
            context=[self.research_task]
        )

        self.response_task = Task(
            description="""
            Prepare the final answer to: {question}

            Use the research and analysis provided.
            Answer clearly using simple professional language.
            Include relevant source filenames and page numbers.
            Do not invent facts or sources.
            If no relevant document information was found, say so clearly.
            """,
            expected_output="A final answer with relevant document citations.",
            agent=self.response_agent,
            context=[self.research_task, self.analysis_task]
        )

        self.crew = Crew(
            agents=[
                self.research_agent,
                self.analysis_agent,
                self.response_agent
            ],
            tasks=[
                self.research_task,
                self.analysis_task,
                self.response_task
            ],
            process=Process.sequential,
            verbose=False
        )

    def ask(self, question):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        result = self.crew.kickoff(
            inputs={"question": question.strip()}
        )

        return {
            "status": "success",
            "question": question.strip(),
            "answer": str(result)
        }
