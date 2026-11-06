import logging
from ai_engine.agents.common import generate_structured
from ai_engine.agents.heuristic_fallback import fallback_scope
from ai_engine.schemas import ScopeResult

logger = logging.getLogger(__name__)


def define_scope(
    project_idea: str,
    feasibility: dict,
    duration_weeks: int,
    team_size: int | None,
) -> ScopeResult:
    team_label = str(team_size) if team_size is not None else "not specified"
    prompt = f"""Act as a university capstone project scope analyst.
Define a clear, bounded, and academically verifiable project scope based on the project idea and feasibility findings.
Prevent scope creep while establishing sufficient depth for an impressive academic evaluation.
Return JSON only matching this exact schema: {ScopeResult.model_json_schema()}

Describe a concrete proposed solution that addresses the project's stated problem.
CRITICAL REAL-TIME REQUIREMENTS & DOMAIN DIRECTIVES:
- Directly analyze the specific domain, real-world operational challenges, and sensory/data inputs of: {project_idea.strip()}
- DO NOT provide generic boilerplate requirements such as "User authentication", "Data ingestion and validation pipeline", or formulaic summaries.
- Every single functional requirement MUST be concrete, technical, and domain-grounded (specifying exact inputs, algorithms/models, processing logic, and expected outputs/actions).
- Non-functional requirements must specify concrete numerical metrics (e.g., latency in ms, FPS, sensor polling intervals, throughput, uptime, security standards).
- Target users must identify real operators, stakeholders, and practitioners for this specific domain.
- MVP features must describe the core functional prototype demonstrable live in viva.
- Out of scope must explicitly eliminate features that would cause capstone scope creep in this domain.

Idea: {project_idea.strip()}
Duration: {duration_weeks} weeks; Team size: {team_label}
Feasibility Context: {feasibility}"""

    try:
        return generate_structured(prompt, ScopeResult)
    except Exception as exc:
        logger.warning(f"Scope agent live LLM call unavailable ({exc}); using domain-aware fallback.")
        return fallback_scope(project_idea, feasibility, duration_weeks, team_size)
