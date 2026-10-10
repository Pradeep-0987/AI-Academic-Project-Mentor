
import os
import time

from google import genai

from schemas.risk_schema import RiskAssessment


class RiskAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL", "gemini-3.1-flash-lite"
        )

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing.")

        self.client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 120000},
        )

    def assess(
        self,
        project_idea: str,
        project_scope: str = "",
        duration_weeks: int = 8,
    ) -> RiskAssessment:

        if not project_idea.strip():
            raise ValueError("Project idea cannot be empty.")

        if not 1 <= duration_weeks <= 52:
            raise ValueError(
                "Duration must be between 1 and 52 weeks."
            )

        prompt = f"""
Assess risks for this student software project.

PROJECT IDEA: {project_idea}
PROJECT SCOPE: {project_scope or "Not supplied"}
DURATION: {duration_weeks} weeks

Identify realistic risks related to data quality, technical complexity,
AI evaluation, integration, team capacity, deadlines, security, and privacy
where relevant.

For each risk, provide its title, description, category, likelihood,
impact, mitigation actions, contingency plan, and responsible role.

Also provide an overall risk level, recommendations, and assumptions.
Do not claim that risks have occurred or that mitigations are complete.
Return concise JSON matching the required schema.
"""

        response = None

        for attempt in range(3):
            try:
                print(
                    f"Generating risk assessment "
                    f"({attempt + 1}/3)..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": RiskAssessment,
                    },
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                break

            except Exception as error:
                message = str(error).upper()

                temporary = any(
                    marker in message
                    for marker in (
                        "503",
                        "UNAVAILABLE",
                        "429",
                        "RESOURCE_EXHAUSTED",
                        "500",
                        "502",
                        "504",
                        "DEADLINE_EXCEEDED",
                    )
                )

                if not temporary or attempt == 2:
                    raise RuntimeError(
                        f"Risk assessment failed after "
                        f"{attempt + 1} attempt(s): {error}"
                    ) from error

                delay = 3 * (attempt + 1)
                print(
                    f"Temporary API issue. Retrying in {delay} seconds..."
                )
                time.sleep(delay)

        if response is None or not response.text:
            raise RuntimeError(
                "Unable to generate risk assessment."
            )

        return RiskAssessment.model_validate_json(response.text)
