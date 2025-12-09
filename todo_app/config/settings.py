"""
Loads environment variables and exposes typed settings for the app.
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"Invalid integer for {name}: {raw!r}")


def _get_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw


@dataclass(frozen=True)
class Settings:
    # Business limits
    MAX_NUMBER_OF_PROJECT: int = _get_int("MAX_NUMBER_OF_PROJECT", 10)
    MAX_NUMBER_OF_TASK: int = _get_int("MAX_NUMBER_OF_TASK", 100)

    # Database config
    DB_HOST: str = _get_str("DB_HOST", "localhost")
    DB_PORT: int = _get_int("DB_PORT", 5432)
    DB_NAME: str = _get_str("DB_NAME", "todolist")
    DB_USER: str = _get_str("DB_USER", "todolist_user")
    DB_PASSWORD: str = _get_str("DB_PASSWORD", "todolist_password")

    @property
    def DATABASE_URL(self) -> str:
        """
        Build a SQLAlchemy-compatible database URL.
        Example: postgresql+psycopg2://user:pass@host:port/dbname
        """
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
