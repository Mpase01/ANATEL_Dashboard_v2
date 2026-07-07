"""Dashboard queries used by API endpoints."""

from __future__ import annotations

from typing import Any


def normalize_period_filter(period: str) -> int:
    if period == "latest":
        return 1
    if period == "last3":
        return 3
    return 1200


def _sql_text(statement: str):
    try:
        from sqlalchemy import text
    except ModuleNotFoundError as exc:  # pragma: no cover - only before deps install.
        raise RuntimeError("SQLAlchemy is not installed.") from exc

    return text(statement)


def get_provider_summary(session: Any, provider_id: int, period: str = "all") -> dict[str, object] | None:
    statement = _sql_text(
        """
        with selected_periods as (
            select distinct period
            from public.subscription_records
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        period_bounds as (
            select min(period) as first_period, max(period) as latest_period
            from selected_periods
        ),
        latest_records as (
            select sr.*
            from public.subscription_records sr
            join period_bounds pb on pb.latest_period = sr.period
            where sr.provider_id = :provider_id
        ),
        latest_total as (
            select coalesce(sum(subscriptions_count), 0)::integer as subscriptions_count
            from latest_records
        ),
        first_total as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as subscriptions_count
            from public.subscription_records sr
            join period_bounds pb on pb.first_period = sr.period
            where sr.provider_id = :provider_id
        ),
        fiber_totals as (
            select coalesce(sum(subscriptions_count), 0)::integer as fiber_count
            from latest_records
            where lower(access_medium) like '%fibra%'
               or lower(technology) like '%ftth%'
        ),
        footprint as (
            select
                count(distinct municipality_code)::integer as municipalities_count,
                count(distinct state)::integer as states_count
            from latest_records
        ),
        national_totals as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as national_count
            from public.subscription_records sr
            join period_bounds pb on pb.latest_period = sr.period
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
            pb.latest_period as period,
            lt.subscriptions_count,
            ft.fiber_count,
            round((ft.fiber_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            round((lt.subscriptions_count::numeric / nullif(nt.national_count, 0)) * 100, 2) as market_share_percent,
            fp.municipalities_count,
            fp.states_count,
            tm.municipality_name as top_municipality_name,
            tm.state as top_municipality_state,
            coalesce(tm.subscriptions_count, 0)::integer as top_municipality_subscriptions,
            ts.state as top_state,
            coalesce(ts.subscriptions_count, 0)::integer as top_state_subscriptions,
            round(((lt.subscriptions_count - fst.subscriptions_count)::numeric / nullif(fst.subscriptions_count, 0)) * 100, 2) as growth_percent,
            pb.first_period
        from public.providers p
        cross join period_bounds pb
        cross join latest_total lt
        cross join first_total fst
        cross join fiber_totals ft
        cross join footprint fp
        cross join national_totals nt
        left join top_municipality tm on true
        left join top_state ts on true
        where p.id = :provider_id
          and pb.latest_period is not null
        """
    )
    row = session.execute(
        statement,
        {"provider_id": provider_id, "period_limit": normalize_period_filter(period)},
    ).mappings().first()
    if row is None:
        return None
    return dict(row)


def get_provider_evolution(session: Any, provider_id: int, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        """
        with selected_periods as (
            select distinct period
            from public.subscription_records
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        )
        select
            sr.period,
            sum(sr.subscriptions_count)::integer as subscriptions_count
        from public.subscription_records sr
        join selected_periods sp on sp.period = sr.period
        where sr.provider_id = :provider_id
        group by sr.period
        order by sr.period
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"provider_id": provider_id, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_provider_technologies(session: Any, provider_id: int, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        """
        with selected_periods as (
            select distinct period
            from public.subscription_records
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
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
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"provider_id": provider_id, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_provider_municipalities(
    session: Any,
    provider_id: int,
    period: str = "all",
    limit: int = 20,
) -> list[dict[str, object]]:
    limit = max(1, min(limit, 100))
    statement = _sql_text(
        """
        with selected_periods as (
            select distinct period
            from public.subscription_records
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
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
            {
                "provider_id": provider_id,
                "period_limit": normalize_period_filter(period),
                "limit": limit,
            },
        ).mappings()
    ]
