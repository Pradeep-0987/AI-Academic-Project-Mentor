
from pydantic import BaseModel, Field


class TechnologyRecommendation(BaseModel):
    frontend: list[str] = Field(min_length=1)
    backend: list[str] = Field(min_length=1)
    database: list[str] = Field(min_length=1)
    ai_ml: list[str] = Field(min_length=1)
    deployment: list[str] = Field(min_length=1)
    development_tools: list[str] = Field(min_length=1)
    alternatives: list[str] = Field(min_length=1)
    rationale: str
    limitations: list[str]
