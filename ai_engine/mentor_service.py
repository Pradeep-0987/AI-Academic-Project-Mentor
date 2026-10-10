"""Persistence and Gemini-backed conversational mentoring services."""
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
DB_PATH = BASE_DIR / "data" / "mentor.db"
load_dotenv(ENV_FILE, override=False)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS mentor_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            idea TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            target_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mentor_milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL REFERENCES mentor_projects(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mentor_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES mentor_projects(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mentor_blueprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_idea TEXT NOT NULL,
            duration_weeks INTEGER NOT NULL,
            team_size INTEGER NOT NULL,
            blueprint_json TEXT NOT NULL,
            quality_report_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)


def row_dict(row):
    return dict(row) if row else None


def list_projects():
    with connect() as db:
        rows = db.execute("""SELECT p.*,
            (SELECT COUNT(*) FROM mentor_milestones m WHERE m.project_id=p.id) AS milestone_count,
            (SELECT COUNT(*) FROM mentor_milestones m WHERE m.project_id=p.id AND m.status='completed') AS completed_count
            FROM mentor_projects p ORDER BY p.updated_at DESC""").fetchall()
        return [row_dict(row) for row in rows]


def create_project(name, idea, target_date=None, milestones=None):
    now = utc_now()
    with connect() as db:
        cur = db.execute("INSERT INTO mentor_projects(name,idea,target_date,created_at,updated_at) VALUES(?,?,?,?,?)",
                          (name, idea, target_date, now, now))
        project_id = cur.lastrowid
        for item in milestones or []:
            db.execute("INSERT INTO mentor_milestones(project_id,title,description,due_date,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                       (project_id, item["title"], item.get("description", ""), item.get("due_date"), item.get("status", "pending"), now, now))
        db.commit()
    return get_project(project_id)


def get_project(project_id):
    with connect() as db:
        project = db.execute("SELECT * FROM mentor_projects WHERE id=?", (project_id,)).fetchone()
        if not project:
            return None
        result = row_dict(project)
        result["milestones"] = [row_dict(r) for r in db.execute(
            "SELECT * FROM mentor_milestones WHERE project_id=? ORDER BY COALESCE(due_date,'9999-12-31'), id", (project_id,)
        ).fetchall()]
        result["messages"] = [row_dict(r) for r in db.execute(
            "SELECT role,content,created_at FROM mentor_messages WHERE project_id=? ORDER BY id DESC LIMIT 30", (project_id,)
        ).fetchall()][::-1]
        return result


def add_milestone(project_id, title, description="", due_date=None):
    now = utc_now()
    with connect() as db:
        if not db.execute("SELECT id FROM mentor_projects WHERE id=?", (project_id,)).fetchone():
            return None
        cur = db.execute("INSERT INTO mentor_milestones(project_id,title,description,due_date,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                         (project_id, title, description, due_date, "pending", now, now))
        db.execute("UPDATE mentor_projects SET updated_at=? WHERE id=?", (now, project_id))
        db.commit()
        row = db.execute("SELECT * FROM mentor_milestones WHERE id=?", (cur.lastrowid,)).fetchone()
        return row_dict(row)


def update_milestone(milestone_id, status=None, title=None, description=None, due_date=None):
    allowed = {"pending", "in_progress", "completed", "blocked"}
    if status is not None and status not in allowed:
        raise ValueError("Status must be pending, in_progress, completed, or blocked.")
    with connect() as db:
        current = db.execute("SELECT * FROM mentor_milestones WHERE id=?", (milestone_id,)).fetchone()
        if not current:
            return None
        values = {
            "status": status if status is not None else current["status"],
            "title": title if title is not None else current["title"],
            "description": description if description is not None else current["description"],
            "due_date": due_date if due_date is not None else current["due_date"],
            "updated_at": utc_now(),
        }
        db.execute("UPDATE mentor_milestones SET status=?,title=?,description=?,due_date=?,updated_at=? WHERE id=?",
                   (values["status"], values["title"], values["description"], values["due_date"], values["updated_at"], milestone_id))
        db.execute("UPDATE mentor_projects SET updated_at=? WHERE id=?", (values["updated_at"], current["project_id"]))
        db.commit()
        return row_dict(db.execute("SELECT * FROM mentor_milestones WHERE id=?", (milestone_id,)).fetchone())


def save_blueprint(project_idea, duration_weeks, team_size, blueprint, quality_report):
    """Persist a generated blueprint and its quality report as JSON."""
    now = utc_now()
    with connect() as db:
        cursor = db.execute(
            """INSERT INTO mentor_blueprints
            (project_idea, duration_weeks, team_size, blueprint_json, quality_report_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                project_idea,
                duration_weeks,
                team_size,
                json.dumps(blueprint, ensure_ascii=False),
                json.dumps(quality_report, ensure_ascii=False),
                now,
            ),
        )
        db.commit()
        return get_blueprint(cursor.lastrowid)


def list_blueprints(limit=50, offset=0):
    """Return recent blueprint metadata without large generated payloads."""
    limit = max(1, min(int(limit), 100))
    offset = max(0, int(offset))
    with connect() as db:
        rows = db.execute(
            """SELECT id, project_idea, duration_weeks, team_size,
            quality_report_json, created_at
            FROM mentor_blueprints ORDER BY id DESC LIMIT ? OFFSET ?""",
            (limit, offset),
        ).fetchall()
    results = []
    for row in rows:
        item = row_dict(row)
        item["quality_report"] = json.loads(item.pop("quality_report_json"))
        results.append(item)
    return results


def get_blueprint(blueprint_id):
    """Return a complete saved blueprint."""
    with connect() as db:
        row = db.execute(
            "SELECT * FROM mentor_blueprints WHERE id = ?", (blueprint_id,)
        ).fetchone()
    if not row:
        return None
    item = row_dict(row)
    item["blueprint"] = json.loads(item.pop("blueprint_json"))
    item["quality_report"] = json.loads(item.pop("quality_report_json"))
    return item


def get_project_progress(project_id):
    """Calculate progress and overdue milestone counts from saved records."""
    project = get_project(project_id)
    if not project:
        return None
    today = datetime.now(timezone.utc).date().isoformat()
    milestones = project.get("milestones", [])
    total = len(milestones)
    completed = sum(m.get("status") == "completed" for m in milestones)
    blocked = sum(m.get("status") == "blocked" for m in milestones)
    overdue = sum(
        bool(m.get("due_date"))
        and m["due_date"][:10] < today
        and m.get("status") != "completed"
        for m in milestones
    )
    return {
        "project_id": project_id,
        "milestone_count": total,
        "completed_count": completed,
        "blocked_count": blocked,
        "overdue_count": overdue,
        "progress_percent": round(completed / total * 100) if total else 0,
        "milestones": milestones,
    }


def chat_with_mentor(message, project_id=None, history=None):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(f"GEMINI_API_KEY is missing. Configure {ENV_FILE}.")
    project = get_project(project_id) if project_id is not None else None
    if project_id is not None and project is None:
        raise ValueError("Project was not found.")
    milestones = project.get("milestones", []) if project else []
    context = {
        "project": {k: project.get(k) for k in ("name", "idea", "status", "target_date")} if project else None,
        "milestones": [{k: m.get(k) for k in ("title", "description", "due_date", "status")} for m in milestones],
        "progress": (round(sum(m["status"] == "completed" for m in milestones) / len(milestones) * 100) if milestones else 0),
    }
    safe_history = []
    for item in (history or [])[-12:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            safe_history.append(f"{role.upper()}: {content[:3000]}")
    prompt = f"""You are ProjectMentor, a supportive, practical academic project mentor for university students.
Give conversational ongoing guidance, break work into actionable steps, help track progress, manage milestones, identify blockers, and prepare for reviews/viva. Be encouraging but honest. Ask at most one clarifying question at a time. Tailor advice to the project context below. Never claim a task was completed unless the saved status says completed. If no project context exists, help generally and invite the user to create/select a project. Prefer concise, specific advice with a next action. For milestone updates, suggest what the student should change in the tracker; do not claim to modify records unless the user uses the tracker controls.

CURRENT PROJECT AND TRACKING CONTEXT:
{json.dumps(context, ensure_ascii=False)}

RECENT CONVERSATION:
{chr(10).join(safe_history)}

STUDENT MESSAGE:
{message}

Respond in helpful Markdown. Include a clear next action when appropriate."""
    from google import genai

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    response = client.models.generate_content(model=model, contents=prompt)
    answer = (response.text or "").strip()
    if not answer:
        raise RuntimeError("The AI mentor returned an empty response.")
    if project_id is not None:
        now = utc_now()
        with connect() as db:
            db.execute("INSERT INTO mentor_messages(project_id,role,content,created_at) VALUES(?,?,?,?)", (project_id, "user", message, now))
            db.execute("INSERT INTO mentor_messages(project_id,role,content,created_at) VALUES(?,?,?,?)", (project_id, "assistant", answer, now))
            db.execute("UPDATE mentor_projects SET updated_at=? WHERE id=?", (now, project_id))
            db.commit()
    return {"reply": answer, "project_context": context}


init_db()
