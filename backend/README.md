# AI Academic Project Mentor — Separate Backend

A separate FastAPI backend with PostgreSQL persistence, Gemini integration, project/milestone tracking, document generation, and token-protected faculty endpoints.

## Requirements
- Python 3.11 recommended
- PostgreSQL 15+ running locally
- Gemini API key (optional for non-AI CRUD endpoints)

## 1. Create database
Open pgAdmin Query Tool or `psql` and run:
```sql
CREATE DATABASE academic_mentor;
```
Use a PostgreSQL role/password that exists on your machine. Put the connection string in `.env`.

## 2. Install and configure
PowerShell, from this folder:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and set `DATABASE_URL`, `GEMINI_API_KEY`, and a private faculty token. Generate a token with:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Do not paste secrets into chat or commit `.env`.

## 3. Start API
```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
On startup, SQLAlchemy creates the initial tables. Open `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/health`.

## API overview
- `POST /api/projects` create a project
- `GET /api/projects` list projects
- `GET /api/projects/{project_id}` get project with milestones
- `PATCH /api/projects/{project_id}` update project status/details
- `POST /api/projects/{project_id}/milestones` add milestone
- `PATCH /api/milestones/{milestone_id}` update milestone
- `POST /api/ai/generate-blueprint` generate a blueprint with Gemini
- `POST /api/mentor/chat` ask the mentor
- `POST /api/documents/generate` create synopsis/methodology/progress report text and store it
- `GET /api/documents/projects/{project_id}` list generated documents
- `GET /api/documents/{document_id}` get a generated document
- `GET /api/faculty/dashboard` faculty overview (Bearer token required)
- `GET /api/faculty/projects/{project_id}` faculty project detail (Bearer token required)

## Important
This is a development-ready foundation, not production authentication. The faculty token is a shared secret, not per-user login. Before public deployment, add user accounts, hashed passwords, role-based access, migrations (Alembic), rate limiting, audit logs, and deployment secret management. Live Gemini calls need a valid API key and internet access.
