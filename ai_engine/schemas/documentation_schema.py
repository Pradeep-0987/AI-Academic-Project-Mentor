from pydantic import BaseModel, Field

class DocumentationPlan(BaseModel):
    report_chapters: list[str] = Field(min_length=5)
    presentation_slides: list[str] = Field(min_length=5)
    viva_questions: list[str] = Field(min_length=5)
    viva_answer_guidance: list[str]
    demo_checklist: list[str] = Field(min_length=3)
    academic_integrity_notes: list[str]
    summary: str
