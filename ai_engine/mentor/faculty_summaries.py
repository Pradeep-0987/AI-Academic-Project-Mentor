"""Faculty monitoring summaries from supplied project records."""
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

def calculate_project_health(project: dict) -> dict:
    tasks=project.get("tasks", []) if isinstance(project,dict) else []
    if not isinstance(tasks,list): tasks=[]
    total=len(tasks); completed=sum(1 for t in tasks if isinstance(t,dict) and str(t.get("status","")).lower() in {"completed","complete","done"})
    overdue=sum(1 for t in tasks if isinstance(t,dict) and t.get("is_overdue") and str(t.get("status","")).lower() not in {"completed","complete","done"})
    pct=round(completed*100/total,2) if total else 0.0
    explicit_risks=project.get("risk_level", "unknown")
    health="At risk" if overdue or str(explicit_risks).lower() in {"high","critical"} else ("Needs attention" if pct < 40 and total else "On track")
    return {"project_id":project.get("id"),"project_title":project.get("title") or project.get("name") or "Untitled project",
            "total_tasks":total,"completed_tasks":completed,"overdue_tasks":overdue,
            "completion_percentage":pct,"health_status":health}

def summarize_faculty_portfolio(projects: list[dict]) -> dict:
    if not isinstance(projects,list): raise ValueError("projects must be a list.")
    health=[calculate_project_health(p) for p in projects if isinstance(p,dict)]
    if not health: return {"portfolio_summary":"No project records were supplied.","project_health":[],"attention_required":[],"limitations":["No data supplied"]}
    prompt=f"""Prepare a concise faculty portfolio summary based only on these records.
Do not invent student names, dates, causes, or accomplishments. Highlight projects that need
attention and suggest neutral mentor follow-ups. Return JSON only with portfolio_summary,
attention_required (array of objects with project_id, reason, suggested_follow_up), and limitations (array).
Computed project health: {health}
Raw project records: {projects}"""
    result=extract_json(generate_text(prompt))
    if not isinstance(result.get("portfolio_summary"),str): raise ValueError("Missing portfolio_summary.")
    result["project_health"]=health
    return result
