import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import Base, get_db
from app.main import app as fastapi_app
from app.models import ProjectBlueprint  # noqa: F401
from app.services import project_service


@pytest.fixture()
def client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(project_service, "generate_blueprint", fake_blueprint)
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def fake_blueprint(project_idea, duration_weeks, team_size, skills):
    result = {
        "project_idea": project_idea,
        "duration_weeks": duration_weeks,
        "team_size": team_size,
        "feasibility": {"feasibility": "Medium"},
        "scope": {"project_objective": "Deliver a tested academic prototype."},
        "technology": {"backend": ["FastAPI"], "reasoning": "A suitable API stack."},
        "planning": {
            "total_duration_weeks": duration_weeks,
            "phases": [{"phase_name": "Build", "start_week": 1, "duration_weeks": duration_weeks, "tasks": ["Implement"], "deliverables": ["Prototype"], "dependencies": []}],
            "weekly_milestones": [
                {"week_number": week, "milestone_title": f"Week {week}", "objectives": ["Progress"], "tasks": [f"Task {week}"], "deliverables": [f"Deliverable {week}"]}
                for week in range(1, duration_weeks + 1)
            ],
        },
        "risk": {"risks": []},
        "quality_report": {"valid": True, "errors": [], "warnings": [], "warning_count": 0},
    }
    return result


def auth_headers(client, email):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": email, "password": "password123"},
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_create_project_auto_generates_blueprint(client):
    headers = auth_headers(client, "student_bp@example.com")
    project_payload = {
        "title": "Smart Attendance System via Facial Recognition",
        "description": "An automated system tracking classroom attendance in real-time using deep learning.",
    }
    create_res = client.post("/api/projects", json=project_payload, headers=headers)
    assert create_res.status_code == 201
    project_id = create_res.json()["id"]

    # Retrieve auto-generated blueprint
    bp_res = client.get(f"/api/projects/{project_id}/blueprint", headers=headers)
    assert bp_res.status_code == 200
    bp = bp_res.json()

    assert "feasibility" in bp
    assert bp["feasibility"]["feasibility"] in {"High", "Medium", "Low"}
    assert "scope" in bp
    assert "technology" in bp
    assert "planning" in bp
    assert len(bp["planning"]["weekly_milestones"]) == 8


def test_preview_blueprint_endpoint(client):
    headers = auth_headers(client, "preview_user@example.com")
    preview_payload = {
        "idea": "Predictive maintenance for industrial wind turbines using vibration sensors and LSTM",
        "duration_weeks": 6,
        "team_size": 3,
        "skills": ["Python", "TensorFlow", "IoT"],
    }
    res = client.post("/api/projects/blueprint/preview", json=preview_payload, headers=headers)
    assert res.status_code == 200
    bp = res.json()

    assert bp["planning"]["total_duration_weeks"] == 6
    assert len(bp["planning"]["weekly_milestones"]) == 6
    assert len(bp["technology"]["backend"]) > 0
    assert len(bp["technology"].get("reasoning") or bp["technology"].get("rationale")) > 0


def test_regenerate_project_blueprint(client):
    headers = auth_headers(client, "regen_user@example.com")
    project_payload = {
        "title": "Autonomous Drone Path Planning with Obstacle Avoidance",
        "description": "Reinforcement learning based trajectory optimization for micro-aerial vehicles in GPS-denied environments.",
    }
    create_res = client.post("/api/projects", json=project_payload, headers=headers)
    project_id = create_res.json()["id"]

    # Trigger custom regeneration with 10 weeks
    regen_res = client.post(
        f"/api/projects/{project_id}/blueprint?duration_weeks=10&team_size=4",
        headers=headers,
    )
    assert regen_res.status_code == 200
    bp = regen_res.json()
    assert bp["planning"]["total_duration_weeks"] == 10
    assert len(bp["planning"]["weekly_milestones"]) == 10


def test_update_milestone_status_updates_real_progress(client):
    headers = auth_headers(client, "progress_user@example.com")
    created = client.post("/api/projects", json={
        "title": "Campus Water Quality Tracker",
        "description": "A sensor dashboard that records and analyzes campus drinking water quality readings.",
        "domain": "Environmental monitoring",
        "department": "Computer Science & Engineering (CSE)",
        "technology_stack": "React, FastAPI, PostgreSQL",
        "duration_weeks": 4,
    }, headers=headers)
    assert created.status_code == 201
    project_id = created.json()["id"]

    updated = client.patch(
        f"/api/projects/{project_id}/milestones/1",
        json={"status": "completed"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["planning"]["weekly_milestones"][0]["status"] == "completed"
    project = client.get("/api/projects", headers=headers).json()[0]
    assert project["milestones_completed"] == 1
    assert project["progress"] == 25


def test_project_chat_uses_owned_project_context(client, monkeypatch):
    headers = auth_headers(client, "chat_user@example.com")
    created = client.post("/api/projects", json={
        "title": "Campus Water Quality Tracker",
        "description": "A sensor dashboard that records and analyzes campus drinking water quality readings.",
        "domain": "Environmental monitoring",
        "department": "Computer Science & Engineering (CSE)",
        "technology_stack": "React, FastAPI, PostgreSQL",
        "duration_weeks": 3,
    }, headers=headers)
    project_id = created.json()["id"]
    seen = {}

    def fake_chat(message, project_context, history):
        seen.update(project_context)
        return {"answer": "Use the project's stored weekly plan.", "suggested_actions": [], "evidence_used": [], "follow_up_question": None}

    monkeypatch.setattr("ai_engine.mentor.chat_service.chat_with_mentor", fake_chat)
    response = client.post(
        f"/api/projects/{project_id}/chat",
        json={"message": "What should I work on?", "history": [{"role": "user", "content": "Hello"}]},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["answer"] == "Use the project's stored weekly plan."
    assert seen["project"]["title"] == "Campus Water Quality Tracker"
    assert seen["project"]["total_milestones"] == 3
