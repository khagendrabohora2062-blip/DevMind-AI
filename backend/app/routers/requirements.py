from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.requirement import Requirement
from app.models.project import Project
from app.schemas.requirement import (
    RequirementCreate,
    RequirementResponse
)
from app.security import get_current_user


router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"]
)


@router.post(
    "/",
    response_model=RequirementResponse,
    status_code=201
)
def create_requirement(
    requirement_data: RequirementCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == requirement_data.project_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_requirement = Requirement(
        project_id=requirement_data.project_id,
        title=requirement_data.title,
        description=requirement_data.description,
        priority=requirement_data.priority
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement


@router.get(
    "/project/{project_id}",
    response_model=list[RequirementResponse]
)
def get_project_requirements(
    project_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    requirements = (
        db.query(Requirement)
        .filter(
            Requirement.project_id == project_id
        )
        .order_by(Requirement.id.desc())
        .all()
    )

    return requirements


@router.get(
    "/{requirement_id}",
    response_model=RequirementResponse
)
def get_requirement(
    requirement_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    requirement = (
        db.query(Requirement)
        .join(
            Project,
            Requirement.project_id == Project.id
        )
        .filter(
            Requirement.id == requirement_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )

    return requirement