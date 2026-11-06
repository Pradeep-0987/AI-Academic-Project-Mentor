# NEXTSTEP AI — Academic Project Planning & Mentorship Platform

**Product category:** AI-powered academic project planning, tracking, and mentorship.

**Every Step Builds Success.** NEXTSTEP AI helps students transform ideas into successful projects through AI-powered planning, dynamic milestones, intelligent progress tracking, risk analysis, and personalized mentorship. It guides students from initial planning to final implementation. **Plan Smart. Build Better. Achieve More.**

This repository contains the NEXTSTEP AI platform's React frontend, FastAPI backend, and AI subsystem. The backend in `backend/` owns authenticated APIs, authorization, and persistence; the frontend in `frontend/` consumes those APIs. See [backend/README.md](backend/README.md) for setup, migrations, and endpoint contracts.

## AI capabilities

1. **Multi-agent project blueprint**: feasibility, scope, technology recommendations, week-wise plan, risk assessment, and deterministic quality checks orchestrated with LangGraph.
2. **Skill-fit assessment**: project-specific required skills, gaps, and a learning sequence from self-reported skills.
3. **Conversational mentor**: project-aware chat, conversation history, next actions, evidence-aware responses, and optional retrieved knowledge snippets.
4. **Local knowledge retrieval (RAG foundation)**: chunk text/Markdown/CSV/JSON/Python/PDF/DOCX files, retrieve relevant passages locally, and pass them to the mentor. This is lexical retrieval, not a trained embedding model; a vector database can replace it later.
5. **Progress analysis**: deterministic task completion/overdue metrics plus LLM-generated priorities, blockers, and proposed schedule adjustments.
6. **Weekly check-in coach**: reflection, next-week priorities, support needs, and suggested plan adjustments.
7. **Plan revision proposals**: compares current plan with progress evidence and returns a proposed revision; it never applies it automatically.
8. **Academic document generation**: synopsis, methodology, progress report, TODOs for missing evidence, and factual claims to verify. The prompt prohibits invented results/citations.
9. **Faculty portfolio summaries**: deterministic project health indicators and an LLM-written summary of supplied project records.
10. **Reliability**: shared structured JSON parsing, Pydantic validation for agents, bounded retries for transient Gemini errors, tests that don't require a live API key.

## Setup — Windows PowerShell

Use Python 3.11 or 3.12 for broad dependency compatibility.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with a new Gemini API key and a model ID available in your Google AI Studio account. If a key was exposed, revoke it first. Keep `.env` out of Git.

## Tests

From the project root (the directory containing `ai_engine`), run:

```powershell
python -m pytest -q
```

The unit tests use no live Gemini API. A deprecation warning from a third-party dependency does not necessarily indicate a project test failure.

## Run the live blueprint generator

```powershell
$env:PYTHONPATH = (Get-Location).Path
python examples/generate_blueprint.py
```

The result is saved to `output/blueprint.json`. Each blueprint agent makes a model call, so temporary model overload or quota can still cause failure despite bounded retries.

## Integration example

```python
from ai_engine.service import (
    generate_blueprint, chat_with_mentor, analyse_progress,
    review_weekly_checkin, propose_plan_adjustment, generate_document,
    summarize_faculty_portfolio, assess_skill_fit, LocalKnowledgeBase,
)

blueprint = generate_blueprint(
    "Email spam detection", duration_weeks=8, team_size=3,
    skills=["Python", "basic machine learning"]
)

knowledge = LocalKnowledgeBase()
knowledge.add_text("project_notes.md", "Dataset notes and project requirements...")
retrieved = knowledge.search("email spam dataset", top_k=3)
reply = chat_with_mentor(
    "What should we implement first?",
    project_context={"blueprint": blueprint}, history=[],
    retrieved_context=retrieved,
)

progress = analyse_progress(
    plan=blueprint["planning"],
    progress={"tasks": [{"title": "Data cleaning", "status": "completed"}]},
)
checkin = review_weekly_checkin(
    {"blueprint": blueprint}, ["Created baseline dataset loader"],
    blockers=["Dataset labels need review"], confidence=3,
)
proposal = propose_plan_adjustment(blueprint["planning"], progress)
doc = generate_document("progress_report", {
    "blueprint": blueprint, "reported_progress": progress,
    "checkin": checkin,
})
portfolio = summarize_faculty_portfolio([
    {"id": 1, "name": "Email spam detection", "tasks": [
        {"status": "completed"}, {"status": "pending"}
    ]}
])
skill_fit = assess_skill_fit("Email spam detection", ["Python"], "beginner")
```

The functions are Python interfaces, not HTTP endpoints. The backend team should wrap them in its existing API routes, run blocking LLM calls in a threadpool for async FastAPI routes, validate the current user's access to every project, and persist results only after explicit application/approval.

## Recommended backend route mapping

| Route purpose | AI function |
|---|---|
| Generate blueprint | `generate_blueprint` |
| Mentor chat | `chat_with_mentor` |
| Analyse progress | `analyse_progress` |
| Weekly check-in | `review_weekly_checkin` |
| Suggest revised plan | `propose_plan_adjustment` |
| Generate synopsis/methodology/progress report | `generate_document` |
| Faculty portfolio | `summarize_faculty_portfolio` |
| Skill profile | `assess_skill_fit` |

## Integration boundaries and production checklist

- **Included here:** AI agents, orchestration, structured prompts/output parsing, local retrieval, deterministic metrics, generated document content, integration facade, tests and instructions.
- **Implemented in the repository's backend/frontend:** login/session security, database models, project ownership authorization, project and milestone APIs, project-aware mentor chat, and student workspace UI. Production document storage/download endpoints, background job processing, and hosting remain deployment-level work.
- Model output is probabilistic. The quality validator catches structural/timeline issues, not factual truth. Human review is required before submitting generated academic work.
- Plan changes are proposals only; do not auto-overwrite the student's plan.
- Faculty summaries depend on the correctness and completeness of supplied project records.
- The local knowledge base is in-memory and lexical. It is not persistent, uses lexical rather than semantic matching and may not extract text from scanned/image-only PDFs. Extract text securely in the backend before ingestion or replace with a vetted vector store.
- Before production: add authentication/authorization at API boundaries, request limits, secrets management, audit logs, monitoring, privacy controls, integration tests, and evaluation on representative project ideas.
