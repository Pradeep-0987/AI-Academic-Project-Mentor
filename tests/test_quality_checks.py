from ai_engine.workflows.quality_checks import validate_blueprint_consistency

def test_valid_blueprint_passes():
    b = {"feasibility": {"x": 1}, "scope": {"x": 1}, "technology": {"x": 1},
         "planning": {"total_duration_weeks": 4, "phases": [
             {"phase_name": "Build", "start_week": 1, "duration_weeks": 4,
              "tasks": ["Implement"], "deliverables": ["Prototype"]}]},
         "risk": {"risks": [{"risk": "Delay", "mitigation": "Add buffer"}]}}
    r = validate_blueprint_consistency(b, 4)
    assert r["valid"] is True
    assert r["errors"] == []

def test_duration_mismatch_fails():
    b = {"feasibility": {"x": 1}, "scope": {"x": 1}, "technology": {"x": 1},
         "planning": {"total_duration_weeks": 5, "phases": []}, "risk": {"risks": []}}
    r = validate_blueprint_consistency(b, 4)
    assert not r["valid"]
