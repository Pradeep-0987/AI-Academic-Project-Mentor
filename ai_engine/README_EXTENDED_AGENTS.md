# Extended AI agents

The workflow now contains ten structured-output agents:
1. Feasibility
2. Scope
3. Technology
4. Planning
5. Risk assessment
6. Research and literature planning
7. Dataset and data-quality planning
8. System architecture
9. Testing and evaluation planning
10. Documentation and viva planning

## Setup (Windows PowerShell)

From the `ai_engine` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Put your Gemini key only in `ai_engine/.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

Run the API:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs`.

## Important notes

- The full workflow now makes ten sequential Gemini model calls. It will take longer and use more API quota than the earlier five-agent workflow.
- Research and dataset agents create plans and search suggestions; they do not browse the web or download datasets.
- Testing agent creates test plans; it does not execute project tests.
- Documentation agent provides outlines and viva practice, not a finished verified report.
- Model output remains AI-generated and should be reviewed by the student and supervisor.
- Do not commit `.env`, API keys, or uploaded datasets.
- The quality report is heuristic and does not prove that every claim is true.

## Validation status

Python syntax compilation was checked for the supplied source files. Full integration tests and live Gemini calls were not run in this build environment. Run your existing tests in the local virtual environment after installing requirements.

## Conversational mentoring, progress tracking, and milestones

The API now includes a Gemini-backed conversational mentor and local SQLite persistence. On first import, `mentor_service.py` creates `data/mentor.db` (the database is generated at runtime and should not be committed).

### Endpoints

- `GET /api/mentor/projects` — list tracked projects and progress counts.
- `POST /api/mentor/projects` — create a tracked project with `name`, `idea`, optional `target_date`, and optional initial `milestones`.
- `GET /api/mentor/projects/{project_id}` — fetch project details, milestones, and recent stored conversation.
- `POST /api/mentor/projects/{project_id}/milestones` — add a milestone.
- `PATCH /api/mentor/milestones/{milestone_id}` — update milestone status (`pending`, `in_progress`, `blocked`, `completed`) or details.
- `POST /api/mentor/chat` — send a conversational message. Request fields: `message`, optional `project_id`, optional recent `history`.

Example chat request:

```json
{
  "message": "I am blocked on cleaning missing values. What should I do next?",
  "project_id": 1,
  "history": []
}
```

Project-bound chat messages are stored in SQLite. For general mentoring without a project ID, the client should send the recent conversation history because those messages are not persisted. This development version is intended for local use: it does not include user authentication, per-user data isolation, backups, or production deployment hardening. Do not expose it publicly until those are added.
