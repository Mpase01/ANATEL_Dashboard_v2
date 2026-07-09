"""Import ANATEL CSV records in small measured batches.

This script is intentionally conservative. It requires an explicit limit by
default and commits each batch separately, so a large CSV can be tested in
controlled slices before a full import.
"""

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
from app.importer.anatel_csv import SubscriptionRecord, inspect_csv, iter_subscription_records
from app.importer.database_writer import ImportDatabaseWriter, ImportFileInfo
from app.importer.persistence import (
    build_provider_alias_rows,
    build_provider_rows,
    build_subscription_rows,
)


def build_limited_file_hash(path: Path, *, limit: int | None) -> str:
    stat = path.stat()
    limit_label = "all" if limit is None else str(limit)
    fingerprint = f"{path.name}|{stat.st_size}|{int(stat.st_mtime)}|batched:{limit_label}"
    return hashlib.sha1(fingerprint.encode("utf-8")).hexdigest()


def chunks(records, size: int):
    iterator = iter(records)
    while True:
        batch = list(itertools.islice(iterator, size))
        if not batch:
            break
        yield batch


def limited_records(path: Path, limit: int | None):
    iterator = iter_subscription_records(path)
    if limit is None:
        return iterator
    return itertools.islice(iterator, limit)


def import_batch(
    *,
    writer: ImportDatabaseWriter,
    records: list[SubscriptionRecord],
    import_batch_id: int,
    import_file_id: int,
) -> int:
    provider_rows = build_provider_rows(records)
    alias_rows = build_provider_alias_rows(records)
    provider_ids_by_cnpj = writer.upsert_providers(provider_rows)
    writer.upsert_provider_aliases(alias_rows, provider_ids_by_cnpj=provider_ids_by_cnpj)
    subscription_rows = build_subscription_rows(
        records,
        provider_ids_by_cnpj=provider_ids_by_cnpj,
        import_batch_id=import_batch_id,
        import_file_id=import_file_id,
    )
    return writer.upsert_subscription_rows(subscription_rows)


def run_import(csv_path: Path, *, limit: int | None, batch_size: int, dry_run: bool) -> dict[str, object]:
    metadata = inspect_csv(csv_path)
    started_at = time.monotonic()
    total_read = 0
    total_written = 0
    batch_count = 0

    if dry_run:
        for batch in chunks(limited_records(csv_path, limit), batch_size):
            batch_count += 1
            total_read += len(batch)
            print(f"dry_run_batch={batch_count} normalized_records={len(batch)}")
        return {
            "dry_run": True,
            "batches": batch_count,
            "normalized_records": total_read,
            "written_records": 0,
            "elapsed_seconds": round(time.monotonic() - started_at, 2),
        }

    with session_scope() as session:
        writer = ImportDatabaseWriter(session)
        import_batch_id = writer.create_batch()
        import_file_id = writer.upsert_import_file(
            import_batch_id=import_batch_id,
            file_info=ImportFileInfo(
                file_name=csv_path.name,
                file_hash=build_limited_file_hash(csv_path, limit=limit),
                file_size_bytes=csv_path.stat().st_size,
                detected_delimiter=metadata.delimiter,
                detected_encoding=metadata.encoding,
                detected_months=list(metadata.month_columns),
            ),
        )
        session.commit()

    try:
        for batch in chunks(limited_records(csv_path, limit), batch_size):
            batch_count += 1
            total_read += len(batch)
            with session_scope() as session:
                writer = ImportDatabaseWriter(session)
                written = import_batch(
                    writer=writer,
                    records=batch,
                    import_batch_id=import_batch_id,
                    import_file_id=import_file_id,
                )
                total_written += written
                session.commit()
                print(
                    f"batch={batch_count} normalized_records={len(batch)} "
                    f"written_records={written} total_written={total_written}"
                )

        with session_scope() as session:
            writer = ImportDatabaseWriter(session)
            writer.finish_batch(
                import_batch_id=import_batch_id,
                rows_read=total_read,
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
                rows_read=total_read,
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
        "batches": batch_count,
        "normalized_records": total_read,
        "written_records": total_written,
        "elapsed_seconds": round(time.monotonic() - started_at, 2),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import ANATEL CSV records in measured batches.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=1000)
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
