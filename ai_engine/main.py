
from dotenv import load_dotenv

from agents.feasibility_agent import FeasibilityAgent

load_dotenv()


def main():
    idea = input(
        "\nEnter a student project idea: "
    ).strip()

    try:
        agent = FeasibilityAgent()
        result = agent.evaluate(idea)

        print("\n--- PROJECT FEASIBILITY REPORT ---\n")
        print(result.model_dump_json(indent=2))

    except Exception as error:
        print(f"\nFeasibility assessment failed: {error}")


if __name__ == "__main__":
    main()
