
from backend.agents.crew_workflow import IntelliQuestCrew


def main():

    print("\n========== INTELLIQUEST CREWAI SYSTEM ==========")

    crew = IntelliQuestCrew()

    question = "What is a list in Python?"

    print("\nQuestion:", question)
    print("\nExecuting CrewAI agents...")

    result = crew.ask(question)

    print("\nStatus:", result["status"])

    print("\n========== FINAL ANSWER ==========")
    print(result["answer"])

    print("\n==================================")


if __name__ == "__main__":
    main()
