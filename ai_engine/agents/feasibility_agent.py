import logging
from ai_engine.agents.common import generate_structured
from ai_engine.agents.heuristic_fallback import fallback_feasibility
from ai_engine.schemas import FeasibilityResult

logger = logging.getLogger(__name__)


def analyse_feasibility(
    project_idea: str,
    duration_weeks: int,
    team_size: int | None,
    skills: list[str] | None = None,
) -> FeasibilityResult:
    if not project_idea or len(project_idea.strip()) < 3:
        raise ValueError("Provide a meaningful project idea.")
    if not 1 <= duration_weeks <= 52:
        raise ValueError("duration_weeks must be 1..52.")
    if team_size is not None and not 1 <= team_size <= 20:
        raise ValueError("team_size must be 1..20.")

    team_capacity = f"a team of {team_size}" if team_size is not None else "the available student team"
    prompt = f"""Act as a senior academic project feasibility analyst.
Evaluate the feasibility of the proposed academic project idea based on timeline, team capacity, and technical requirements.
Return JSON only matching this exact schema: {FeasibilityResult.model_json_schema()}

CRITICAL PROBLEM STATEMENT & DOMAIN DIRECTIVES:
- Directly analyze the specific domain, real-world context, and technical architecture of: {project_idea.strip()}
- Formulate a tailored, realistic problem statement describing the exact practical bottlenecks, operational pain points, and current limitations that this project addresses. DO NOT output generic template phrases like "Addressing the challenges in X through a data-driven methodology".
- Required skills must list the exact libraries, hardware/IoT protocols, and ML architectures needed for this specific topic.
- Required resources must list actual domain datasets (e.g., Kaggle, Hugging Face, UCI), specialized hardware/sensors (if applicable), and compute needs.
- Potential challenges and recommendations must address domain-specific engineering hurdles (e.g. lighting variation in computer vision, sensor noise in IoT, imbalanced classes in fraud/medical, real-time latency).

Criteria to analyze:
1. Feasibility: High / Medium / Low (consider if {duration_weeks} weeks and {team_capacity} is realistic)
2. Economic feasibility: High / Medium / Low, with a specific cost and resource rationale.
3. Operational feasibility: High / Medium / Low, with a specific workflow and adoption rationale.
4. Complexity: Beginner / Intermediate / Advanced
5. Required skills and domain competencies
6. Required hardware, software, datasets, and API resources
7. Specific technical challenges and bottlenecks
8. Strategic recommendations to ensure successful academic defense
9. Academic assumptions made
10. Detailed reasoning explaining the feasibility rating and complexity assignment

Idea: {project_idea.strip()}
Duration weeks: {duration_weeks}
Team size: {team_size if team_size is not None else "not specified; do not assume a team size"}
Student Skills: {skills or []}"""

    try:
        return generate_structured(prompt, FeasibilityResult)
    except Exception as exc:
        logger.warning(f"Feasibility agent live LLM call unavailable ({exc}); using domain-aware fallback.")
        return fallback_feasibility(project_idea, duration_weeks, team_size, skills)
