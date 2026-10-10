from langgraph.graph import StateGraph, START, END

from agents.feasibility_agent import FeasibilityAgent
from agents.scope_agent import ScopeAgent
from agents.technology_agent import TechnologyAgent
from agents.planning_agent import PlanningAgent
from agents.risk_agent import RiskAgent
from agents.research_agent import ResearchAgent
from agents.dataset_agent import DatasetAgent
from agents.architecture_agent import ArchitectureAgent
from agents.testing_agent import TestingAgent
from agents.documentation_agent import DocumentationAgent

from schemas.blueprint_schema import ProjectBlueprint
from workflows.state import BlueprintState


def feasibility_node(state: BlueprintState) -> dict:
    result = FeasibilityAgent().evaluate(state["project_idea"])
    return {"feasibility": result.model_dump()}


def scope_node(state: BlueprintState) -> dict:
    result = ScopeAgent().generate_scope(state["project_idea"])
    return {"scope": result.model_dump()}


def technology_node(state: BlueprintState) -> dict:
    result = TechnologyAgent().recommend(
        project_idea=state["project_idea"],
        project_scope=str(state["scope"]),
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


def research_node(state: BlueprintState) -> dict:
    result = ResearchAgent().create_plan(
        state["project_idea"], scope=str(state["scope"])
    )
    return {"research": result.model_dump()}


def dataset_node(state: BlueprintState) -> dict:
    result = DatasetAgent().assess(
        state["project_idea"], scope=str(state["scope"])
    )
    return {"dataset": result.model_dump()}


def architecture_node(state: BlueprintState) -> dict:
    result = ArchitectureAgent().design(
        project_idea=state["project_idea"],
        scope=str(state["scope"]),
        technology=str(state["technology"]),
    )
    return {"architecture": result.model_dump()}


def testing_node(state: BlueprintState) -> dict:
    result = TestingAgent().create_plan(
        project_idea=state["project_idea"],
        scope=str(state["scope"]),
        architecture=str(state["architecture"]),
    )
    return {"testing": result.model_dump()}


def documentation_node(state: BlueprintState) -> dict:
    result = DocumentationAgent().create_plan(
        project_idea=state["project_idea"],
        scope=str(state["scope"]),
        architecture=str(state["architecture"]),
        testing=str(state["testing"]),
    )
    return {"documentation": result.model_dump()}


def build_blueprint_graph():
    graph = StateGraph(BlueprintState)

    nodes = [
        ("feasibility", feasibility_node),
        ("scope", scope_node),
        ("technology", technology_node),
        ("planning", planning_node),
        ("risk_assessment", risk_node),
        ("research", research_node),
        ("dataset", dataset_node),
        ("architecture", architecture_node),
        ("testing", testing_node),
        ("documentation", documentation_node),
    ]
    for name, node in nodes:
        graph.add_node(name, node)

    graph.add_edge(START, "feasibility")
    graph.add_edge("feasibility", "scope")
    graph.add_edge("scope", "technology")
    graph.add_edge("technology", "planning")
    graph.add_edge("planning", "risk_assessment")
    graph.add_edge("risk_assessment", "research")
    graph.add_edge("research", "dataset")
    graph.add_edge("dataset", "architecture")
    graph.add_edge("architecture", "testing")
    graph.add_edge("testing", "documentation")
    graph.add_edge("documentation", END)

    return graph.compile()


def generate_blueprint(
    project_idea: str,
    duration_weeks: int = 8,
    team_size: int = 6,
) -> ProjectBlueprint:
    if not project_idea or not project_idea.strip():
        raise ValueError("Project idea cannot be empty.")
    if not 1 <= duration_weeks <= 52:
        raise ValueError("duration_weeks must be between 1 and 52.")
    if not 1 <= team_size <= 20:
        raise ValueError("team_size must be between 1 and 20.")

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
        "research": result["research"],
        "dataset": result["dataset"],
        "architecture": result["architecture"],
        "testing": result["testing"],
        "documentation": result["documentation"],
    })
