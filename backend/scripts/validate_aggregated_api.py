"""Validate dashboard repository queries against the aggregated Supabase table."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))

from sqlalchemy import text

from app.db.session import session_scope
from app.repositories.dashboard import (
    get_provider_evolution,
    get_provider_municipalities,
    get_provider_person_types,
    get_provider_summary,
    get_provider_technologies,
)


def main() -> None:
    with session_scope() as session:
        provider = session.execute(
            text(
                """
                select
                    provider_id,
                    sum(subscriptions_count)::bigint as subscriptions_count
                from public.aggregated_subscription_records
                group by provider_id
                order by subscriptions_count desc
                limit 1
                """
            )
        ).mappings().one()

        provider_id = int(provider["provider_id"])
        summary = get_provider_summary(session, provider_id=provider_id, period="all")
        evolution = get_provider_evolution(session, provider_id=provider_id, period="all")
        technologies = get_provider_technologies(session, provider_id=provider_id, period="all")
        person_types = get_provider_person_types(session, provider_id=provider_id, period="all")
        municipalities = get_provider_municipalities(session, provider_id=provider_id, period="all", limit=5)

    print(f"provider_id: {provider_id}")
    print(f"summary_found: {summary is not None}")
    print(f"summary_name: {summary['name'] if summary else ''}")
    print(f"summary_subscriptions_latest: {summary['subscriptions_count'] if summary else 0}")
    print(f"evolution_points: {len(evolution)}")
    print(f"technologies_count: {len(technologies)}")
    print(f"person_types_count: {len(person_types)}")
    print(f"municipalities_count: {len(municipalities)}")


if __name__ == "__main__":
    main()
