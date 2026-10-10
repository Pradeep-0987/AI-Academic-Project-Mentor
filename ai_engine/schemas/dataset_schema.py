from pydantic import BaseModel, Field

class DatasetPlan(BaseModel):
    data_requirements: list[str] = Field(min_length=2)
    potential_dataset_sources: list[str] = Field(min_length=2)
    recommended_columns: list[str]
    preprocessing_steps: list[str] = Field(min_length=2)
    data_quality_checks: list[str] = Field(min_length=2)
    leakage_risks: list[str]
    summary: str
