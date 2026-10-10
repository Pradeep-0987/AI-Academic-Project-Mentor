from pathlib import Path

import mentor_service as service


def setup_module():
    # Keep tests isolated from the developer's real local database.
    service.DB_PATH = Path(__file__).parent / "test_mentor.db"
    if service.DB_PATH.exists():
        service.DB_PATH.unlink()
    service.init_db()


def teardown_module():
    if service.DB_PATH.exists():
        service.DB_PATH.unlink()


def test_project_milestone_progress_and_blueprint_history():
    project = service.create_project("Test project", "Test idea")
    project_id = project["id"]

    milestone = service.add_milestone(
        project_id,
        "Build backend",
        "Create endpoints",
        "2099-01-01",
    )
    assert milestone is not None

    updated = service.update_milestone(milestone["id"], status="completed")
    assert updated["status"] == "completed"

    progress = service.get_project_progress(project_id)
    assert progress["progress_percent"] == 100
    assert progress["completed_count"] == 1

    saved = service.save_blueprint(
        "Test idea",
        8,
        4,
        {"project_idea": "Test idea"},
        {"passed": True, "warning_count": 0},
    )
    assert saved["blueprint"]["project_idea"] == "Test idea"
    assert service.get_blueprint(saved["id"])["quality_report"]["passed"] is True
    assert service.list_blueprints(limit=10)[0]["id"] == saved["id"]
