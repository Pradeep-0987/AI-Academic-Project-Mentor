# Outcomes 3 and 4: Documentation Studio and Faculty Dashboard

## Outcome 3: On-demand documentation
The backend exposes:
- `POST /api/documents/generate` with `{ "project_id": 1, "document_type": "synopsis" }`
- Supported document types: `synopsis`, `methodology`, `progress_report`
- `GET /api/documents/projects/{project_id}` to list saved documents
- `GET /api/documents/{document_id}` to read a saved document
- `GET /api/documents/{document_id}/download` to download Markdown

Documents are generated from the saved project, milestone records, and the latest blueprint whose idea exactly matches the project idea. If no blueprint exists, the generator labels missing details as requiring confirmation and must not invent results.

## Outcome 4: Faculty dashboard
The backend exposes:
- `GET /api/faculty/dashboard`
- `GET /api/faculty/projects/{project_id}`

Both require an `X-Faculty-Token` header. Configure a long random token in `ai_engine/.env`:

```env
FACULTY_DASHBOARD_TOKEN=replace_with_a_long_random_secret
```

The faculty UI has a token input and requests the dashboard with this header. The API fails closed with HTTP 503 if the token is not configured, and returns HTTP 401 for a missing or incorrect token.

The dashboard calculates project health from saved milestone statuses and due dates:
- `needs_attention`: one or more blocked or overdue milestones
- `completed`: all milestones are completed and at least one milestone exists
- `not_started`: no milestones yet
- `on_track`: otherwise

Progress is completed milestones divided by total milestones. The summaries are automatically composed from database facts, not presented as predictive AI judgments.

## Run locally
1. Keep your Gemini key in `ai_engine/.env` (never in React code or Git).
2. Configure `FACULTY_DASHBOARD_TOKEN` in the same file.
3. From `ai_engine`, run `python -m pip install -r requirements.txt`.
4. Start the backend with `python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000`.
5. In another terminal, run `npm install` and `npm run dev` from `frontend`.
6. Use the Vite URL printed in the terminal (CORS currently permits ports 5173 and 5174).

## Security and validation notes
This is a local development implementation. Existing student project endpoints do not yet implement individual user authentication/authorization, so do not expose this server publicly. The faculty token is a shared-secret development gate, not a replacement for full account-based role authorization. Generated documentation should be reviewed by the student/supervisor before submission. Live Gemini generation and a production frontend build were not executed in this environment.
