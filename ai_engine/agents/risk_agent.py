import logging
from ai_engine.agents.common import generate_structured
from ai_engine.agents.heuristic_fallback import fallback_risks
from ai_engine.schemas import RiskResult

logger = logging.getLogger(__name__)


def assess_risks(
    project_idea: str,
    feasibility: dict,
    scope: dict,
    technology: dict,
    planning: dict,
) -> RiskResult:
    prompt = f"""Act as a project risk analyst. Identify specific academic project risks and
provide likelihood, impact, mitigation and contingency. Consider data, scope, schedule,
integration, quality and API risks where relevant. Return JSON only matching:
{RiskResult.model_json_schema()}
Idea: {project_idea}
Feasibility: {feasibility}
Scope: {scope}
Technology: {technology}
Planning: {planning}"""

    try:
        return generate_structured(prompt, RiskResult)
    except Exception as exc:
        logger.warning(f"Risk agent live LLM call unavailable ({exc}); using domain-aware fallback.")
        return fallback_risks(project_idea, feasibility, scope, technology, planning)
