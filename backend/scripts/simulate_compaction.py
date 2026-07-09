"""Estimate how much the ANATEL CSV shrinks after dashboard-friendly aggregation."""

from __future__ import annotations

import argparse
import itertools
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))

from app.importer.anatel_csv import inspect_csv, iter_subscription_records


def limited_records(path: Path, limit: int | None):
    records = iter_subscription_records(path)
    if limit is None:
        return records
    return itertools.islice(records, limit)


def build_compaction_key(record) -> tuple[object, ...]:
    return (
        record.cnpj,
        record.company_name,
        record.period,
        record.municipality_code,
        record.municipality_name,
        record.state,
        record.technology,
        record.access_medium,
        record.person_type,
    )


def simulate(csv_path: Path, *, limit: int | None, progress_every: int) -> dict[str, object]:
    started_at = time.monotonic()
    metadata = inspect_csv(csv_path)
    aggregates: defaultdict[tuple[object, ...], int] = defaultdict(int)
    providers: set[tuple[str, str]] = set()
    municipalities: set[tuple[str, str, str]] = set()
    technologies: Counter[str] = Counter()
    access_media: Counter[str] = Counter()
    person_types: Counter[str] = Counter()
    raw_records = 0
    raw_subscriptions = 0

    for record in limited_records(csv_path, limit):
        raw_records += 1
        raw_subscriptions += record.subscriptions_count
        aggregates[build_compaction_key(record)] += record.subscriptions_count
        providers.add((record.cnpj, record.company_name))
        municipalities.add((record.municipality_code, record.municipality_name, record.state))
        technologies[record.technology] += record.subscriptions_count
        access_media[record.access_medium] += record.subscriptions_count
        person_types[record.person_type] += record.subscriptions_count

        if progress_every and raw_records % progress_every == 0:
            print(
                f"raw_records={raw_records} aggregated_rows={len(aggregates)} "
                f"reduction={calculate_reduction(raw_records, len(aggregates))}%"
            )

    aggregated_rows = len(aggregates)
    return {
        "file_name": csv_path.name,
        "file_size_bytes": csv_path.stat().st_size,
        "months": list(metadata.month_columns),
        "raw_records": raw_records,
        "aggregated_rows": aggregated_rows,
        "reduction_percent": calculate_reduction(raw_records, aggregated_rows),
        "raw_subscriptions_sum": raw_subscriptions,
        "aggregated_subscriptions_sum": sum(aggregates.values()),
        "providers": len(providers),
        "municipalities": len(municipalities),
        "technologies": len(technologies),
        "access_media": len(access_media),
        "person_types": dict(sorted(person_types.items())),
        "top_technologies": technologies.most_common(10),
        "top_access_media": access_media.most_common(10),
        "elapsed_seconds": round(time.monotonic() - started_at, 2),
    }


def calculate_reduction(raw_records: int, aggregated_rows: int) -> float:
    if raw_records == 0:
        return 0.0
    return round((1 - (aggregated_rows / raw_records)) * 100, 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate dashboard-friendly ANATEL CSV compaction.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--progress-every", type=int, default=250000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = simulate(
        args.csv_path,
        limit=args.limit,
        progress_every=args.progress_every,
    )
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
