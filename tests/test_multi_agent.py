
from backend.agents.research_agent import ResearchAgent
from backend.agents.analysis_agent import AnalysisAgent
from backend.agents.response_agent import ResponseAgent


def main():

    research_agent = ResearchAgent()
    analysis_agent = AnalysisAgent()
    response_agent = ResponseAgent()

    question = "What is a list in Python?"

    print("\n========== INTELLIQUEST MULTI-AGENT SYSTEM ==========")

    print("\n[1] RESEARCH AGENT")

    research = research_agent.research(question)

    print("Status:", research["status"])

    if research["status"] != "success":
        print(research["research"])
        return

    print("\n[2] ANALYSIS AGENT")

    analysis = analysis_agent.analyze(
        question,
        research["research"]
    )

    print("Status:", analysis["status"])

    if analysis["status"] != "success":
        print(analysis["error"])
        return

    print("\n[3] RESPONSE AGENT")

    response = response_agent.generate(
        question,
        analysis["analysis"],
        research["sources"]
    )

    print("Status:", response["status"])

    print("\n========== FINAL ANSWER ==========")
    print(response["answer"])

    print("\n========== SOURCES ==========")

    for source in response["sources"]:
        print(
            source["filename"],
            "| Page:", source["page"]
        )

    print("\n============================================")


if __name__ == "__main__":
    main()
