from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.requirement import Requirement
from app.models.requirement_analysis import RequirementAnalysis
from app.models.project import Project
from app.schemas.requirement_analysis import (
    RequirementAnalysisCreate,
    RequirementAnalysisResponse
)
from app.security import get_current_user


router = APIRouter(
    prefix="/requirement-analysis",
    tags=["Requirement Analysis"]
)


@router.post(
    "/",
    response_model=RequirementAnalysisResponse,
    status_code=201
)
def create_analysis(
    analysis_data: RequirementAnalysisCreate,
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
            Requirement.id == analysis_data.requirement_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )

    analysis = RequirementAnalysis(
        requirement_id=analysis_data.requirement_id,
        summary=analysis_data.summary,
        functional_requirements=analysis_data.functional_requirements,
        non_functional_requirements=analysis_data.non_functional_requirements,
        assumptions=analysis_data.assumptions,
        risks=analysis_data.risks
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@router.get(
    "/requirement/{requirement_id}",
    response_model=list[RequirementAnalysisResponse]
)
def get_requirement_analysis(
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

    analyses = (
        db.query(RequirementAnalysis)
        .filter(
            RequirementAnalysis.requirement_id == requirement_id
        )
        .order_by(RequirementAnalysis.id.desc())
        .all()
    )

    return analyses