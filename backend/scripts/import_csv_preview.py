"""Import a small ANATEL CSV preview into the configured database.

This script is intentionally limited by default. It is useful for validating the
full path from a real CSV file to PostgreSQL before running a complete import.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from app.db.session import session_scope
from app.importer.anatel_csv import inspect_csv, read_preview
from app.importer.database_writer import ImportDatabaseWriter, ImportFileInfo
from app.importer.persistence import (
    build_provider_alias_rows,
    build_provider_rows,
    build_subscription_rows,
)


def build_preview_file_hash(path: Path, *, limit: int) -> str:
    stat = path.stat()
    fingerprint = f"{path.name}|{stat.st_size}|{int(stat.st_mtime)}|preview:{limit}"
    return hashlib.sha1(fingerprint.encode("utf-8")).hexdigest()


def import_preview(csv_path: Path, *, limit: int) -> dict[str, int]:
    metadata = inspect_csv(csv_path)
    records = read_preview(csv_path, limit=limit)

    with session_scope() as session:
        writer = ImportDatabaseWriter(session)
        import_batch_id = writer.create_batch()

        provider_rows = build_provider_rows(records)
        alias_rows = build_provider_alias_rows(records)
        provider_ids_by_cnpj = writer.upsert_providers(provider_rows)
        writer.upsert_provider_aliases(
            alias_rows,
            provider_ids_by_cnpj=provider_ids_by_cnpj,
        )

        import_file_id = writer.upsert_import_file(
            import_batch_id=import_batch_id,
            file_info=ImportFileInfo(
                file_name=csv_path.name,
                file_hash=build_preview_file_hash(csv_path, limit=limit),
                file_size_bytes=csv_path.stat().st_size,
                detected_delimiter=metadata.delimiter,
                detected_encoding=metadata.encoding,
                detected_months=list(metadata.month_columns),
            ),
        )

        subscription_rows = build_subscription_rows(
            records,
            provider_ids_by_cnpj=provider_ids_by_cnpj,
            import_batch_id=import_batch_id,
            import_file_id=import_file_id,
        )
        written_rows = writer.upsert_subscription_rows(subscription_rows)
        writer.finish_batch(
            import_batch_id=import_batch_id,
            rows_read=len(records),
            rows_inserted=written_rows,
            rows_updated=0,
            rows_skipped=0,
        )
        session.commit()

    return {
        "import_batch_id": import_batch_id,
        "import_file_id": import_file_id,
        "normalized_records": len(records),
        "written_records": written_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a limited ANATEL CSV preview.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()

    result = import_preview(args.csv_path, limit=args.limit)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
