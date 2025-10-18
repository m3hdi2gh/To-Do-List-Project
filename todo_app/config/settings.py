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


@dataclass(frozen=True)
class Settings:
    MAX_NUMBER_OF_PROJECT: int = _get_int("MAX_NUMBER_OF_PROJECT", 10)
    MAX_NUMBER_OF_TASK: int = _get_int("MAX_NUMBER_OF_TASK", 100)


settings = Settings()
