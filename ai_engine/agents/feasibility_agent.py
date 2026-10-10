
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import ValidationError

from schemas.feasibility_schema import ProjectFeasibility


# Load ai_engine/.env regardless of the terminal's working directory.
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)


class FeasibilityAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-flash-lite",
        )

        if not api_key:
            raise RuntimeError(
                f"GEMINI_API_KEY is missing. Checked: {ENV_FILE}"
            )

        self.client = genai.Client(api_key=api_key)

    def evaluate(self, project_idea: str) -> ProjectFeasibility:
        if not project_idea.strip():
            raise ValueError("Project idea cannot be empty.")

        prompt = f"""
You are a careful academic software project feasibility analyst.

Evaluate the following student project idea:
{project_idea}

Assess its feasibility for a student team. Do not invent completed
experiments, results, datasets, or achievements.

Return a structured assessment matching the supplied schema.
Be realistic about complexity, resources, and risks.
Clearly identify assumptions where information is missing.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ProjectFeasibility,
            },
        )

        if not response.text:
            raise RuntimeError("The AI returned an empty response.")

        try:
            return ProjectFeasibility.model_validate_json(response.text)
        except ValidationError as exc:
            raise RuntimeError(
                "The AI response did not match the required schema."
            ) from exc
