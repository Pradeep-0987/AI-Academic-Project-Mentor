
from dotenv import load_dotenv

from agents.scope_agent import ScopeAgent

load_dotenv()


def main():
    idea = input("Enter your project idea: ")

    try:
        result = ScopeAgent().generate_scope(idea)
        print("\n--- PROJECT SCOPE ---\n")
        print(result.model_dump_json(indent=2))
    except Exception as error:
        print(f"Scope generation failed: {error}")


if __name__ == "__main__":
    main()
