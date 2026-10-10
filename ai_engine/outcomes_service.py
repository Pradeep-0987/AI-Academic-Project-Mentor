"""Documentation generation and faculty project monitoring services."""
import json
import os
import sqlite3
from datetime import datetime, timezone, date
from pathlib import Path

from dotenv import load_dotenv
from mentor_service import init_db

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
DB_PATH = BASE_DIR / "data" / "mentor.db"
load_dotenv(ENV_FILE, override=False)


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def _now():
    return datetime.now(timezone.utc).isoformat()


def init_outcome_tables():
    with _connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS generated_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL REFERENCES mentor_projects(id) ON DELETE CASCADE,
                document_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        db.commit()


def _project_context(project_id):
    with _connect() as db:
        project = db.execute(
            "SELECT * FROM mentor_projects WHERE id = ?", (project_id,)
        ).fetchone()
        if not project:
            return None
        project = dict(project)
        project["milestones"] = [
            dict(row) for row in db.execute(
                "SELECT title, description, due_date, status, updated_at "
                "FROM mentor_milestones WHERE project_id = ? ORDER BY id",
                (project_id,),
            ).fetchall()
        ]
        project["blueprints"] = [
            {
                "id": row["id"],
                "project_idea": row["project_idea"],
                "blueprint": json.loads(row["blueprint_json"]),
                "quality_report": json.loads(row["quality_report_json"]),
                "created_at": row["created_at"],
            }
            for row in db.execute(
                "SELECT * FROM mentor_blueprints WHERE project_idea = ? "
                "ORDER BY id DESC LIMIT 5", (project["idea"],)
            ).fetchall()
        ]
        return project


