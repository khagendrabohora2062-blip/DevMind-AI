from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.security import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# Create Project
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=201
)
def create_project(
    project_data: ProjectCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# Get My Projects
@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def get_my_projects(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = (
        db.query(Project)
        .filter(Project.owner_id == current_user.id)
        .order_by(Project.id.desc())
        .all()
    )

    return projects


# Get Single Project
@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
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

    return project