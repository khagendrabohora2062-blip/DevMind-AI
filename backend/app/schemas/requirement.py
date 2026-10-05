from datetime import datetime

from pydantic import BaseModel


class RequirementCreate(BaseModel):
    project_id: int
    title: str
    description: str
    priority: str = "medium"


class RequirementResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True