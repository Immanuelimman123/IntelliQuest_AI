
from backend.agents.research_agent import ResearchAgent
from backend.agents.analysis_agent import AnalysisAgent


def main():

    research_agent = ResearchAgent()
    analysis_agent = AnalysisAgent()

    question = "What is a list in Python?"

    print("\n========== MULTI-AGENT ANALYSIS ==========")

    research = research_agent.research(question)

    print("\nResearch Status:", research["status"])

    if research["status"] != "success":
        print(research["research"])
        return

    result = analysis_agent.analyze(
        question,
        research["research"]
    )

    print("\nAnalysis Status:", result["status"])

    print("\nAnalysis Results:")
    print(result["analysis"])

    print("\n==========================================")


if __name__ == "__main__":
    main()
