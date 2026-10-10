
from dotenv import load_dotenv

from workflows.blueprint_graph import generate_blueprint


def main():
    load_dotenv()

    idea = input("Enter your project idea: ").strip()

    try:
        blueprint = generate_blueprint(
            project_idea=idea,
            duration_weeks=8,
            team_size=6,
        )

        output_path = "project_blueprint.json"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(blueprint.model_dump_json(indent=2))

        print("\n--- UNIFIED PROJECT BLUEPRINT ---\n")
        print(blueprint.model_dump_json(indent=2))
        print(f"\nBlueprint saved to: {output_path}")

    except Exception as error:
        print(f"\nBlueprint generation failed: {error}")
        print(
            "Check the error and retry if the Gemini API "
            "is temporarily unavailable."
        )


if __name__ == "__main__":
    main()
