"""Dashboard queries used by API endpoints."""

from __future__ import annotations

from typing import Any


def _sql_text(statement: str):
    try:
        from sqlalchemy import text
    except ModuleNotFoundError as exc:  # pragma: no cover - only before deps install.
        raise RuntimeError("SQLAlchemy is not installed.") from exc

    return text(statement)


def get_provider_summary(session: Any, provider_id: int) -> dict[str, object] | None:
    statement = _sql_text(
        """
        with latest_period as (
            select max(period) as period
            from public.subscription_records
            where provider_id = :provider_id
        ),
        latest_records as (
            select sr.*
            from public.subscription_records sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
        ),
        provider_totals as (
            select
                sum(subscriptions_count)::integer as subscriptions_count,
                count(distinct municipality_code)::integer as municipalities_count,
                count(distinct state)::integer as states_count
            from latest_records
        ),
        fiber_totals as (
            select coalesce(sum(subscriptions_count), 0)::integer as fiber_count
            from latest_records
            where lower(access_medium) like '%fibra%'
               or lower(technology) like '%ftth%'
        ),
        national_totals as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as national_count
            from public.subscription_records sr
            join latest_period lp on lp.period = sr.period
        ),
        first_month as (
            select period, sum(subscriptions_count)::integer as subscriptions_count
            from public.subscription_records
            where provider_id = :provider_id
            group by period
            order by period
            limit 1
        ),
        latest_month as (
            select lp.period, pt.subscriptions_count
            from latest_period lp
            cross join provider_totals pt
        ),
        top_municipality as (
            select municipality_name, state, sum(subscriptions_count)::integer as subscriptions_count
            from latest_records
            group by municipality_name, state
            order by subscriptions_count desc, municipality_name
            limit 1
        ),
        top_state as (
            select state, sum(subscriptions_count)::integer as subscriptions_count
            from latest_records
            group by state
            order by subscriptions_count desc, state
            limit 1
        )
        select
            p.id as provider_id,
            p.cnpj,
            p.primary_name as name,
            lm.period,
            coalesce(pt.subscriptions_count, 0)::integer as subscriptions_count,
            coalesce(ft.fiber_count, 0)::integer as fiber_count,
            round((coalesce(ft.fiber_count, 0)::numeric / nullif(pt.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            round((pt.subscriptions_count::numeric / nullif(nt.national_count, 0)) * 100, 2) as market_share_percent,
            coalesce(pt.municipalities_count, 0)::integer as municipalities_count,
            coalesce(pt.states_count, 0)::integer as states_count,
            tm.municipality_name as top_municipality_name,
            tm.state as top_municipality_state,
            coalesce(tm.subscriptions_count, 0)::integer as top_municipality_subscriptions,
            ts.state as top_state,
            coalesce(ts.subscriptions_count, 0)::integer as top_state_subscriptions,
            round(((lm.subscriptions_count - fm.subscriptions_count)::numeric / nullif(fm.subscriptions_count, 0)) * 100, 2) as growth_percent,
            fm.period as first_period
        from public.providers p
        cross join latest_month lm
        cross join provider_totals pt
        cross join fiber_totals ft
        cross join national_totals nt
        left join first_month fm on true
        left join top_municipality tm on true
        left join top_state ts on true
        where p.id = :provider_id
        """
    )
    row = session.execute(statement, {"provider_id": provider_id}).mappings().first()
    if row is None:
        return None

    return dict(row)


def get_provider_evolution(session: Any, provider_id: int) -> list[dict[str, object]]:
    statement = _sql_text(
        """
        select
            period,
            sum(subscriptions_count)::integer as subscriptions_count
        from public.subscription_records
        where provider_id = :provider_id
        group by period
        order by period
        """
    )
    return [dict(row) for row in session.execute(statement, {"provider_id": provider_id}).mappings()]


def get_provider_technologies(session: Any, provider_id: int) -> list[dict[str, object]]:
    statement = _sql_text(
        """
        with latest_period as (
            select max(period) as period
            from public.subscription_records
            where provider_id = :provider_id
        ),
        totals as (
            select sum(subscriptions_count)::numeric as total
            from public.subscription_records sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
        )
        select
            sr.technology,
            sr.access_medium,
            sum(sr.subscriptions_count)::integer as subscriptions_count,
            round((sum(sr.subscriptions_count)::numeric / nullif(t.total, 0)) * 100, 2) as share_percent
        from public.subscription_records sr
        join latest_period lp on lp.period = sr.period
        cross join totals t
        where sr.provider_id = :provider_id
        group by sr.technology, sr.access_medium, t.total
        order by subscriptions_count desc, sr.technology, sr.access_medium
        """
    )
    return [dict(row) for row in session.execute(statement, {"provider_id": provider_id}).mappings()]


def get_provider_municipalities(session: Any, provider_id: int, limit: int = 20) -> list[dict[str, object]]:
    limit = max(1, min(limit, 100))
    statement = _sql_text(
        """
        with latest_period as (
            select max(period) as period
            from public.subscription_records
            where provider_id = :provider_id
        )
        select
            municipality_name,
            state,
            municipality_code,
            sum(subscriptions_count)::integer as subscriptions_count
        from public.subscription_records sr
        join latest_period lp on lp.period = sr.period
        where sr.provider_id = :provider_id
        group by municipality_name, state, municipality_code
        order by subscriptions_count desc, municipality_name
        limit :limit
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"provider_id": provider_id, "limit": limit},
        ).mappings()
    ]
