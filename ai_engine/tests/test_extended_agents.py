from schemas.blueprint_schema import ProjectBlueprint
from workflows.blueprint_graph import build_blueprint_graph
from workflows.quality_checks import validate_blueprint_consistency


def test_blueprint_schema_has_all_ten_agent_outputs():
    fields = set(ProjectBlueprint.model_fields)
    assert {
        "feasibility", "scope", "technology", "planning", "risk_assessment",
        "research", "dataset", "architecture", "testing", "documentation",
    }.issubset(fields)


def test_graph_compiles():
    graph = build_blueprint_graph()
    assert graph is not None


def test_quality_checker_flags_overlong_plan():
    report = validate_blueprint_consistency(
        {
            "project_idea": "demo",
            "feasibility": {},
            "scope": {},
            "technology": {},
            "planning": {
                "total_duration_days": 70,
                "phases": [{"duration_days": 70}],
            },
            "risk_assessment": {},
        },
        duration_weeks=8,
    )
    assert report["warning_count"] >= 1
