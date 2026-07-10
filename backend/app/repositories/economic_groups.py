"""Economic group search queries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .dashboard import RECORDS_TABLE, _sql_text


@dataclass(frozen=True)
class EconomicGroupSearchResult:
    name: str
    latest_subscriptions_count: int
    kind: str = "group"
    provider_id: int | None = None
    cnpj: str = ""


def search_economic_groups(session: Any, query: str, limit: int = 20) -> list[EconomicGroupSearchResult]:
    clean_query = "".join(character for character in query if character.isdigit())
    group_statement = _sql_text(
        f"""
        with latest_period as (
            select max(period) as period
            from {RECORDS_TABLE}
        ),
        matching_groups as (
            select distinct economic_group
            from {RECORDS_TABLE}
            where economic_group <> 'OUTROS'
              and (
                  economic_group ilike :query
                  or company_name ilike :query
                  or (:clean_query <> '' and cnpj like :cnpj_query)
              )
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
    params = {
        "query": f"%{query.strip()}%",
        "clean_query": clean_query,
        "cnpj_query": f"%{clean_query}%",
        "limit": limit,
    }
    group_rows = session.execute(group_statement, params).mappings()
    results = [
        EconomicGroupSearchResult(
            name=str(row["name"]),
            latest_subscriptions_count=int(row["latest_subscriptions_count"] or 0),
        )
        for row in group_rows
    ]

    remaining = max(0, limit - len(results))
    if remaining == 0:
        return results

    provider_statement = _sql_text(
        f"""
        with latest_period as (
            select max(period) as period
            from {RECORDS_TABLE}
        ),
        latest_totals as (
            select
                sr.provider_id,
                sr.cnpj,
                sr.company_name,
                sum(sr.subscriptions_count)::integer as latest_subscriptions_count
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.economic_group = 'OUTROS'
              and (
                  sr.company_name ilike :query
                  or (:clean_query <> '' and sr.cnpj like :cnpj_query)
              )
            group by sr.provider_id, sr.cnpj, sr.company_name
        )
        select provider_id, cnpj, company_name as name, latest_subscriptions_count
        from latest_totals
        order by latest_subscriptions_count desc, name
        limit :limit
        """
    )
    provider_rows = session.execute(provider_statement, {**params, "limit": remaining}).mappings()
    results.extend(
        EconomicGroupSearchResult(
            name=str(row["name"]),
            latest_subscriptions_count=int(row["latest_subscriptions_count"] or 0),
            kind="provider",
            provider_id=int(row["provider_id"]),
            cnpj=str(row["cnpj"]),
        )
        for row in provider_rows
    )
    return results
