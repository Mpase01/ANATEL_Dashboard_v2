"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.session import session_scope
from app.repositories.dashboard import (
    get_provider_evolution,
    get_provider_municipalities,
    get_provider_summary,
    get_provider_technologies,
)
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
            {"id": result.id, "cnpj": result.cnpj, "name": result.name}
            for result in results
        ]

    @app.get("/providers/{provider_id}/summary")
    def provider_summary(provider_id: int) -> dict[str, object]:
        try:
            with session_scope() as session:
                summary = get_provider_summary(session, provider_id=provider_id)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        if summary is None:
            raise HTTPException(status_code=404, detail="Provider not found.")
        return summary

    @app.get("/providers/{provider_id}/evolution")
    def provider_evolution(provider_id: int) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_evolution(session, provider_id=provider_id)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/providers/{provider_id}/technologies")
    def provider_technologies(provider_id: int) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_technologies(session, provider_id=provider_id)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/providers/{provider_id}/municipalities")
    def provider_municipalities(
        provider_id: int,
        limit: int = Query(default=20, ge=1, le=100),
    ) -> list[dict[str, object]]:
        try:
            with session_scope() as session:
                return get_provider_municipalities(
                    session,
                    provider_id=provider_id,
                    limit=limit,
                )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app


app = create_app()
