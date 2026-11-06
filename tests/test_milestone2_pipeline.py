"""Tests validating Milestone 2:
1. Feasibility Analysis Agent and Scope Definition Agent.
2. Technology Stack Recommendation Agent with reasoning output.
3. Milestone and Timeline Planning Agent — generates week-wise execution plan.
4. End-to-end pipeline validation using sample student project ideas.
"""
import pytest
from ai_engine.agents.feasibility_agent import analyse_feasibility
from ai_engine.agents.scope_agent import define_scope
from ai_engine.agents.technology_agent import recommend_technology
from ai_engine.agents.planning_agent import create_plan
from ai_engine.agents.risk_agent import assess_risks
from ai_engine.agents.heuristic_fallback import fallback_planning
from ai_engine.agents import planning_agent
from ai_engine.schemas import PlannedPhase, PlanningResult, WeeklyMilestone
from ai_engine.workflows.blueprint_graph import generate_blueprint
from ai_engine.workflows.quality_checks import validate_blueprint_consistency


def test_feasibility_analysis_agent():
    idea = "Smart waste segregation using computer vision and robotic arm"
    result = analyse_feasibility(idea, duration_weeks=8, team_size=4, skills=["Python", "OpenCV"])

    assert result.feasibility in {"High", "Medium", "Low"}
    assert result.complexity in {"Beginner", "Intermediate", "Advanced"}
    assert len(result.project_title) > 0
    assert len(result.problem_statement) > 0
    assert len(result.required_skills) > 0
    assert len(result.required_resources) > 0
    assert len(result.potential_challenges) > 0
    assert len(result.recommendations) > 0
    assert len(result.assumptions) > 0
    assert len(result.reasoning) > 0
    assert result.economic_feasibility in {"High", "Medium", "Low"}
    assert result.operational_feasibility in {"High", "Medium", "Low"}


def test_feasibility_validation_errors():
    with pytest.raises(ValueError, match="meaningful project idea"):
        analyse_feasibility("  ", duration_weeks=8, team_size=4)

    with pytest.raises(ValueError, match="duration_weeks must be 1..52"):
        analyse_feasibility("Smart traffic light system", duration_weeks=0, team_size=4)

    with pytest.raises(ValueError, match="team_size must be 1..20"):
        analyse_feasibility("Smart traffic light system", duration_weeks=8, team_size=25)


def test_scope_definition_agent():
    idea = "Healthcare appointment scheduling and triage AI assistant"
    feasibility = {
        "project_title": "AI Healthcare Triage Assistant",
        "feasibility": "High",
        "complexity": "Intermediate",
    }
    result = define_scope(idea, feasibility, duration_weeks=10, team_size=3)

    assert len(result.project_title) > 0
    assert len(result.project_objective) > 0
    assert len(result.proposed_solution) > 0
    assert len(result.target_users) > 0
    assert len(result.functional_requirements) > 0
    assert len(result.non_functional_requirements) > 0
    assert len(result.mvp_features) > 0
    assert len(result.out_of_scope) > 0
    assert len(result.deliverables) > 0
    assert len(result.success_criteria) > 0


def test_technology_recommendation_agent_with_reasoning():
    idea = "Real-time stock market sentiment analysis using NLP"
    feasibility = {"feasibility": "High", "complexity": "Intermediate"}
    scope = {"mvp_features": ["Sentiment scoring", "Dashboard", "Alerts"]}

    result = recommend_technology(idea, feasibility, scope, skills=["Python", "React"])

    assert len(result.frontend) > 0
    assert len(result.backend) > 0
    assert len(result.database) > 0
    assert len(result.ai_ml) > 0
    assert len(result.deployment) > 0
    assert len(result.development_tools) > 0
    assert len(result.alternatives) > 0
    assert len(result.rationale) > 0
    assert len(result.limitations) > 0
    # Requirement 2: Reasoning output
    reasoning_text = result.reasoning or result.rationale
    assert len(reasoning_text) > 20, "Technology agent must provide detailed reasoning output"


def test_planning_agent_generates_week_wise_plan():
    idea = "IoT based soil moisture monitoring and automated irrigation"
    duration = 8
    team_size = 4
    scope = {"deliverables": ["Hardware prototype", "Web dashboard", "Final report"]}
    tech = {"backend": ["FastAPI"], "frontend": ["React"]}

    result = create_plan(idea, duration_weeks=duration, team_size=team_size, scope=scope, technology=tech)

    assert result.total_duration_weeks == duration
    assert len(result.phases) > 0

    # Requirement 3: Generates week-wise execution plan
    assert len(result.weekly_milestones) == duration, f"Expected {duration} week milestones, got {len(result.weekly_milestones)}"

    week_numbers = [m.week_number for m in result.weekly_milestones]
    assert week_numbers == list(range(1, duration + 1)), "Milestones must cover each week sequentially"

    for milestone in result.weekly_milestones:
        assert len(milestone.milestone_title) > 0
        assert len(milestone.tasks) > 0
        assert len(milestone.deliverables) > 0


