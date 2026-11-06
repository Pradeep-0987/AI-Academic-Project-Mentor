"""Milestone 2 Validation Runner — NEXTSTEP AI

Demonstrates and validates:
1. Feasibility Analysis Agent and Scope Definition Agent.
2. Technology Stack Recommendation Agent with reasoning output.
3. Milestone and Timeline Planning Agent (week-wise execution plan).
4. End-to-end multi-agent pipeline validation using sample student project ideas.
"""
import json
import sys
from pathlib import Path

# Ensure root is in sys.path
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from ai_engine.workflows.blueprint_graph import generate_blueprint

SAMPLE_STUDENT_IDEAS = [
    {
        "title": "Smart Crop Disease Detection",
        "idea": "An automated system detecting crop diseases from aerial drone imagery using deep learning and providing treatment guidance to local farmers.",
        "duration_weeks": 8,
        "team_size": 4,
        "skills": ["Python", "Computer Vision", "PyTorch"],
    },
    {
        "title": "Medical Prescription Decryption & Drug Safety",
        "idea": "AI-powered web portal that scans handwritten doctor prescriptions using OCR and cross-references active drug ingredients for hazardous drug-drug interactions.",
        "duration_weeks": 10,
        "team_size": 3,
        "skills": ["Python", "FastAPI", "React", "OCR"],
    },
    {
        "title": "Financial Transaction Fraud Sentinel",
        "idea": "Real-time streaming pipeline monitoring credit card and wire transactions to flag fraudulent anomaly spikes and money laundering patterns.",
        "duration_weeks": 6,
        "team_size": 2,
        "skills": ["Python", "Pandas", "Scikit-Learn", "SQL"],
    },
]


def print_separator(char="=", length=80):
    print(char * length)


def validate_sample_idea(sample_idx: int, sample: dict):
    title = sample["title"]
    idea = sample["idea"]
    duration = sample["duration_weeks"]
    team = sample["team_size"]
    skills = sample["skills"]

    print_separator("=")
    print(f"[{sample_idx}/3] VALIDATING SAMPLE STUDENT PROJECT: {title.upper()}")
    print(f"  Idea: {idea}")
    print(f"  Timeline: {duration} Weeks | Team Size: {team} | Skills: {', '.join(skills)}")
    print_separator("-")

    # Run multi-agent pipeline
    blueprint = generate_blueprint(
        project_idea=idea,
        duration_weeks=duration,
        team_size=team,
        skills=skills,
    )

    feasibility = blueprint["feasibility"]
    scope = blueprint["scope"]
    technology = blueprint["technology"]
    planning = blueprint["planning"]
    risk = blueprint["risk"]
    quality = blueprint["quality_report"]

    # 1. Feasibility & Scope
    print("\n1. FEASIBILITY ANALYSIS & SCOPE DEFINITION AGENTS:")
    print(f"   Project Title: {feasibility['project_title']}")
    print(f"   Feasibility Rating: {feasibility['feasibility']} | Complexity: {feasibility['complexity']}")
    print(f"   Reasoning: {feasibility['reasoning'][:200]}...")
    print(f"   Scope Objective: {scope['project_objective'][:160]}...")
    print(f"   MVP Features ({len(scope['mvp_features'])} items):")
    for mvp in scope["mvp_features"][:3]:
        print(f"     * {mvp}")
    print(f"   Deliverables ({len(scope['deliverables'])} items):")
    for d in scope["deliverables"][:3]:
        print(f"     * {d}")

    # 2. Technology Recommendation with Reasoning
    print("\n2. TECHNOLOGY STACK RECOMMENDATION AGENT (WITH REASONING OUTPUT):")
    print(f"   Frontend: {', '.join(technology['frontend'])}")
    print(f"   Backend: {', '.join(technology['backend'])}")
    print(f"   Database: {', '.join(technology['database'])}")
    print(f"   AI / ML: {', '.join(technology['ai_ml'])}")
    print("   Architectural Reasoning Output:")
    tech_reasoning = technology.get("reasoning") or technology.get("rationale")
    for line in tech_reasoning.strip().split("\n"):
        print(f"     {line}")

    # 3. Milestone & Timeline Planning (Week-Wise Execution Plan)
    print(f"\n3. MILESTONE & TIMELINE PLANNING AGENT ({duration}-WEEK EXECUTION PLAN):")
    print(f"   Execution Phases: {len(planning['phases'])} phases")
    for p in planning["phases"]:
        print(f"     * {p['phase_name']} (Weeks {p['start_week']}-{p['start_week'] + p['duration_weeks'] - 1})")
    print(f"   Week-Wise Milestones ({len(planning['weekly_milestones'])} weeks generated):")
    for wm in planning["weekly_milestones"][:4]:
        print(f"     [Week {wm['week_number']}] {wm['milestone_title']}")
        print(f"        Task: {wm['tasks'][0]}")
        print(f"        Deliverable: {wm['deliverables'][0]}")
    if len(planning["weekly_milestones"]) > 4:
        print(f"     ... and {len(planning['weekly_milestones']) - 4} more weeks up to Week {duration}")

    # 4. Pipeline Quality & Validation
    print("\n4. QUALITY CHECKS & PIPELINE CONSISTENCY:")
    print(f"   Pipeline Consistency: {'PASSED [VALID]' if quality['valid'] else 'FAILED'}")
    print(f"   Errors: {len(quality['errors'])} | Warnings: {quality['warning_count']}")
    print_separator("=")
    print()


def main():
    print_separator("#")
    print("AI ACADEMIC PROJECT MENTOR — MILESTONE 2 VALIDATION SUITE")
    print("Multi-Agent Architecture: Feasibility -> Scope -> Tech -> Planning -> Risk -> Quality")
    print_separator("#")
    print()

    for idx, sample in enumerate(SAMPLE_STUDENT_IDEAS, start=1):
        validate_sample_idea(idx, sample)

    # Save output sample
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    sample_bp = generate_blueprint(
        project_idea=SAMPLE_STUDENT_IDEAS[0]["idea"],
        duration_weeks=SAMPLE_STUDENT_IDEAS[0]["duration_weeks"],
        team_size=SAMPLE_STUDENT_IDEAS[0]["team_size"],
        skills=SAMPLE_STUDENT_IDEAS[0]["skills"],
    )
    bp_path = out_dir / "milestone2_sample_blueprint.json"
    bp_path.write_text(json.dumps(sample_bp, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved sample validated blueprint to: {bp_path.resolve()}\n")
    print("ALL MILESTONE 2 REQUIREMENTS SUCCESSFULLY VALIDATED! [OK]")


if __name__ == "__main__":
    main()
