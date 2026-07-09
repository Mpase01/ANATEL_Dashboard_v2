"""Provider queries used by API endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderSearchResult:
    id: int
    cnpj: str
    name: str
    latest_subscriptions_count: int = 0


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
        with latest_period as (
            select max(period) as period
            from public.aggregated_subscription_records
        ),
        latest_totals as (
            select
                provider_id,
                sum(subscriptions_count)::bigint as latest_subscriptions_count
            from public.aggregated_subscription_records ar
            join latest_period lp on lp.period = ar.period
            group by provider_id
        )
        select distinct
            p.id,
            p.cnpj,
            p.primary_name as name,
            coalesce(lt.latest_subscriptions_count, 0)::bigint as latest_subscriptions_count
        from providers p
        left join provider_aliases pa on pa.provider_id = p.id
        left join latest_totals lt on lt.provider_id = p.id
        where
            (:digits <> '' and p.cnpj like :cnpj_query)
            or p.primary_name ilike :name_query
            or pa.alias_name ilike :name_query
        order by latest_subscriptions_count desc, p.primary_name, p.cnpj
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
            latest_subscriptions_count=int(row["latest_subscriptions_count"] or 0),
        )
        for row in rows
    ]
