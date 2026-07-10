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


RECORDS_TABLE = "public.aggregated_subscription_records"


def get_provider_summary(session: Any, provider_id: int, period: str = "all") -> dict[str, object] | None:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
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
            from {RECORDS_TABLE} sr
            join period_bounds pb on pb.latest_period = sr.period
            where sr.provider_id = :provider_id
        ),
        latest_total as (
            select coalesce(sum(subscriptions_count), 0)::integer as subscriptions_count
            from latest_records
        ),
        first_total as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as subscriptions_count
            from {RECORDS_TABLE} sr
            join period_bounds pb on pb.first_period = sr.period
            where sr.provider_id = :provider_id
        ),
        fiber_totals as (
            select coalesce(sum(subscriptions_count), 0)::integer as fiber_count
            from latest_records
            where access_medium = 'Fibra'
        ),
        client_profile as (
            select
                coalesce(sum(subscriptions_count) filter (where lower(person_type) like '%jur%dica%'), 0)::integer as b2b_count,
                coalesce(sum(subscriptions_count) filter (where lower(person_type) like '%f%sica%'), 0)::integer as b2c_count
            from latest_records
        ),
        footprint as (
            select
                count(distinct municipality_code)::integer as municipalities_count,
                count(distinct state)::integer as states_count
            from latest_records
        ),
        national_totals as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as national_count
            from {RECORDS_TABLE} sr
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
            cp.b2b_count,
            cp.b2c_count,
            round((ft.fiber_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            round((cp.b2b_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as b2b_share_percent,
            round((cp.b2c_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as b2c_share_percent,
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
        cross join client_profile cp
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
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        )
        select
            sr.period,
            sum(sr.subscriptions_count)::integer as subscriptions_count
        from {RECORDS_TABLE} sr
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
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        totals as (
            select sum(subscriptions_count)::numeric as total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
        )
        select
            sr.access_medium,
            sum(sr.subscriptions_count)::integer as subscriptions_count,
            round((sum(sr.subscriptions_count)::numeric / nullif(t.total, 0)) * 100, 2) as share_percent
        from {RECORDS_TABLE} sr
        join latest_period lp on lp.period = sr.period
        cross join totals t
        where sr.provider_id = :provider_id
        group by sr.access_medium, t.total
        order by subscriptions_count desc, sr.access_medium
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"provider_id": provider_id, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_provider_person_types(session: Any, provider_id: int, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        totals as (
            select sum(subscriptions_count)::numeric as total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
        )
        select
            sr.person_type,
            sum(sr.subscriptions_count)::integer as subscriptions_count,
            round((sum(sr.subscriptions_count)::numeric / nullif(t.total, 0)) * 100, 2) as share_percent
        from {RECORDS_TABLE} sr
        join latest_period lp on lp.period = sr.period
        cross join totals t
        where sr.provider_id = :provider_id
        group by sr.person_type, t.total
        order by subscriptions_count desc, sr.person_type
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
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where provider_id = :provider_id
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        entity_city as (
            select
                sr.municipality_name,
                sr.state,
                sr.municipality_code,
                sum(sr.subscriptions_count)::integer as subscriptions_count,
                coalesce(sum(sr.subscriptions_count) filter (where sr.access_medium = 'Fibra'), 0)::integer as fiber_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%jur%dica%'), 0)::integer as b2b_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%f%sica%'), 0)::integer as b2c_count
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
            group by sr.municipality_name, sr.state, sr.municipality_code
        ),
        city_market as (
            select
                municipality_code,
                sum(subscriptions_count)::numeric as city_total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by municipality_code
        ),
        city_ranks as (
            select
                provider_id,
                municipality_code,
                rank() over (
                    partition by municipality_code
                    order by sum(subscriptions_count) desc
                )::integer as rank_position
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by provider_id, municipality_code
        ),
        entity_state as (
            select
                sr.state,
                sum(sr.subscriptions_count)::integer as state_subscriptions_count,
                coalesce(sum(sr.subscriptions_count) filter (where sr.access_medium = 'Fibra'), 0)::integer as state_fiber_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%jur%dica%'), 0)::integer as state_b2b_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%f%sica%'), 0)::integer as state_b2c_count
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.provider_id = :provider_id
            group by sr.state
        ),
        state_market as (
            select
                state,
                sum(subscriptions_count)::numeric as state_total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by state
        ),
        state_ranks as (
            select
                provider_id,
                state,
                rank() over (
                    partition by state
                    order by sum(subscriptions_count) desc
                )::integer as state_rank_position
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by provider_id, state
        )
        select
            ec.municipality_name,
            ec.state,
            ec.municipality_code,
            ec.subscriptions_count,
            round((ec.subscriptions_count::numeric / nullif(cm.city_total, 0)) * 100, 2) as market_share_percent,
            ec.fiber_count,
            round((ec.fiber_count::numeric / nullif(ec.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            ec.b2b_count,
            ec.b2c_count,
            cr.rank_position,
            es.state_subscriptions_count,
            round((es.state_subscriptions_count::numeric / nullif(sm.state_total, 0)) * 100, 2) as state_market_share_percent,
            es.state_fiber_count,
            round((es.state_fiber_count::numeric / nullif(es.state_subscriptions_count, 0)) * 100, 2) as state_fiber_share_percent,
            es.state_b2b_count,
            es.state_b2c_count,
            srk.state_rank_position
        from entity_city ec
        join city_market cm on cm.municipality_code = ec.municipality_code
        left join city_ranks cr on cr.provider_id = :provider_id and cr.municipality_code = ec.municipality_code
        join entity_state es on es.state = ec.state
        join state_market sm on sm.state = ec.state
        left join state_ranks srk on srk.provider_id = :provider_id and srk.state = ec.state
        order by es.state_subscriptions_count desc, ec.subscriptions_count desc, ec.municipality_name
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


def get_economic_group_summary(session: Any, economic_group: str, period: str = "all") -> dict[str, object] | None:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where economic_group = :economic_group
            order by period desc
            limit :period_limit
        ),
        period_bounds as (
            select min(period) as first_period, max(period) as latest_period
            from selected_periods
        ),
        latest_records as (
            select sr.*
            from {RECORDS_TABLE} sr
            join period_bounds pb on pb.latest_period = sr.period
            where sr.economic_group = :economic_group
        ),
        latest_total as (
            select coalesce(sum(subscriptions_count), 0)::integer as subscriptions_count
            from latest_records
        ),
        first_total as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as subscriptions_count
            from {RECORDS_TABLE} sr
            join period_bounds pb on pb.first_period = sr.period
            where sr.economic_group = :economic_group
        ),
        fiber_totals as (
            select coalesce(sum(subscriptions_count), 0)::integer as fiber_count
            from latest_records
            where access_medium = 'Fibra'
        ),
        client_profile as (
            select
                coalesce(sum(subscriptions_count) filter (where lower(person_type) like '%jur%dica%'), 0)::integer as b2b_count,
                coalesce(sum(subscriptions_count) filter (where lower(person_type) like '%f%sica%'), 0)::integer as b2c_count
            from latest_records
        ),
        footprint as (
            select
                count(distinct municipality_code)::integer as municipalities_count,
                count(distinct state)::integer as states_count
            from latest_records
        ),
        national_totals as (
            select coalesce(sum(sr.subscriptions_count), 0)::integer as national_count
            from {RECORDS_TABLE} sr
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
            null::integer as provider_id,
            '' as cnpj,
            :economic_group as name,
            pb.latest_period as period,
            lt.subscriptions_count,
            ft.fiber_count,
            cp.b2b_count,
            cp.b2c_count,
            round((ft.fiber_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            round((cp.b2b_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as b2b_share_percent,
            round((cp.b2c_count::numeric / nullif(lt.subscriptions_count, 0)) * 100, 2) as b2c_share_percent,
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
        from period_bounds pb
        cross join latest_total lt
        cross join first_total fst
        cross join fiber_totals ft
        cross join client_profile cp
        cross join footprint fp
        cross join national_totals nt
        left join top_municipality tm on true
        left join top_state ts on true
        where pb.latest_period is not null
        """
    )
    row = session.execute(
        statement,
        {"economic_group": economic_group, "period_limit": normalize_period_filter(period)},
    ).mappings().first()
    if row is None:
        return None
    return dict(row)


def get_economic_group_evolution(session: Any, economic_group: str, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where economic_group = :economic_group
            order by period desc
            limit :period_limit
        )
        select
            sr.period,
            sum(sr.subscriptions_count)::integer as subscriptions_count
        from {RECORDS_TABLE} sr
        join selected_periods sp on sp.period = sr.period
        where sr.economic_group = :economic_group
        group by sr.period
        order by sr.period
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"economic_group": economic_group, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_economic_group_technologies(session: Any, economic_group: str, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where economic_group = :economic_group
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        totals as (
            select sum(subscriptions_count)::numeric as total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.economic_group = :economic_group
        )
        select
            sr.access_medium,
            sum(sr.subscriptions_count)::integer as subscriptions_count,
            round((sum(sr.subscriptions_count)::numeric / nullif(t.total, 0)) * 100, 2) as share_percent
        from {RECORDS_TABLE} sr
        join latest_period lp on lp.period = sr.period
        cross join totals t
        where sr.economic_group = :economic_group
        group by sr.access_medium, t.total
        order by subscriptions_count desc, sr.access_medium
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"economic_group": economic_group, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_economic_group_person_types(session: Any, economic_group: str, period: str = "all") -> list[dict[str, object]]:
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where economic_group = :economic_group
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        totals as (
            select sum(subscriptions_count)::numeric as total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.economic_group = :economic_group
        )
        select
            sr.person_type,
            sum(sr.subscriptions_count)::integer as subscriptions_count,
            round((sum(sr.subscriptions_count)::numeric / nullif(t.total, 0)) * 100, 2) as share_percent
        from {RECORDS_TABLE} sr
        join latest_period lp on lp.period = sr.period
        cross join totals t
        where sr.economic_group = :economic_group
        group by sr.person_type, t.total
        order by subscriptions_count desc, sr.person_type
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {"economic_group": economic_group, "period_limit": normalize_period_filter(period)},
        ).mappings()
    ]


def get_economic_group_municipalities(
    session: Any,
    economic_group: str,
    period: str = "all",
    limit: int = 20,
) -> list[dict[str, object]]:
    limit = max(1, min(limit, 100))
    statement = _sql_text(
        f"""
        with selected_periods as (
            select distinct period
            from {RECORDS_TABLE}
            where economic_group = :economic_group
            order by period desc
            limit :period_limit
        ),
        latest_period as (
            select max(period) as period from selected_periods
        ),
        entity_city as (
            select
                sr.municipality_name,
                sr.state,
                sr.municipality_code,
                sum(sr.subscriptions_count)::integer as subscriptions_count,
                coalesce(sum(sr.subscriptions_count) filter (where sr.access_medium = 'Fibra'), 0)::integer as fiber_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%jur%dica%'), 0)::integer as b2b_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%f%sica%'), 0)::integer as b2c_count
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.economic_group = :economic_group
            group by sr.municipality_name, sr.state, sr.municipality_code
        ),
        city_market as (
            select
                municipality_code,
                sum(subscriptions_count)::numeric as city_total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by municipality_code
        ),
        city_ranks as (
            select
                economic_group,
                municipality_code,
                rank() over (
                    partition by municipality_code
                    order by sum(subscriptions_count) desc
                )::integer as rank_position
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by economic_group, municipality_code
        ),
        entity_state as (
            select
                sr.state,
                sum(sr.subscriptions_count)::integer as state_subscriptions_count,
                coalesce(sum(sr.subscriptions_count) filter (where sr.access_medium = 'Fibra'), 0)::integer as state_fiber_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%jur%dica%'), 0)::integer as state_b2b_count,
                coalesce(sum(sr.subscriptions_count) filter (where lower(sr.person_type) like '%f%sica%'), 0)::integer as state_b2c_count
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            where sr.economic_group = :economic_group
            group by sr.state
        ),
        state_market as (
            select
                state,
                sum(subscriptions_count)::numeric as state_total
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by state
        ),
        state_ranks as (
            select
                economic_group,
                state,
                rank() over (
                    partition by state
                    order by sum(subscriptions_count) desc
                )::integer as state_rank_position
            from {RECORDS_TABLE} sr
            join latest_period lp on lp.period = sr.period
            group by economic_group, state
        )
        select
            ec.municipality_name,
            ec.state,
            ec.municipality_code,
            ec.subscriptions_count,
            round((ec.subscriptions_count::numeric / nullif(cm.city_total, 0)) * 100, 2) as market_share_percent,
            ec.fiber_count,
            round((ec.fiber_count::numeric / nullif(ec.subscriptions_count, 0)) * 100, 2) as fiber_share_percent,
            ec.b2b_count,
            ec.b2c_count,
            cr.rank_position,
            es.state_subscriptions_count,
            round((es.state_subscriptions_count::numeric / nullif(sm.state_total, 0)) * 100, 2) as state_market_share_percent,
            es.state_fiber_count,
            round((es.state_fiber_count::numeric / nullif(es.state_subscriptions_count, 0)) * 100, 2) as state_fiber_share_percent,
            es.state_b2b_count,
            es.state_b2c_count,
            srk.state_rank_position
        from entity_city ec
        join city_market cm on cm.municipality_code = ec.municipality_code
        left join city_ranks cr on cr.economic_group = :economic_group and cr.municipality_code = ec.municipality_code
        join entity_state es on es.state = ec.state
        join state_market sm on sm.state = ec.state
        left join state_ranks srk on srk.economic_group = :economic_group and srk.state = ec.state
        order by es.state_subscriptions_count desc, ec.subscriptions_count desc, ec.municipality_name
        limit :limit
        """
    )
    return [
        dict(row)
        for row in session.execute(
            statement,
            {
                "economic_group": economic_group,
                "period_limit": normalize_period_filter(period),
                "limit": limit,
            },
        ).mappings()
    ]
