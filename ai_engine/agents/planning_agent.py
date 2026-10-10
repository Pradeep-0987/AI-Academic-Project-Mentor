
import os
import time

from google import genai

from schemas.planning_schema import ProjectPlan


class PlanningAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL", "gemini-3.8-flash"
        )

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        self.client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 120000},
        )

    def create_plan(
        self,
        project_idea: str,
        duration_weeks: int = 8,
        team_size: int = 6,
    ) -> ProjectPlan:

        if not project_idea.strip():
            raise ValueError("Project idea cannot be empty.")

        if not 1 <= duration_weeks <= 52:
            raise ValueError(
                "Duration must be between 1 and 52 weeks."
            )

        if not 1 <= team_size <= 20:
            raise ValueError(
                "Team size must be between 1 and 20."
            )

        available_days = duration_weeks * 7

        prompt = f"""
Create a practical academic software project schedule.

Project: {project_idea}
Available duration: {duration_weeks} weeks ({available_days} days)
Team size: {team_size}

Return a concise structured plan with:
1. Setup and requirements
2. Core implementation
3. Integration
4. Testing and bug fixing
5. Documentation and final demo

You may combine or subdivide these phases as appropriate.

Rules:
- Use calendar days for phase durations.
- Every phase must have a positive duration.
- Sum of phase durations must equal total_duration_days.
- Total duration must not exceed {available_days} days.
- Include tasks, deliverables, dependencies, milestones,
  assumptions, and schedule risks.
- Dependencies must refer to actual phase names.
- Do not claim work has already been completed.
- Keep the response concise.
"""

        response = None

        for attempt in range(3):
            try:
                print(
                    f"Generating project plan "
                    f"({attempt + 1}/3)..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": ProjectPlan,
                    },
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                break

            except Exception as error:
                error_text = str(error).upper()

                temporary_error = any(
                    marker in error_text
                    for marker in (
                        "503",
                        "UNAVAILABLE",
                        "429",
                        "RESOURCE_EXHAUSTED",
                        "500",
                        "INTERNAL",
                        "502",
                        "504",
                        "DEADLINE_EXCEEDED",
                    )
                )

                if not temporary_error or attempt == 2:
                    raise RuntimeError(
                        "Project planning failed after "
                        f"{attempt + 1} attempt(s): {error}"
                    ) from error

                delay = 3 * (attempt + 1)

                print(
                    f"Temporary API issue. Retrying in "
                    f"{delay} seconds..."
                )
                time.sleep(delay)

        if response is None or not response.text:
            raise RuntimeError(
                "Unable to generate a project plan."
            )

        plan = ProjectPlan.model_validate_json(response.text)

        calculated_days = sum(
            phase.duration_days for phase in plan.phases
        )

        if calculated_days != plan.total_duration_days:
            raise ValueError(
                "Invalid plan: total_duration_days must equal "
                "the sum of all phase durations."
            )

        if plan.total_duration_days > available_days:
            raise ValueError(
                f"Plan exceeds the available {available_days} days."
            )

        return plan
