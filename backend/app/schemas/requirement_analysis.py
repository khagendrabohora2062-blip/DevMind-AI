from datetime import datetime

from pydantic import BaseModel


class RequirementAnalysisCreate(BaseModel):
    requirement_id: int
    summary: str | None = None
    functional_requirements: str | None = None
    non_functional_requirements: str | None = None
    assumptions: str | None = None
    risks: str | None = None


class RequirementAnalysisResponse(BaseModel):
    id: int
    requirement_id: int
    summary: str | None
    functional_requirements: str | None
    non_functional_requirements: str | None
    assumptions: str | None
    risks: str | None
    created_at: datetime

    class Config:
        from_attributes = True