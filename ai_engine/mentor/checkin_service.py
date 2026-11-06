"""Weekly student check-ins that return structured coaching and proposed next steps."""
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

def review_weekly_checkin(project_context: dict, completed_this_week: list[str],
                          blockers: list[str] | None = None, confidence: int = 3) -> dict:
    if not isinstance(project_context,dict): raise ValueError("project_context must be a dictionary.")
    if not 1 <= confidence <= 5: raise ValueError("confidence must be from 1 to 5.")
    if len(completed_this_week)>100: raise ValueError("Too many completed items.")
    prompt=f"""Act as an academic project coach reviewing a weekly student check-in.
Do not assume tasks were completed beyond the student's report. Suggest a realistic next week.
Return JSON only with: reflection (string), positive_progress (array), blockers (array),
next_week_priorities (array), support_needed (array), plan_adjustment_proposals (array),
mentor_escalation_recommended (boolean), missing_information (array).
Project context: {project_context}
Student-reported completed work: {completed_this_week}
Student-reported blockers: {blockers or []}
Student confidence from 1 (low) to 5 (high): {confidence}"""
    result=extract_json(generate_text(prompt))
    required={"reflection","positive_progress","blockers","next_week_priorities","support_needed","plan_adjustment_proposals","mentor_escalation_recommended","missing_information"}
    missing=required-result.keys()
    if missing: raise ValueError("Check-in response missing: "+", ".join(sorted(missing)))
    result["plan_changes_applied"]=False
    return result
