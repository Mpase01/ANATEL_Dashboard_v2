"""Provider queries used by API endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderSearchResult:
    id: int
    cnpj: str
    name: str


def normalize_search_query(query: str) -> str:
    return " ".join((query or "").strip().split())


def search_providers(session: Any, query: str, limit: int = 20) -> list[ProviderSearchResult]:
    normalized_query = normalize_search_query(query)
    if not normalized_query:
        return []

    try:
        from sqlalchemy import text
    except ModuleNotFoundError as exc:  # pragma: no cover - only before deps install.
        raise RuntimeError("SQLAlchemy is not installed.") from exc

    limit = max(1, min(limit, 50))
    digits = "".join(character for character in normalized_query if character.isdigit())

    statement = text(
        """
        select distinct
            p.id,
            p.cnpj,
            p.primary_name as name
        from providers p
        left join provider_aliases pa on pa.provider_id = p.id
        where
            (:digits <> '' and p.cnpj like :cnpj_query)
            or p.primary_name ilike :name_query
            or pa.alias_name ilike :name_query
        order by p.primary_name
        limit :limit
        """
    )

    rows = session.execute(
        statement,
        {
            "digits": digits,
            "cnpj_query": f"%{digits}%",
            "name_query": f"%{normalized_query}%",
            "limit": limit,
        },
    ).mappings()

    return [
        ProviderSearchResult(
            id=int(row["id"]),
            cnpj=str(row["cnpj"]),
            name=str(row["name"]),
        )
        for row in rows
    ]
