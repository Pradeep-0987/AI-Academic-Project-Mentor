# NEXTSTEP AI Backend

Backend services for NEXTSTEP AI — an AI-powered academic project planning, tracking, and mentorship platform. Existing API routes and stored project/user records remain unchanged.

## Setup

From the `backend` directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Database (PostgreSQL / Supabase)

Create a project in [Supabase](https://supabase.com). In your Supabase Project Settings -> Database, copy your Connection String (URI).

Set `DATABASE_URL` in `.env`:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

For an existing database, back it up and apply the additive project metadata migration before starting
the updated application. Existing project records and users are retained; new metadata columns are
nullable except for `duration_weeks`, which is backfilled to 8 weeks for old projects.

```powershell
alembic upgrade head
python -m uvicorn app.main:app --reload
python -m pytest
```

`Base.metadata.create_all()` creates missing tables, but does not apply schema changes to existing
tables. Run `alembic upgrade head` whenever deploying a database that already contains projects.

## Project workspace APIs

- `POST /api/projects` creates a project and generates a blueprint using the submitted `duration_weeks`.
  The web form requires title, description, domain, department, technology stack, and a 1–52 week
  duration. `team_size` and `guide_name` may be omitted or null.
- `GET /api/projects` returns only the authenticated student's projects, including progress derived
  from stored milestone statuses and available due dates.
- `GET /api/projects/{project_id}/blueprint` returns the project's feasibility, scope, technology,
  risks, and weekly plan.
- `PATCH /api/projects/{project_id}/milestones/{week_number}` accepts
  `{"status":"pending"|"in_progress"|"completed"}` and persists the milestone status.
- `POST /api/projects/{project_id}/chat` accepts a question and recent conversation history. It
  passes only that student's project and saved blueprint to the AI mentor.

AI blueprint and chat responses require the root AI-engine dependencies and a configured Gemini API
key. If automatic blueprint generation fails, the project record remains available and the UI offers
an authenticated retry action.

## API examples

Register:

```powershell
curl.exe -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" -d "{\"name\":\"Test Student\",\"email\":\"student@example.com\",\"password\":\"password123\"}"
```

Login:

```powershell
curl.exe -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"student@example.com\",\"password\":\"password123\"}"
```

Use the returned access token:

```powershell
curl.exe http://localhost:8000/api/auth/me -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
