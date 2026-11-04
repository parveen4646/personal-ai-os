"""Configuration shared by all Personal AI OS services."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from the environment and optional `.env` file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Personal AI OS"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_os"
    ollama_url: str = "http://localhost:11434"
    model_name: str = "qwen3:8b"


@lru_cache
def get_settings() -> Settings:
    return Settings()
