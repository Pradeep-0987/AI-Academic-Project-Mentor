"""Evidence-grounded academic document generation."""
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

DOCUMENT_INSTRUCTIONS = {
    "synopsis": "Write title, abstract, problem statement, objectives, scope, methodology, technology, expected outcomes and references-to-be-verified section.",
    "methodology": "Write system approach, architecture/workflow, data needs, algorithms, implementation stages, evaluation protocol and limitations.",
    "progress_report": "Write objectives, completed work (only evidence supplied), work in progress, pending tasks, blockers, corrective actions, next steps and evidence gaps.",
}

def generate_document(document_type: str, project_context: dict) -> dict:
    if document_type not in DOCUMENT_INSTRUCTIONS:
        raise ValueError("document_type must be synopsis, methodology, or progress_report.")
    if not isinstance(project_context,dict): raise ValueError("project_context must be a dictionary.")
    prompt=f"""Generate a professional academic document in Markdown. Use only facts in the
context. Never fabricate citations, results, accuracy metrics, experiments, completed tasks,
student approvals, or references. Mark unknowns as [TODO: information needed]. Clearly separate
proposed methodology from work actually completed. Return JSON only with title, document_type,
content_markdown, missing_information (array), factual_claims_to_verify (array).
Requested type: {document_type}
Instructions: {DOCUMENT_INSTRUCTIONS[document_type]}
Context: {project_context}"""
    result=extract_json(generate_text(prompt))
    required=("title","document_type","content_markdown","missing_information")
    if any(k not in result for k in required): raise ValueError("Document generator response is missing required fields.")
    if result["document_type"] != document_type: raise ValueError("Returned document_type does not match request.")
    if not isinstance(result["content_markdown"],str) or not result["content_markdown"].strip(): raise ValueError("Document content is empty.")
    result.setdefault("factual_claims_to_verify",[])
    return result
