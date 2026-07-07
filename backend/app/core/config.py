"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "ANATEL Dashboard API"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    database_url: str | None = None
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None


def get_settings() -> Settings:
    return Settings(
        backend_host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        backend_port=parse_int(os.getenv("BACKEND_PORT"), default=8000),
        database_url=os.getenv("DATABASE_URL"),
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
    )


def parse_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
