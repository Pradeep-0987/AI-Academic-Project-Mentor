"""Gemini client with bounded retries for transient API failures."""
import os
import time
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
_RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}

@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your-gemini-api-key" or key.startswith("your-"):
        raise RuntimeError("GEMINI_API_KEY is missing or configured with a placeholder. Configure your local .env.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: python -m pip install -r requirements.txt") from exc
    return genai.Client(api_key=key)

def get_model_name():
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not model:
        raise RuntimeError("GEMINI_MODEL is missing. Set a model available to your account.")
    return model

def generate_text(prompt: str, *, max_attempts: int | None = None) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    attempts = max_attempts or int(os.getenv("GEMINI_MAX_ATTEMPTS", "4"))
    attempts = max(1, min(attempts, 6))
    delays = [2, 4, 8, 16, 30]
    for attempt in range(attempts):
        try:
            response = get_client().models.generate_content(
                model=get_model_name(), contents=prompt
            )
            result = getattr(response, "text", None)
            if not result or not result.strip():
                raise RuntimeError("LLM returned an empty response.")
            return result.strip()
        except Exception as exc:
            code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            message = str(exc).lower()
            if code is None:
                for status in _RETRYABLE_STATUS:
                    if str(status) in message:
                        code = status
                        break
            transient = code in _RETRYABLE_STATUS or any(
                marker in message for marker in ("high demand", "temporarily unavailable", "rate limit", "resource exhausted")
            )
            if not transient or attempt >= attempts - 1:
                raise
            wait = delays[min(attempt, len(delays)-1)]
            print(f"Gemini temporary failure; retrying in {wait}s ({attempt+1}/{attempts-1}).")
            time.sleep(wait)
