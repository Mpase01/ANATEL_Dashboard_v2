"""Economic group search queries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .dashboard import RECORDS_TABLE, _sql_text


@dataclass(frozen=True)
class EconomicGroupSearchResult:
    name: str
    latest_subscriptions_count: int


def search_economic_groups(session: Any, query: str, limit: int = 20) -> list[EconomicGroupSearchResult]:
    clean_query = "".join(character for character in query if character.isdigit())
    statement = _sql_text(
        f"""
        with latest_period as (
            select max(period) as period
            from {RECORDS_TABLE}
        ),
        matching_groups as (
            select distinct economic_group
            from {RECORDS_TABLE}
            where economic_group ilike :query
               or company_name ilike :query
               or (:clean_query <> '' and cnpj like :cnpj_query)
        )
        select
            sr.economic_group as name,
            sum(sr.subscriptions_count)::integer as latest_subscriptions_count
        from {RECORDS_TABLE} sr
        join latest_period lp on lp.period = sr.period
        join matching_groups mg on mg.economic_group = sr.economic_group
        group by sr.economic_group
        order by latest_subscriptions_count desc, sr.economic_group
        limit :limit
        """
    )
    rows = session.execute(
        statement,
        {
            "query": f"%{query.strip()}%",
            "clean_query": clean_query,
            "cnpj_query": f"%{clean_query}%",
            "limit": limit,
        },
    ).mappings()
    return [
        EconomicGroupSearchResult(
            name=str(row["name"]),
            latest_subscriptions_count=int(row["latest_subscriptions_count"] or 0),
        )
        for row in rows
    ]
