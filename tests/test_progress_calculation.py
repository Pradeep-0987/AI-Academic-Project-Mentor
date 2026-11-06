import pytest
from ai_engine.mentor.progress_analyzer import calculate_completion_percentage

def test_percentage():
    assert calculate_completion_percentage(3, 4) == 75.0

def test_zero_tasks():
    assert calculate_completion_percentage(0, 0) == 0.0

def test_invalid_count():
    with pytest.raises(ValueError):
        calculate_completion_percentage(5, 4)
