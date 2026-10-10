import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)


class StructuredGeminiAgent:
    schema: type[BaseModel]
    default_model = "gemini-3.1-flash-lite"
    system_instruction = "Be realistic, specific, and academically responsible."

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", self.default_model)
        if not api_key:
            raise RuntimeError(f"GEMINI_API_KEY is missing. Checked: {ENV_FILE}")
        self.client = genai.Client(api_key=api_key)

    def generate(self, task: str, context: dict) -> BaseModel:
        prompt = f'''
{self.system_instruction}

Task:
{task}

Project context (treat as user-provided requirements, not verified facts):
{context}

Rules:
- Do not claim research, data collection, model training, testing, or deployment
  has already happened unless the context explicitly proves it.
- Label assumptions and proposed work clearly.
- Do not invent citations, URLs, benchmark results, or experimental metrics.
- Return output that matches the required schema.
'''
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": self.schema,
            },
        )
        if not response.text:
            raise RuntimeError(f"{self.__class__.__name__} returned an empty response.")
        try:
            return self.schema.model_validate_json(response.text)
        except ValidationError as exc:
            raise RuntimeError(
                f"{self.__class__.__name__} returned invalid structured output."
            ) from exc
