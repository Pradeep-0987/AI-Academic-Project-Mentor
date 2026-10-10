
from dotenv import load_dotenv

from agents.technology_agent import TechnologyAgent

load_dotenv()


def main():
    idea = input("Enter your project idea: ").strip()

    scope = input(
        "Paste a short scope description (or press Enter): "
    ).strip()

    try:
        agent = TechnologyAgent()
        result = agent.recommend(idea, scope)

        print("\n--- TECHNOLOGY RECOMMENDATIONS ---\n")
        print(result.model_dump_json(indent=2))

    except Exception as error:
        print(f"Technology recommendation failed: {error}")


if __name__ == "__main__":
    main()
