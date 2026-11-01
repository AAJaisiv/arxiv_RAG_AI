"""Application settings, loaded from environment variables and .env."""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "arxiv-rag"
    environment: Literal["dev", "test", "prod"] = "dev"
    log_level: str = "INFO"

    # Postgres
    postgres_user: str = "rag_user"
    postgres_password: SecretStr
    postgres_db: str = "rag_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        """Connection string built from the parts above."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Build Settings once and reuse the same object everywhere."""
    return Settings()