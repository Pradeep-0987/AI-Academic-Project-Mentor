import json
from pathlib import Path
from ai_engine.workflows.blueprint_graph import generate_blueprint

def main():
    idea = input("Project idea: ").strip()
    if not idea:
        raise SystemExit("Project idea cannot be empty.")
    duration = int(input("Duration in weeks [8]: ").strip() or "8")
    team_size = int(input("Team size [6]: ").strip() or "6")
    skills = input("Skills, comma separated (optional): ").strip()
    result = generate_blueprint(idea, duration, team_size,
        [x.strip() for x in skills.split(",") if x.strip()])
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "blueprint.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved blueprint to {path.resolve()}")

if __name__ == "__main__":
    main()
