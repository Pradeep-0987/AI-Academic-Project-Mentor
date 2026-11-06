import pytest
from ai_engine.workflows.blueprint_graph import generate_blueprint

def test_empty_idea_rejected_before_api_call():
    with pytest.raises(ValueError):
        generate_blueprint("", 8, 4)

def test_invalid_duration_rejected_before_api_call():
    with pytest.raises(ValueError):
        generate_blueprint("AI academic project", 0, 4)
