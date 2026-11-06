from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_backend_env = Path(__file__).resolve().parent.parent.parent / ".env"
_root_env = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///mentor.db"
    SECRET_KEY: str = "academic-mentor-jwt-secret-key-development-2026-safe"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=[str(_backend_env), str(_root_env), ".env"],
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
