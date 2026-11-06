import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import Base, get_db
from app.main import app
from app.models.project import Project  # noqa: F401  (makes sure the table is created)
from app.models.user import User  # noqa: F401
from app.services import project_service

GOOD_IDEA = {
    "title": "Smart Campus Lost and Found",
    "description": "A web app where students report lost items and get matches using photos.",
}


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

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(project_service, "generate_blueprint", fake_blueprint)
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def fake_blueprint(project_idea, duration_weeks, team_size, skills):
    return {
        "project_idea": project_idea,
        "duration_weeks": duration_weeks,
        "team_size": team_size,
        "feasibility": {"feasibility": "Medium", "required_resources": [], "potential_challenges": []},
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


def auth_headers(client, email):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test Student", "email": email, "password": "password123"},
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_create_project_valid(client):
    headers = auth_headers(client, "a@example.com")
    response = client.post("/api/projects", json=GOOD_IDEA, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == GOOD_IDEA["title"]
    assert body["status"] == "submitted"


def test_description_too_short(client):
    headers = auth_headers(client, "a@example.com")
    bad = {"title": "Good title", "description": "too short"}
    response = client.post("/api/projects", json=bad, headers=headers)
    assert response.status_code == 422


def test_description_whitespace_only(client):
    headers = auth_headers(client, "a@example.com")
    bad = {"title": "Good title", "description": " " * 30}
    response = client.post("/api/projects", json=bad, headers=headers)
    assert response.status_code == 422


def test_new_project_metadata_must_be_complete(client):
    headers = auth_headers(client, "incomplete@example.com")
    response = client.post(
        "/api/projects",
        headers=headers,
        json={**GOOD_IDEA, "domain": "Education"},
    )
    assert response.status_code == 422
    assert "require domain, department, technology_stack, and duration_weeks" in response.json()["detail"][0]["msg"]


def test_no_token(client):
    assert client.post("/api/projects", json=GOOD_IDEA).status_code == 401
    assert client.get("/api/projects").status_code == 401


def test_list_only_own_projects(client):
    headers_a = auth_headers(client, "a@example.com")
    headers_b = auth_headers(client, "b@example.com")
    client.post("/api/projects", json=GOOD_IDEA, headers=headers_a)

    list_a = client.get("/api/projects", headers=headers_a).json()
    list_b = client.get("/api/projects", headers=headers_b).json()

    assert len(list_a) == 1
    assert list_b == []


def test_project_metadata_optional_team_and_dynamic_duration(client):
    headers = auth_headers(client, "dynamic@example.com")
    response = client.post(
        "/api/projects",
        headers=headers,
        json={
            **GOOD_IDEA,
            "domain": "Education",
            "department": "Artificial Intelligence and Machine Learning (AIML)",
            "technology_stack": "React, FastAPI, PostgreSQL",
            "duration_weeks": 10,
        },
    )
    assert response.status_code == 201
    project = response.json()
    assert project["duration_weeks"] == 10
    assert project["department"].endswith("(AIML)")
    assert project["team_size"] is None
    assert project["guide_name"] is None

    blueprint = client.get(
        f"/api/projects/{project['id']}/blueprint",
        headers=headers,
    )
    assert blueprint.status_code == 200
    milestones = blueprint.json()["planning"]["weekly_milestones"]
    assert len(milestones) == 10
    assert all(item["status"] == "pending" for item in milestones)
    assert all(item["expected_completion_date"] for item in milestones)


def test_project_with_optional_team_and_guide_fields(client):
    headers = auth_headers(client, "complete_project@example.com")
    response = client.post(
        "/api/projects",
        headers=headers,
        json={
            **GOOD_IDEA,
            "domain": "Education",
            "department": "Computer Science & Engineering (CSE)",
            "technology_stack": "React, FastAPI, PostgreSQL",
            "duration_weeks": 6,
            "team_size": 4,
            "guide_name": "Dr. Example Guide",
        },
    )
    assert response.status_code == 201
    assert response.json()["team_size"] == 4
    assert response.json()["guide_name"] == "Dr. Example Guide"
    blueprint = client.get(
        f"/api/projects/{response.json()['id']}/blueprint",
        headers=headers,
    )
    assert blueprint.status_code == 200
    assert len(blueprint.json()["planning"]["weekly_milestones"]) == 6


@pytest.mark.parametrize("duration_weeks", [1, 7, 52])
def test_project_blueprint_matches_requested_duration_and_null_optional_fields(client, duration_weeks):
    headers = auth_headers(client, f"duration-{duration_weeks}@example.com")
    response = client.post(
        "/api/projects",
        headers=headers,
        json={
            **GOOD_IDEA,
            "domain": "Education",
            "department": "Artificial Intelligence and Machine Learning (AIML)",
            "technology_stack": "React, FastAPI, PostgreSQL",
            "duration_weeks": duration_weeks,
            "team_size": None,
            "guide_name": None,
        },
    )
    assert response.status_code == 201
    project = response.json()
    assert project["team_size"] is None
    assert project["guide_name"] is None

    blueprint = client.get(f"/api/projects/{project['id']}/blueprint", headers=headers)
    assert blueprint.status_code == 200
    milestones = blueprint.json()["planning"]["weekly_milestones"]
    assert [milestone["week_number"] for milestone in milestones] == list(range(1, duration_weeks + 1))


def test_blueprint_generation_failure_returns_error_without_saving_project(client, monkeypatch):
    headers = auth_headers(client, "blueprint-failure@example.com")

    def fail_blueprint(**kwargs):
        raise RuntimeError("AI provider unavailable")

    monkeypatch.setattr(project_service, "generate_blueprint", fail_blueprint)
    response = client.post(
        "/api/projects",
        headers=headers,
        json={
            **GOOD_IDEA,
            "domain": "Education",
            "department": "Computer Science & Engineering (CSE)",
            "technology_stack": "React, FastAPI, PostgreSQL",
            "duration_weeks": 5,
        },
    )
    assert response.status_code == 502
    assert "no project was saved" in response.json()["detail"]
    assert client.get("/api/projects", headers=headers).json() == []


def test_student_profile_accepts_aiml(client):
    headers = auth_headers(client, "aiml@example.com")
    saved = client.post(
        "/api/students/profile",
        headers=headers,
        json={
            "institution": "Example University",
            "department": "Artificial Intelligence and Machine Learning (AIML)",
            "semester": "Semester 6",
            "graduation_year": 2027,
        },
    )
    assert saved.status_code == 200
    profile = client.get("/api/students/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["department"] == "Artificial Intelligence and Machine Learning (AIML)"