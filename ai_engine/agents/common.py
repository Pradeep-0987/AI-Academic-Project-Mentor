"""Shared structured-output parsing and validation for all agents."""
import json
import re
from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError
from ai_engine.llm_client import generate_text

T = TypeVar("T", bound=BaseModel)

def extract_json(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Model response did not contain a JSON object.")
        try:
            value = json.loads(text[start:end+1])
        except json.JSONDecodeError as exc:
            raise ValueError("Model response contained malformed JSON.") from exc
    if not isinstance(value, dict):
        raise ValueError("Model response must be a JSON object.")
    return value

def generate_structured(prompt: str, schema: Type[T]) -> T:
    raw = generate_text(prompt)
    data = extract_json(raw)
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Model output failed {schema.__name__} validation: {exc}") from exc
