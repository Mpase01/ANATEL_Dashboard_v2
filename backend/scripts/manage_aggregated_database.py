"""Manage the Supabase tables used by the aggregated dashboard import."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))

from sqlalchemy import create_engine, text


def load_env_file() -> None:
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def create_database_engine():
    load_env_file()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")
    return create_engine(database_url, pool_pre_ping=True)


def show_status() -> None:
    engine = create_database_engine()
    queries = {
        "providers": "select count(*)::bigint from public.providers",
        "subscription_records": "select count(*)::bigint from public.subscription_records",
        "import_batches": "select count(*)::bigint from public.import_batches",
        "import_files": "select count(*)::bigint from public.import_files",
    }

    with engine.connect() as connection:
        for label, sql in queries.items():
            count = connection.execute(text(sql)).scalar_one()
            print(f"{label}: {count}")

        aggregate_exists = connection.execute(
            text("select to_regclass('public.aggregated_subscription_records') is not null")
        ).scalar_one()
        print(f"aggregated_subscription_records_exists: {aggregate_exists}")

        if aggregate_exists:
            aggregate_count = connection.execute(
                text("select count(*)::bigint from public.aggregated_subscription_records")
            ).scalar_one()
            aggregate_total = connection.execute(
                text("select coalesce(sum(subscriptions_count), 0)::bigint from public.aggregated_subscription_records")
            ).scalar_one()
            print(f"aggregated_subscription_records: {aggregate_count}")
            print(f"aggregated_subscriptions_sum: {aggregate_total}")


def apply_aggregated_schema() -> None:
    schema_path = ROOT_DIR / "database" / "aggregated_schema.sql"
    sql = schema_path.read_text(encoding="utf-8")
    engine = create_database_engine()
    with engine.begin() as connection:
        connection.exec_driver_sql(sql)
    print("aggregated_schema_applied: True")


def clear_detailed_records() -> None:
    engine = create_database_engine()
    with engine.begin() as connection:
        before = connection.execute(text("select count(*)::bigint from public.subscription_records")).scalar_one()
        connection.execute(text("truncate table public.subscription_records restart identity"))
    print(f"subscription_records_deleted: {before}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage aggregated ANATEL dashboard database tables.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status")
    subparsers.add_parser("apply-schema")

    clear_parser = subparsers.add_parser("clear-detailed-records")
    clear_parser.add_argument("--yes-i-understand", action="store_true")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "status":
        show_status()
    elif args.command == "apply-schema":
        apply_aggregated_schema()
    elif args.command == "clear-detailed-records":
        if not args.yes_i_understand:
            raise SystemExit("Refusing to clear detailed records without --yes-i-understand.")
        clear_detailed_records()


if __name__ == "__main__":
    main()
