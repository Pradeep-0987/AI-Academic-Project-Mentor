import json
from google import genai
from app.core.config import settings

def ask_gemini(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured in .env")
    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(model=settings.gemini_model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    return text.strip()

def generate_blueprint(title: str, idea: str, academic_level: str, constraints: str | None) -> dict:
    prompt = f"""
You are an academic project mentor. Create a practical, honest project blueprint.
Return valid JSON only with keys: project_title, problem_statement, objectives (array),
scope, proposed_technology (array), methodology (array), dataset_plan, architecture,
milestones (array of objects with title, description, suggested_duration),
testing_and_evaluation (array), risks (array), documentation_sections (array), viva_questions (array).
Do not claim that models were trained or results achieved unless provided as facts.
Academic level: {academic_level}
Title: {title}
Idea: {idea}
Constraints: {constraints or "Not specified"}
"""
    raw = ask_gemini(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Preserve model output instead of pretending malformed output is valid JSON.
        return {"project_title": title, "raw_blueprint": raw, "format_warning": "Model response was not valid JSON."}

def mentor_reply(message: str, project_context: str = "") -> str:
    return ask_gemini(
        "You are a supportive academic project mentor. Give clear, practical steps, "
        "avoid inventing completed work or fabricated metrics.\n"
        f"Project context: {project_context or 'No project context supplied'}\n"
        f"Student question: {message}"
    )

def generate_document(document_type: str, title: str, idea: str, blueprint: str | None, extra: str | None) -> str:
    labels = {
        "synopsis": "an academic project synopsis with abstract, problem statement, objectives, scope, methodology, tools, expected outcome and references placeholders",
        "methodology": "a detailed methodology chapter with workflow, data preparation, algorithms, evaluation plan and limitations",
        "progress_report": "a progress report separating completed work, current work, blockers and next steps; do not fabricate progress",
    }
    return ask_gemini(
        f"Write {labels[document_type]}. Use formal academic language and Markdown. "
        "Do not fabricate results, citations, or completed work. Clearly label unknown details as placeholders.\n"
        f"Project title: {title}\nIdea: {idea}\nBlueprint: {blueprint or 'Not yet generated'}\n"
        f"Extra instructions: {extra or 'None'}"
    )
