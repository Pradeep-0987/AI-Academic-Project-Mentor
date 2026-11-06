import pytest
from ai_engine.agents.common import extract_json

def test_extracts_fenced_json():
    assert extract_json('```json\n{"answer":"ok"}\n```') == {"answer":"ok"}

def test_rejects_non_object():
    with pytest.raises(ValueError): extract_json('[1,2]')
