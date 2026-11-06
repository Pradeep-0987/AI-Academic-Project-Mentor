"""Generate a proposed revised plan from progress evidence; never mutate stored plans."""
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

def propose_plan_adjustment(current_plan: dict, progress_analysis: dict, new_constraints: dict | None = None) -> dict:
    if not isinstance(current_plan,dict) or not isinstance(progress_analysis,dict):
        raise ValueError("current_plan and progress_analysis must be dictionaries.")
    prompt=f"""You are a project planning agent. Propose a revision that preserves completed work,
keeps dependencies valid, and explicitly explains any scope trade-offs. Do not claim the
proposal has been applied. Return JSON only with revised_plan (object), changes (array of
objects with item, reason, impact), risks (array), student_approval_required (boolean),
mentor_review_required (boolean).
Current plan: {current_plan}
Progress evidence/analysis: {progress_analysis}
New constraints: {new_constraints or {}}"""
    result=extract_json(generate_text(prompt))
    required={"revised_plan","changes","risks","student_approval_required","mentor_review_required"}
    if required-result.keys(): raise ValueError("Plan adjustment response missing required fields.")
    result["applied"]=False
    return result
