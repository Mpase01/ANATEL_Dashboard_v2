"""Import ANATEL CSV data into the compact aggregated dashboard table."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))

from app.db.session import session_scope
from app.importer.aggregation import (
    aggregate_subscription_records_with_stats,
    build_aggregated_subscription_rows,
)
from app.importer.anatel_csv import inspect_csv, iter_subscription_records
from app.importer.database_writer import ImportDatabaseWriter, ImportFileInfo
from app.importer.persistence import build_provider_alias_rows, build_provider_rows


def build_aggregated_file_hash(path: Path, *, limit: int | None) -> str:
    stat = path.stat()
    limit_label = "all" if limit is None else str(limit)
    fingerprint = f"{path.name}|{stat.st_size}|{int(stat.st_mtime)}|aggregated:{limit_label}"
    return hashlib.sha1(fingerprint.encode("utf-8")).hexdigest()


def chunks(rows, size: int):
    iterator = iter(rows)
    while True:
        batch = list(itertools.islice(iterator, size))
        if not batch:
            break
        yield batch


def limited_records(path: Path, limit: int | None):
    records = iter_subscription_records(path)
    if limit is None:
        return records
    return itertools.islice(records, limit)


def run_import(csv_path: Path, *, limit: int | None, batch_size: int, dry_run: bool) -> dict[str, object]:
    metadata = inspect_csv(csv_path)
    started_at = time.monotonic()
    aggregation = aggregate_subscription_records_with_stats(limited_records(csv_path, limit))
    aggregated_records = aggregation.records
    raw_records_count = aggregation.raw_records_count
    raw_total = aggregation.subscriptions_sum
    aggregated_total = sum(record.subscriptions_count for record in aggregated_records)

    if dry_run:
        return {
            "dry_run": True,
            "raw_records": raw_records_count,
            "aggregated_records": len(aggregated_records),
            "reduction_percent": calculate_reduction(raw_records_count, len(aggregated_records)),
            "raw_subscriptions_sum": raw_total,
            "aggregated_subscriptions_sum": aggregated_total,
            "elapsed_seconds": round(time.monotonic() - started_at, 2),
        }

    with session_scope() as session:
        writer = ImportDatabaseWriter(session)
        import_batch_id = writer.create_batch()
        import_file_id = writer.upsert_import_file(
            import_batch_id=import_batch_id,
            file_info=ImportFileInfo(
                file_name=csv_path.name,
                file_hash=build_aggregated_file_hash(csv_path, limit=limit),
                file_size_bytes=csv_path.stat().st_size,
                detected_delimiter=metadata.delimiter,
                detected_encoding=metadata.encoding,
                detected_months=list(metadata.month_columns),
            ),
        )
        session.commit()

    total_written = 0
    batch_count = 0
    try:
        for batch in chunks(aggregated_records, batch_size):
            batch_count += 1
            provider_rows = build_provider_rows(batch)
            alias_rows = build_provider_alias_rows(batch)

            with session_scope() as session:
                writer = ImportDatabaseWriter(session)
                provider_ids_by_cnpj = writer.upsert_providers(provider_rows)
                writer.upsert_provider_aliases(alias_rows, provider_ids_by_cnpj=provider_ids_by_cnpj)
                rows = build_aggregated_subscription_rows(
                    batch,
                    provider_ids_by_cnpj=provider_ids_by_cnpj,
                    import_batch_id=import_batch_id,
                    import_file_id=import_file_id,
                )
                written = writer.upsert_aggregated_subscription_rows(rows)
                total_written += written
                session.commit()
                print(
                    f"batch={batch_count} aggregated_records={len(batch)} "
                    f"written_records={written} total_written={total_written}"
                )

        with session_scope() as session:
            writer = ImportDatabaseWriter(session)
            writer.finish_batch(
                import_batch_id=import_batch_id,
                rows_read=raw_records_count,
                rows_inserted=total_written,
                rows_updated=0,
                rows_skipped=0,
            )
            session.commit()
    except Exception as exc:
        with session_scope() as session:
            writer = ImportDatabaseWriter(session)
            writer.finish_batch(
                import_batch_id=import_batch_id,
                rows_read=raw_records_count,
                rows_inserted=total_written,
                rows_updated=0,
                rows_skipped=0,
                status="failed",
                error_message=str(exc)[:1000],
            )
            session.commit()
        raise

    return {
        "dry_run": False,
        "import_batch_id": import_batch_id,
        "import_file_id": import_file_id,
        "raw_records": raw_records_count,
        "aggregated_records": len(aggregated_records),
        "written_records": total_written,
        "batches": batch_count,
        "reduction_percent": calculate_reduction(raw_records_count, len(aggregated_records)),
        "raw_subscriptions_sum": raw_total,
        "aggregated_subscriptions_sum": aggregated_total,
        "elapsed_seconds": round(time.monotonic() - started_at, 2),
    }


def calculate_reduction(raw_records: int, aggregated_records: int) -> float:
    if raw_records == 0:
        return 0.0
    return round((1 - (aggregated_records / raw_records)) * 100, 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import ANATEL CSV records into the aggregated dashboard table.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=5000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--full-import", action="store_true")
    args = parser.parse_args()

    if args.full_import:
        args.limit = None
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be greater than zero.")
    if args.batch_size <= 0:
        parser.error("--batch-size must be greater than zero.")
    return args


def main() -> None:
    args = parse_args()
    result = run_import(
        args.csv_path,
        limit=args.limit,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
    )
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
