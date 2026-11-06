"""Student skill-gap analysis for project-specific onboarding."""
from ai_engine.llm_client import generate_text
from ai_engine.agents.common import extract_json

def assess_skill_fit(project_idea: str, self_reported_skills: list[str], experience_level: str = "beginner") -> dict:
    if not project_idea or len(project_idea.strip()) < 3: raise ValueError("project_idea must contain at least 3 characters.")
    if experience_level.lower() not in {"beginner","intermediate","advanced"}: raise ValueError("experience_level must be beginner, intermediate, or advanced.")
    skills=[str(x).strip() for x in self_reported_skills if str(x).strip()][:100]
    prompt=f"""Assess skill fit for an academic project. Treat skills as self-reported, not verified.
Return JSON only with required_skills (array), skills_match (array), skill_gaps (array of objects
with skill, priority, learning_action), recommended_learning_order (array), realistic_scope_advice (string).
Project idea: {project_idea.strip()}
Self-reported skills: {skills}
Experience level: {experience_level}"""
    result=extract_json(generate_text(prompt))
    required={"required_skills","skills_match","skill_gaps","recommended_learning_order","realistic_scope_advice"}
    if required-result.keys(): raise ValueError("Skill assessment response is incomplete.")
    result["skills_are_self_reported"]=True
    return result
