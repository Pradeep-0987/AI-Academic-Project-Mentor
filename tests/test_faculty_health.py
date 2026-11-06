from ai_engine.mentor.faculty_summaries import calculate_project_health

def test_project_health_is_deterministic():
    result=calculate_project_health({"id":3,"name":"Demo","tasks":[{"status":"completed"},{"status":"pending","is_overdue":True}]})
    assert result["completion_percentage"] == 50.0
    assert result["overdue_tasks"] == 1
    assert result["health_status"] == "At risk"
