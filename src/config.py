"""Application settings, loaded from environment variables and .env."""

from functools import lru_cache
from typing import Literal
from sqlalchemy.engine import URL

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
        # OpenSearch and Ollama
    opensearch_host: str = "http://localhost:9200"
    ollama_host: str = "http://localhost:11434"

    @property
    def database_url(self) -> URL:
        """Connection URL, built safely so special characters can't break it."""
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,

        )


@lru_cache
def get_settings() -> Settings:
    """Build Settings once and reuse the same object everywhere."""
    return Settings()