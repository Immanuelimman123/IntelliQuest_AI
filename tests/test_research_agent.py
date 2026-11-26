
from backend.agents.research_agent import ResearchAgent


def main():

    agent = ResearchAgent()

    question = "What is a list in Python?"

    print("\n========== RESEARCH AGENT ==========")
    print("\nQuestion:", question)

    result = agent.research(question)

    print("\nStatus:", result["status"])

    print("\nResearch Results:")
    print(result["research"])

    print("\nSources:")

    for source in result["sources"]:
        print(source)

    print("\n====================================")


if __name__ == "__main__":
    main()
