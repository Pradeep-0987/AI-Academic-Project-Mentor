from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END

from ai_engine.agents.feasibility_agent import analyse_feasibility
from ai_engine.agents.scope_agent import define_scope
from ai_engine.agents.technology_agent import recommend_technology
from ai_engine.agents.planning_agent import create_plan
from ai_engine.agents.risk_agent import assess_risks
from ai_engine.workflows.quality_checks import validate_blueprint_consistency

class BlueprintState(TypedDict, total=False):
    project_idea: str
    duration_weeks: int
    team_size: int | None
    skills: list[str]
    feasibility: dict
    scope: dict
    technology: dict
    planning: dict
    risk: dict
    quality_report: dict

def _feasibility(s):
    return {"feasibility": analyse_feasibility(s["project_idea"], s["duration_weeks"],
            s["team_size"], s.get("skills", [])).model_dump(mode="json")}

def _scope(s):
    return {"scope": define_scope(s["project_idea"], s["feasibility"],
            s["duration_weeks"], s["team_size"]).model_dump(mode="json")}

def _technology(s):
    return {"technology": recommend_technology(s["project_idea"], s["feasibility"],
            s["scope"], s.get("skills", [])).model_dump(mode="json")}

def _planning(s):
    return {"planning": create_plan(s["project_idea"], s["duration_weeks"], s["team_size"],
            s["scope"], s["technology"]).model_dump(mode="json")}

def _risk(s):
    return {"risk": assess_risks(s["project_idea"], s["feasibility"], s["scope"],
            s["technology"], s["planning"]).model_dump(mode="json")}

def _quality(s):
    report = validate_blueprint_consistency(
        {k: s.get(k) for k in ("feasibility", "scope", "technology", "planning", "risk")},
        s["duration_weeks"])
    if not report["valid"]:
        raise ValueError("Blueprint quality validation failed: " + "; ".join(report["errors"]))
    return {"quality_report": report}

def build_blueprint_graph():
    graph = StateGraph(BlueprintState)
    for name, fn in [("feasibility", _feasibility), ("scope", _scope),
                     ("technology", _technology), ("planning", _planning),
                     ("risk", _risk), ("quality", _quality)]:
        graph.add_node(name, fn)
    graph.add_edge(START, "feasibility")
    graph.add_edge("feasibility", "scope")
    graph.add_edge("scope", "technology")
    graph.add_edge("technology", "planning")
    graph.add_edge("planning", "risk")
    graph.add_edge("risk", "quality")
    graph.add_edge("quality", END)
    return graph.compile()

def generate_blueprint(project_idea: str, duration_weeks: int = 8,
                       team_size: int | None = 6, skills: list[str] | None = None) -> dict[str, Any]:
    if not project_idea or len(project_idea.strip()) < 3:
        raise ValueError("project_idea must contain at least 3 characters.")
    if not 1 <= duration_weeks <= 52:
        raise ValueError("duration_weeks must be 1..52.")
    if team_size is not None and not 1 <= team_size <= 20:
        raise ValueError("team_size must be 1..20.")
    result = build_blueprint_graph().invoke({"project_idea": project_idea.strip(),
        "duration_weeks": duration_weeks, "team_size": team_size, "skills": skills or []})
    return {"project_idea": project_idea.strip(), "duration_weeks": duration_weeks,
        "team_size": team_size, **{k: result[k] for k in
        ("feasibility", "scope", "technology", "planning", "risk", "quality_report")}}
