"""Stable import facade for backend integration."""
from ai_engine.workflows.blueprint_graph import generate_blueprint
from ai_engine.mentor.chat_service import chat_with_mentor
from ai_engine.mentor.progress_analyzer import analyse_progress, calculate_progress_metrics
from ai_engine.mentor.checkin_service import review_weekly_checkin
from ai_engine.mentor.faculty_summaries import summarize_faculty_portfolio, calculate_project_health
from ai_engine.workflows.plan_adjustment import propose_plan_adjustment
from ai_engine.documents.document_generator import generate_document
from ai_engine.skill_assessment import assess_skill_fit
from ai_engine.knowledge.retriever import LocalKnowledgeBase

__all__ = [
    "generate_blueprint", "chat_with_mentor", "analyse_progress",
    "calculate_progress_metrics", "review_weekly_checkin",
    "summarize_faculty_portfolio", "calculate_project_health",
    "propose_plan_adjustment", "generate_document", "assess_skill_fit",
    "LocalKnowledgeBase",
]
