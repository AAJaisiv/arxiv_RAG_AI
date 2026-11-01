"""Database connection setup and health check."""

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 3},
)


def check_database() -> bool:
    """Return True if the database answers a trivial query, else False."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        return False