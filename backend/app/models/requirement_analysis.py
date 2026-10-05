from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class RequirementAnalysis(Base):
    __tablename__ = "requirement_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    requirement_id = Column(
        Integer,
        ForeignKey("requirements.id"),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    functional_requirements = Column(
        Text,
        nullable=True
    )

    non_functional_requirements = Column(
        Text,
        nullable=True
    )

    assumptions = Column(
        Text,
        nullable=True
    )

    risks = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )