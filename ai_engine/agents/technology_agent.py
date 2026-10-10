
import os

from google import genai

from schemas.technology_schema import TechnologyRecommendation


class TechnologyAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL", "gemini-3.8-flash"
        )

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing.")

        self.client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 60000},
        )

    def recommend(
        self, project_idea: str, project_scope: str = ""
    ) -> TechnologyRecommendation:
        if not project_idea.strip():
            raise ValueError("Project idea cannot be empty.")

        prompt = f"""
You are a software architecture and technology advisor
for academic projects.

PROJECT IDEA:
{project_idea}

PROJECT SCOPE:
{project_scope or "No detailed scope supplied."}

Recommend a practical technology stack suitable for a student team.
Consider implementation effort, maintainability, cost, and integration.

For an AI retail forecasting project, consider Python, pandas,
scikit-learn, statsmodels, FastAPI, React, and PostgreSQL where suitable.
Do not claim that any technology has already been implemented.
Do not invent benchmark results or guarantee performance.

Return JSON matching the requested schema.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": TechnologyRecommendation,
            },
        )

        if not response.text:
            raise RuntimeError("The AI returned an empty response.")

        return TechnologyRecommendation.model_validate_json(
            response.text
        )
