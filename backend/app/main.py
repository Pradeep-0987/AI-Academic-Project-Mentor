from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.db import models  # noqa: F401 - registers models
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient for local development. Use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok"}
