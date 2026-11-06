from contextlib import asynccontextmanager
from pathlib import Path
import sys

# Ensure root (containing ai_engine) is importable
_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.students import router as students_router
from app.core.config import settings
from app.database.session import init_db
import app.models  # Ensure all models are registered for init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="NEXTSTEP AI", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(students_router)


@app.get("/health")
def health():
    return {"status": "ok"}