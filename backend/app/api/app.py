"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import session_scope
from app.repositories.dashboard import (
    get_economic_group_evolution,
    get_economic_group_municipalities,
    get_economic_group_person_types,
    get_economic_group_summary,
    get_economic_group_technologies,
    get_provider_evolution,
    get_provider_municipalities,
    get_provider_person_types,
    get_provider_summary,
    get_provider_technologies,
)
from app.repositories.economic_groups import search_economic_groups
from app.repositories.providers import search_providers


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/database")
    def database_health() -> dict[str, object]:
        try:
            with session_scope() as session:
                result = session.execute(
                    text(
                        """
                        select
                            (select count(*) from public.providers) as providers_count,
                            (select count(*) from public.aggregated_subscription_records) as records_count,
                            (select coalesce(sum(subscriptions_count), 0) from public.aggregated_subscription_records) as subscriptions_sum
                        """
                    )
                ).mappings().one()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=503, detail="Database connection failed.") from exc

        return {
            "status": "ok",
            "providers_count": result["providers_count"],
            "records_count": result["records_count"],
            "subscriptions_sum": result["subscriptions_sum"],
        }

    @app.get("/providers/search")
    def providers_search(
        query: str = Query(min_length=1),
        limit: int = Query(default=20, ge=1, le=50),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                results = search_providers(session, query=query, limit=limit)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        return [
            {
                "id": result.id,
                "cnpj": result.cnpj,
                "name": result.name,
                "latest_subscriptions_count": result.latest_subscriptions_count,
            }
            for result in results
        ]

    @app.get("/economic-groups/search")
    def economic_groups_search(
        query: str = Query(min_length=1),
        limit: int = Query(default=20, ge=1, le=50),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                results = search_economic_groups(session, query=query, limit=limit)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        return [
            {
                "name": result.name,
                "latest_subscriptions_count": result.latest_subscriptions_count,
                "kind": result.kind,
                "provider_id": result.provider_id,
                "cnpj": result.cnpj,
            }
            for result in results
        ]

    @app.get("/providers/{provider_id}/summary")
    def provider_summary(
        provider_id: int,
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> dict[str, object]:
        try:
            with session_scope() as session:
                summary = get_provider_summary(session, provider_id=provider_id, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        if summary is None:
            raise HTTPException(status_code=404, detail="Provider not found.")
        return summary

    @app.get("/providers/{provider_id}/evolution")
    def provider_evolution(
        provider_id: int,
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_evolution(session, provider_id=provider_id, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/providers/{provider_id}/technologies")
    def provider_technologies(
        provider_id: int,
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_technologies(session, provider_id=provider_id, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/providers/{provider_id}/person-types")
    def provider_person_types(
        provider_id: int,
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_person_types(session, provider_id=provider_id, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/providers/{provider_id}/municipalities")
    def provider_municipalities(
        provider_id: int,
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
        limit: int = Query(default=20, ge=1, le=100),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_municipalities(
                    session,
                    provider_id=provider_id,
                    period=period,
                    limit=limit,
                )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/economic-groups/summary")
    def economic_group_summary(
        group: str = Query(min_length=1),
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> dict[str, object]:
        try:
            with session_scope() as session:
                summary = get_economic_group_summary(session, economic_group=group, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        if summary is None:
            raise HTTPException(status_code=404, detail="Economic group not found.")
        return summary

    @app.get("/economic-groups/evolution")
    def economic_group_evolution(
        group: str = Query(min_length=1),
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_economic_group_evolution(session, economic_group=group, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/economic-groups/technologies")
    def economic_group_technologies(
        group: str = Query(min_length=1),
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_economic_group_technologies(session, economic_group=group, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/economic-groups/person-types")
    def economic_group_person_types(
        group: str = Query(min_length=1),
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_economic_group_person_types(session, economic_group=group, period=period)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/economic-groups/municipalities")
    def economic_group_municipalities(
        group: str = Query(min_length=1),
        period: str = Query(default="all", pattern="^(all|last3|latest)$"),
        limit: int = Query(default=20, ge=1, le=100),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_economic_group_municipalities(
                    session,
                    economic_group=group,
                    period=period,
                    limit=limit,
                )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app


app = create_app()