def test_planning_agent_custom_duration():
    idea = "Blockchain based certificate verification platform"
    duration = 12
    result = create_plan(idea, duration_weeks=duration, team_size=3, scope={}, technology={})

    assert result.total_duration_weeks == duration
    assert len(result.weekly_milestones) == duration


@pytest.mark.parametrize("duration_weeks", range(1, 53))
def test_fallback_planning_phases_fit_requested_duration(duration_weeks):
    plan = fallback_planning(
        "Smart campus energy monitoring",
        duration_weeks=duration_weeks,
        team_size=None,
        scope={},
        technology={},
    ).model_dump(mode="json")
    report = validate_blueprint_consistency(
        {
            "feasibility": {"feasibility": "Medium"},
            "scope": {"project_objective": ["Build a prototype"]},
            "technology": {"backend": ["FastAPI"]},
            "planning": plan,
            "risk": {"risks": []},
        },
        duration_weeks,
    )

    assert report["valid"], report["errors"]
    assert [item["week_number"] for item in plan["weekly_milestones"]] == list(range(1, duration_weeks + 1))
    assert len(plan["phases"]) == min(4, duration_weeks)


def test_planning_agent_normalizes_duplicate_and_missing_weeks(monkeypatch):
    def milestone(week):
        return WeeklyMilestone(
            week_number=week,
            milestone_title=f"Week {week}",
            objectives=["Objective"],
            tasks=[f"Task {week}"],
            deliverables=[f"Deliverable {week}"],
        )

    phase = PlannedPhase(
        phase_name="Build",
        start_week=1,
        duration_weeks=3,
        tasks=["Implement"],
        deliverables=["Prototype"],
        dependencies=[],
    )
    generated = PlanningResult(
        total_duration_weeks=3,
        phases=[phase],
        weekly_milestones=[milestone(1), milestone(1), milestone(9)],
    )
    fallback = PlanningResult(
        total_duration_weeks=3,
        phases=[phase],
        weekly_milestones=[milestone(week) for week in range(1, 4)],
    )
    monkeypatch.setattr(planning_agent, "generate_structured", lambda *_args: generated)
    monkeypatch.setattr(planning_agent, "fallback_planning", lambda *_args: fallback)

    plan = planning_agent.create_plan("Test project", 3, None, {}, {})
    assert [item.week_number for item in plan.weekly_milestones] == [1, 2, 3]


# Requirement 4: Validate end-to-end pipeline using sample student project ideas
@pytest.mark.parametrize(
    "idea,duration,team,skills",
    [
        (
            "Automated Crop Disease Detection using UAV Imagery and Deep Learning",
            8,
            4,
            ["Python", "PyTorch", "OpenCV"],
        ),
        (
            "AI-Powered Medical Prescription Handwriting Decryption and Drug Interaction Checker",
            10,
            3,
            ["Python", "FastAPI", "OCR"],
        ),
        (
            "Real-time Financial Fraud and Money Laundering Detection Platform",
            6,
            2,
            ["Python", "Pandas", "Machine Learning"],
        ),
        (
            "IoT-enabled Smart Campus Energy Monitoring and Predictive HVAC Optimization",
            8,
            4,
            ["C++", "Python", "MQTT", "React"],
        ),
    ],
)
def test_end_to_end_pipeline_validation(idea, duration, team, skills):
    blueprint = generate_blueprint(
        project_idea=idea,
        duration_weeks=duration,
        team_size=team,
        skills=skills,
    )

    # 1. Verify all sections are present
    for sec in ["feasibility", "scope", "technology", "planning", "risk", "quality_report"]:
        assert sec in blueprint, f"Missing section '{sec}' in generated blueprint"

    # 2. Feasibility verification
    feasibility = blueprint["feasibility"]
    assert feasibility["feasibility"] in {"High", "Medium", "Low"}
    assert len(feasibility["reasoning"]) > 0

    # 3. Scope verification
    scope = blueprint["scope"]
    assert len(scope["mvp_features"]) > 0
    assert len(scope["deliverables"]) > 0

    # 4. Tech stack with reasoning
    tech = blueprint["technology"]
    assert len(tech["backend"]) > 0
    assert len(tech["frontend"]) > 0
    assert len(tech.get("reasoning") or tech.get("rationale")) > 0

    # 5. Planning with week-wise plan
    plan = blueprint["planning"]
    assert plan["total_duration_weeks"] == duration
    assert len(plan["phases"]) > 0
    assert len(plan["weekly_milestones"]) == duration

    # 6. Quality report validation
    quality = blueprint["quality_report"]
    assert quality["valid"] is True, f"Blueprint quality checks failed: {quality.get('errors')}"
