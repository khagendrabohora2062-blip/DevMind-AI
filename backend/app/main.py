from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base

from app.models.user import User
from app.models.project import Project
from app.models.requirement import Requirement
from app.models.requirement_analysis import RequirementAnalysis

from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.projects import router as project_router
from app.routers.requirement_analysis import router as requirement_analysis_router
from app.routers.requirements import router as requirement_router


# Create database tables
Base.metadata.create_all(bind=engine)


# FastAPI application
app = FastAPI(
    title="DevMind AI",
    description="AI-Powered Autonomous Software Engineering Platform",
    version="1.0.0"
)


# Register routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(requirement_router)
app.include_router(requirement_analysis_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to DevMind AI",
        "status": "running"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Database connection test
@app.get("/db-test")
def database_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

        return {
            "database": "connected",
            "result": value
        }

    except Exception as e:
        return {
            "database": "connection_failed",
            "error": str(e)
        }