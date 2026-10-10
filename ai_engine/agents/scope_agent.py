
import os

from google import genai

from schemas.scope_schema import ProjectScope


class ScopeAgent:
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

    def generate_scope(self, project_idea: str) -> ProjectScope:
        if not project_idea.strip():
            raise ValueError("Project idea cannot be empty.")

        prompt = f"""
You are an academic software project scope analyst.

Create a realistic scope for this student project:
{project_idea}

Requirements:
- Define a manageable minimum viable product (MVP).
- Separate required features from future enhancements.
- Include measurable success criteria.
- Do not claim that features have already been implemented.
- State assumptions explicitly.
- Return data matching the requested structured schema.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ProjectScope,
            },
        )

        if not response.text:
            raise RuntimeError("The AI returned an empty response.")

        return ProjectScope.model_validate_json(response.text)