def generate_document(project_id: int, document_type: str):
    allowed = {"synopsis", "methodology", "progress_report"}
    if document_type not in allowed:
        raise ValueError("document_type must be synopsis, methodology, or progress_report")

    project = _project_context(project_id)
    if not project:
        raise LookupError("Project not found.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(f"GEMINI_API_KEY is missing. Configure {ENV_FILE}.")

    milestones = project.get("milestones", [])
    total = len(milestones)
    completed = sum(m.get("status") == "completed" for m in milestones)
    blocked = sum(m.get("status") == "blocked" for m in milestones)
    today = date.today().isoformat()
    overdue = sum(
        bool(m.get("due_date")) and m["due_date"][:10] < today
        and m.get("status") != "completed" for m in milestones
    )
    progress = {
        "total_milestones": total,
        "completed": completed,
        "blocked": blocked,
        "overdue": overdue,
        "completion_percent": round(completed / total * 100) if total else 0,
    }

    blueprint = project["blueprints"][0]["blueprint"] if project["blueprints"] else {}
    labels = {
        "synopsis": "Academic Project Synopsis",
        "methodology": "Project Methodology",
        "progress_report": "Project Progress Report",
    }
    instructions = {
        "synopsis": (
            "Write an academic project synopsis with title, abstract, problem "
            "statement, motivation, objectives, scope, proposed methodology, "
            "technology stack, expected outcomes, limitations, and references/search leads. "
            "Clearly label expected outcomes as proposed, not achieved."
        ),
        "methodology": (
            "Write a detailed, reproducible methodology with phases, architecture, "
            "data collection/validation, algorithms or implementation steps, testing, "
            "evaluation metrics, tools, and limitations. Do not claim experiments were run "
            "unless the supplied context proves it."
        ),
        "progress_report": (
            "Write a dated progress report with project overview, completed work, "
            "in-progress work, blocked and overdue milestones, completion percentage, "
            "risks, next actions, and a short supervisor summary. Use only milestone statuses "
            "from the supplied context as evidence of completed work. Explicitly state when "
            "there is no tracked evidence."
        ),
    }
    context = {
        "project": {k: project.get(k) for k in ("name", "idea", "status", "target_date", "created_at")},
        "milestones": milestones,
        "calculated_progress": progress,
        "latest_blueprint": blueprint,
        "today": today,
    }
    from google import genai
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    response = client.models.generate_content(
        model=model,
        contents=(
            "You are an academic project documentation assistant. Write clear, "
            "professional Markdown. Never fabricate citations, data, results, approvals, "
            "or completed work. Mark missing information as 'To be confirmed'.\n\n"
            f"DOCUMENT REQUEST: {instructions[document_type]}\n\n"
            f"PROJECT RECORD (source of truth):\n{json.dumps(context, ensure_ascii=False, default=str)}"
        ),
    )
    content = (response.text or "").strip()
    if not content:
        raise RuntimeError("The documentation model returned an empty response.")
    title = f"{labels[document_type]} — {project['name']}"
    with _connect() as db:
        cur = db.execute(
            "INSERT INTO generated_documents(project_id, document_type, title, content, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (project_id, document_type, title, content, _now()),
        )
        db.commit()
        document_id = cur.lastrowid
    return {
        "id": document_id,
        "project_id": project_id,
        "document_type": document_type,
        "title": title,
        "content": content,
        "created_at": _now(),
        "progress_snapshot": progress,
    }


def list_documents(project_id: int):
    with _connect() as db:
        return [dict(row) for row in db.execute(
            "SELECT id, project_id, document_type, title, created_at "
            "FROM generated_documents WHERE project_id = ? ORDER BY id DESC",
            (project_id,),
        ).fetchall()]


def get_document(document_id: int):
    with _connect() as db:
        row = db.execute(
            "SELECT * FROM generated_documents WHERE id = ?", (document_id,)
        ).fetchone()
    return dict(row) if row else None


def faculty_dashboard():
    """Aggregate project health from persisted milestone facts, not an AI-invented score."""
    today = date.today().isoformat()
    with _connect() as db:
        projects = db.execute("SELECT * FROM mentor_projects ORDER BY updated_at DESC").fetchall()
        items = []
        for row in projects:
            p = dict(row)
            milestones = [dict(m) for m in db.execute(
                "SELECT title, due_date, status FROM mentor_milestones WHERE project_id = ?",
                (p["id"],),
            ).fetchall()]
            total = len(milestones)
            completed = sum(m["status"] == "completed" for m in milestones)
            blocked = sum(m["status"] == "blocked" for m in milestones)
            overdue = sum(
                bool(m.get("due_date")) and m["due_date"][:10] < today
                and m["status"] != "completed" for m in milestones
            )
            if blocked or overdue:
                health = "needs_attention"
            elif total and completed == total:
                health = "completed"
            elif total == 0:
                health = "not_started"
            else:
                health = "on_track"
            summary = (
                f"{p['name']}: {completed}/{total} milestones completed "
                f"({round(completed / total * 100) if total else 0}%). "
                f"{blocked} blocked and {overdue} overdue. "
                f"Health: {health.replace('_', ' ')}."
            )
            items.append({
                "id": p["id"],
                "name": p["name"],
                "idea": p["idea"],
                "status": p["status"],
                "target_date": p["target_date"],
                "created_at": p["created_at"],
                "updated_at": p["updated_at"],
                "milestone_count": total,
                "completed_count": completed,
                "blocked_count": blocked,
                "overdue_count": overdue,
                "progress_percent": round(completed / total * 100) if total else 0,
                "health": health,
                "summary": summary,
                "milestones": milestones,
            })
    return {
        "generated_at": _now(),
        "total_projects": len(items),
        "needs_attention": sum(p["health"] == "needs_attention" for p in items),
        "completed_projects": sum(p["health"] == "completed" for p in items),
        "average_progress_percent": round(sum(p["progress_percent"] for p in items) / len(items)) if items else 0,
        "projects": items,
        "note": "Health is rule-based from stored milestone statuses and due dates; it is not a predictive assessment.",
    }


init_db()
init_outcome_tables()
