import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProfilePayload(BaseModel):
    institution: str = Field(min_length=2, max_length=255)
    department: str = Field(min_length=2, max_length=255)
    semester: str = Field(min_length=1, max_length=100)
    graduation_year: int = Field(ge=2020, le=2040)


class SkillItem(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: str = "Intermediate"
    isCustom: bool = False


class SkillsAssessmentPayload(BaseModel):
    skills: list[SkillItem] = []
    interests: list[str] = []


class StudentFullDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    institution: str | None = None
    department: str | None = None
    semester: str | None = None
    graduation_year: int | None = None
    onboarding_completed: bool = False
    skills: list[dict] = []
    interests: list[str] = []
