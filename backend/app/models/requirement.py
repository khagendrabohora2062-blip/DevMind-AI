from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(50),
        default="medium"
    )

    status = Column(
        String(50),
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )