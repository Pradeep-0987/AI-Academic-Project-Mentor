from pydantic import BaseModel, Field

class ArchitecturePlan(BaseModel):
    architecture_style: str
    components: list[str] = Field(min_length=3)
    api_contracts: list[str]
    data_entities: list[str]
    data_flow: list[str] = Field(min_length=2)
    security_controls: list[str] = Field(min_length=2)
    deployment_plan: list[str]
    architecture_diagram_mermaid: str
    assumptions: list[str]
