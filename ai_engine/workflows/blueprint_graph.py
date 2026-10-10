
from langgraph.graph import StateGraph, START, END

from agents.feasibility_agent import FeasibilityAgent
from agents.scope_agent import ScopeAgent
from agents.technology_agent import TechnologyAgent
from agents.planning_agent import PlanningAgent
from agents.risk_agent import RiskAgent

from schemas.blueprint_schema import ProjectBlueprint
from workflows.state import BlueprintState


def feasibility_node(state: BlueprintState) -> dict:
    result = FeasibilityAgent().evaluate(state["project_idea"])
    return {"feasibility": result.model_dump()}


def scope_node(state: BlueprintState) -> dict:
    result = ScopeAgent().generate_scope(state["project_idea"])
    return {"scope": result.model_dump()}


def technology_node(state: BlueprintState) -> dict:
    scope_json = str(state["scope"])

    result = TechnologyAgent().recommend(
        project_idea=state["project_idea"],
        project_scope=scope_json,
    )
    return {"technology": result.model_dump()}


def planning_node(state: BlueprintState) -> dict:
    result = PlanningAgent().create_plan(
        project_idea=state["project_idea"],
        duration_weeks=state.get("duration_weeks", 8),
        team_size=state.get("team_size", 6),
    )
    return {"planning": result.model_dump()}


def risk_node(state: BlueprintState) -> dict:
    result = RiskAgent().assess(
        project_idea=state["project_idea"],
        project_scope=str(state["scope"]),
        duration_weeks=state.get("duration_weeks", 8),
    )
    return {"risk_assessment": result.model_dump()}


def build_blueprint_graph():
    graph = StateGraph(BlueprintState)

    graph.add_node("feasibility", feasibility_node)
    graph.add_node("scope", scope_node)
    graph.add_node("technology", technology_node)
    graph.add_node("planning", planning_node)
    graph.add_node("risk_assessment", risk_node)

    graph.add_edge(START, "feasibility")
    graph.add_edge("feasibility", "scope")
    graph.add_edge("scope", "technology")
    graph.add_edge("technology", "planning")
    graph.add_edge("planning", "risk_assessment")
    graph.add_edge("risk_assessment", END)

    return graph.compile()


def generate_blueprint(
    project_idea: str,
    duration_weeks: int = 8,
    team_size: int = 6,
) -> ProjectBlueprint:
    if not project_idea.strip():
        raise ValueError("Project idea cannot be empty.")

    workflow = build_blueprint_graph()

    result = workflow.invoke({
        "project_idea": project_idea.strip(),
        "duration_weeks": duration_weeks,
        "team_size": team_size,
    })

    return ProjectBlueprint.model_validate({
        "project_idea": project_idea.strip(),
        "feasibility": result["feasibility"],
        "scope": result["scope"],
        "technology": result["technology"],
        "planning": result["planning"],
        "risk_assessment": result["risk_assessment"],
    })
