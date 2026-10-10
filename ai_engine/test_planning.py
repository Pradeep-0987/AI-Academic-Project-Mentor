
from dotenv import load_dotenv

from agents.planning_agent import PlanningAgent

load_dotenv()


def main():
    idea = input("Enter your project idea: ").strip()

    try:
        plan = PlanningAgent().create_plan(
            project_idea=idea,
            duration_weeks=8,
            team_size=6,
        )

        print("\n--- PROJECT IMPLEMENTATION PLAN ---\n")
        print(plan.model_dump_json(indent=2))

    except Exception as error:
        print(f"Planning failed: {error}")


if __name__ == "__main__":
    main()
