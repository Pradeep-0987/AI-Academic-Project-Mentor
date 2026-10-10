
from dotenv import load_dotenv

from agents.risk_agent import RiskAgent

load_dotenv()


def main():
    idea = input("Enter your project idea: ").strip()

    scope = input(
        "Enter a short project scope (or press Enter): "
    ).strip()

    try:
        result = RiskAgent().assess(
            project_idea=idea,
            project_scope=scope,
            duration_weeks=8,
        )

        print("\n--- PROJECT RISK ASSESSMENT ---\n")
        print(result.model_dump_json(indent=2))

    except Exception as error:
        print(f"Risk assessment failed: {error}")


if __name__ == "__main__":
    main()
