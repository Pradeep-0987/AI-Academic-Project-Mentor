"""Deterministic progress metrics plus AI recommendations; never persists changes."""
from datetime import date
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

def calculate_completion_percentage(completed_tasks: int, total_tasks: int) -> float:
    if total_tasks < 0: raise ValueError("total_tasks cannot be negative.")
    if completed_tasks < 0 or completed_tasks > total_tasks:
        raise ValueError("completed_tasks must be between zero and total_tasks.")
    return round(completed_tasks / total_tasks * 100, 2) if total_tasks else 0.0

def calculate_progress_metrics(tasks: list[dict]) -> dict:
    """Calculate transparent status metrics from task records (no LLM required)."""
    if not isinstance(tasks, list): raise ValueError("tasks must be a list.")
    completed=0; in_progress=0; pending=0; overdue=0; invalid_dates=[]
    today=date.today()
    for task in tasks:
        if not isinstance(task,dict): continue
        status=str(task.get("status","pending")).strip().lower().replace(" ","_")
        if status in {"completed","complete","done"}: completed += 1
        elif status in {"in_progress","in-progress","ongoing"}: in_progress += 1
        else: pending += 1
        due=task.get("due_date") or task.get("deadline")
        if due and status not in {"completed","complete","done"}:
            try:
                due_date=date.fromisoformat(str(due)[:10])
                if due_date < today: overdue += 1
            except ValueError: invalid_dates.append(str(due))
    total=completed+in_progress+pending
    return {"total_tasks":total,"completed_tasks":completed,"in_progress_tasks":in_progress,
            "pending_tasks":pending,"overdue_tasks":overdue,
            "completion_percentage":calculate_completion_percentage(completed,total),
            "invalid_due_dates":invalid_dates}

def analyse_progress(plan: dict, progress: dict, current_date: str | None = None) -> dict:
    if not isinstance(plan,dict) or not isinstance(progress,dict):
        raise ValueError("plan and progress must be dictionaries.")
    metrics=calculate_progress_metrics(progress.get("tasks", [])) if isinstance(progress.get("tasks"),list) else {}
    prompt=f"""Compare the plan with the student-reported progress. Give actionable, realistic
recommendations. Do not claim a delay unless dates/status support it. Never modify the plan.
Return JSON only with summary (string), delayed_tasks (array), blockers (array), priorities
(array), schedule_adjustments (array of proposals), reasoning (string), and questions_for_student (array).
Current date: {current_date or date.today().isoformat()}
Deterministic task metrics: {metrics}
Plan: {plan}
Reported progress: {progress}"""
    result=extract_json(generate_text(prompt))
    required=("summary","delayed_tasks","blockers","priorities","schedule_adjustments","reasoning")
    if any(k not in result for k in required): raise ValueError("Progress analysis is missing required fields.")
    result["metrics"]=metrics
    result["changes_applied"]=False
    return result
