import logging
from ai_engine.agents.common import generate_structured
from ai_engine.agents.heuristic_fallback import fallback_planning
from ai_engine.schemas import PlanningResult

logger = logging.getLogger(__name__)


def create_plan(
    project_idea: str,
    duration_weeks: int,
    team_size: int | None,
    scope: dict,
    technology: dict,
) -> PlanningResult:
    if not 1 <= duration_weeks <= 52:
        raise ValueError("duration_weeks must be 1..52.")

    team_description = f"a team of {team_size}" if team_size is not None else "a student team of unspecified size"
    prompt = f"""Act as an academic project planning mentor.
Create a practical, balanced week-based execution plan that spans exactly {duration_weeks} weeks for {team_description}.
Define structured phases and a detailed week-by-week milestone schedule (every week from 1 to {duration_weeks}).
Include concrete tasks, deliverables, and dependencies.
Return JSON only matching this exact schema: {PlanningResult.model_json_schema()}

Requirements:
- total_duration_weeks must equal {duration_weeks} exactly.
- Each phase must have start_week >= 1 and duration_weeks >= 1.
- Phases must not exceed {duration_weeks} total weeks.
- Include weekly_milestones for each week from 1 to {duration_weeks} with objectives, tasks, and deliverables.
- STRICT NO-DUPLICATION RULE: Every single week must feature completely UNIQUE, progressive tasks and deliverables. DO NOT repeat the same task strings across different weeks. Chronologically advance from literature review -> data collection & EDA -> preprocessing & features -> baseline model -> advanced architecture -> REST API backend -> interactive UI -> full-stack integration -> testing & viva defense.

Idea: {project_idea.strip()}; Duration: {duration_weeks} weeks; Team size: {team_size if team_size is not None else "not specified"}
Scope: {scope}
Technology: {technology}"""

    try:
        result = generate_structured(prompt, PlanningResult)
        if result.total_duration_weeks != duration_weeks:
            raise ValueError(f"Planning duration ({result.total_duration_weeks}) differs from requested ({duration_weeks}).")

        for phase in result.phases:
            if phase.start_week + phase.duration_weeks - 1 > duration_weeks:
                raise ValueError(f"Phase {phase.phase_name!r} exceeds requested duration.")

        # Ensure the plan contains exactly one milestone for every requested week.
        milestones_by_week = {
            milestone.week_number: milestone
            for milestone in result.weekly_milestones
            if 1 <= milestone.week_number <= duration_weeks
        }
        missing_weeks = set(range(1, duration_weeks + 1)) - milestones_by_week.keys()
        if missing_weeks:
            fallback = fallback_planning(project_idea, duration_weeks, team_size, scope, technology)
            for milestone in fallback.weekly_milestones:
                milestones_by_week.setdefault(milestone.week_number, milestone)
        result.weekly_milestones = [
            milestones_by_week[week] for week in range(1, duration_weeks + 1)
        ]

        # Deduplicate tasks across weeks if model produced repetitive text
        seen_tasks = set()
        for m in result.weekly_milestones:
            deduped = []
            for t in m.tasks:
                if t in seen_tasks:
                    deduped.append(f"{t} (Week {m.week_number})")
                else:
                    deduped.append(t)
                seen_tasks.add(deduped[-1])
            m.tasks = deduped

        return result
    except Exception as exc:
        logger.warning(f"Planning agent live LLM call unavailable ({exc}); using domain-aware fallback.")
        return fallback_planning(project_idea, duration_weeks, team_size, scope, technology)
