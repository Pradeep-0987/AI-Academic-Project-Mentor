from pydantic import BaseModel, Field

class ResearchPlan(BaseModel):
    research_questions: list[str] = Field(min_length=2)
    related_work_topics: list[str] = Field(min_length=3)
    potential_research_gaps: list[str] = Field(min_length=2)
    search_queries: list[str] = Field(min_length=3)
    source_verification_notes: list[str]
    summary: str
