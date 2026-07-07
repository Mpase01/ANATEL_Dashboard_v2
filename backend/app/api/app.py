"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from app.core.config import get_settings
from app.db.session import session_scope
from app.repositories.providers import search_providers


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

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

    return app


app = create_app()
