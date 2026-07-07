"""Database writer for ANATEL import batches.

This module keeps the database write rules in one place. The importer reads and
normalizes the CSV; this writer persists the normalized rows into PostgreSQL.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class ImportFileInfo:
    file_name: str
    file_hash: str
    file_size_bytes: int
    detected_delimiter: str
    detected_encoding: str
    detected_months: list[str]


class ImportDatabaseWriter:
    """Persist one controlled ANATEL import into the database."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_batch(self, *, status: str = "running") -> int:
        result = self.session.execute(
            text(
                """
                insert into public.import_batches(status)
                values (:status)
                returning id
                """
            ),
            {"status": status},
        )
        return int(result.scalar_one())

    def finish_batch(
        self,
        *,
        import_batch_id: int,
        rows_read: int,
        rows_inserted: int,
        rows_updated: int,
        rows_skipped: int,
        status: str = "completed",
        error_message: str | None = None,
    ) -> None:
        self.session.execute(
            text(
                """
                update public.import_batches
                set status = :status,
                    rows_read = :rows_read,
                    rows_inserted = :rows_inserted,
                    rows_updated = :rows_updated,
                    rows_skipped = :rows_skipped,
                    error_message = :error_message,
                    finished_at = now()
                where id = :import_batch_id
                """
            ),
            {
                "import_batch_id": import_batch_id,
                "status": status,
                "rows_read": rows_read,
                "rows_inserted": rows_inserted,
                "rows_updated": rows_updated,
                "rows_skipped": rows_skipped,
                "error_message": error_message,
            },
        )

    def upsert_providers(self, provider_rows: Iterable[dict[str, str]]) -> dict[str, int]:
        provider_ids_by_cnpj: dict[str, int] = {}
        for row in provider_rows:
            result = self.session.execute(
                text(
                    """
                    insert into public.providers(cnpj, primary_name)
                    values (:cnpj, :primary_name)
                    on conflict (cnpj) do update
                    set primary_name = excluded.primary_name,
                        updated_at = now()
                    returning id
                    """
                ),
                row,
            )
            provider_ids_by_cnpj[row["cnpj"]] = int(result.scalar_one())

        return provider_ids_by_cnpj

    def upsert_provider_aliases(
        self,
        alias_rows: Iterable[dict[str, str]],
        *,
        provider_ids_by_cnpj: dict[str, int],
    ) -> None:
        for row in alias_rows:
            provider_id = provider_ids_by_cnpj[row["cnpj"]]
            self.session.execute(
                text(
                    """
                    insert into public.provider_aliases(provider_id, alias_name)
                    values (:provider_id, :alias_name)
                    on conflict (provider_id, alias_name) do nothing
                    """
                ),
                {"provider_id": provider_id, "alias_name": row["alias_name"]},
            )

    def upsert_import_file(
        self,
        *,
        import_batch_id: int,
        file_info: ImportFileInfo,
    ) -> int:
        result = self.session.execute(
            text(
                """
                insert into public.import_files(
                    import_batch_id,
                    file_name,
                    file_hash,
                    file_size_bytes,
                    detected_delimiter,
                    detected_encoding,
                    detected_months
                )
                values (
                    :import_batch_id,
                    :file_name,
                    :file_hash,
                    :file_size_bytes,
                    :detected_delimiter,
                    :detected_encoding,
                    :detected_months
                )
                on conflict (file_hash) do update
                set import_batch_id = excluded.import_batch_id,
                    file_name = excluded.file_name,
                    file_size_bytes = excluded.file_size_bytes,
                    detected_delimiter = excluded.detected_delimiter,
                    detected_encoding = excluded.detected_encoding,
                    detected_months = excluded.detected_months
                returning id
                """
            ),
            {
                "import_batch_id": import_batch_id,
                "file_name": file_info.file_name,
                "file_hash": file_info.file_hash,
                "file_size_bytes": file_info.file_size_bytes,
                "detected_delimiter": file_info.detected_delimiter,
                "detected_encoding": file_info.detected_encoding,
                "detected_months": file_info.detected_months,
            },
        )
        return int(result.scalar_one())

    def upsert_subscription_rows(self, rows: Iterable[dict[str, object]]) -> int:
        written = 0
        for row in rows:
            self.session.execute(
                text(
                    """
                    insert into public.subscription_records(
                        provider_id,
                        import_batch_id,
                        import_file_id,
                        period,
                        source_row_hash,
                        cnpj,
                        company_name,
                        speed_mbps,
                        municipality_name,
                        state,
                        speed_range,
                        technology,
                        provider_size,
                        person_type,
                        product_type,
                        municipality_code,
                        economic_group,
                        access_medium,
                        subscriptions_count
                    )
                    values (
                        :provider_id,
                        :import_batch_id,
                        :import_file_id,
                        :period,
                        :source_row_hash,
                        :cnpj,
                        :company_name,
                        :speed_mbps,
                        :municipality_name,
                        :state,
                        :speed_range,
                        :technology,
                        :provider_size,
                        :person_type,
                        :product_type,
                        :municipality_code,
                        :economic_group,
                        :access_medium,
                        :subscriptions_count
                    )
                    on conflict (period, source_row_hash) do update
                    set provider_id = excluded.provider_id,
                        import_batch_id = excluded.import_batch_id,
                        import_file_id = excluded.import_file_id,
                        company_name = excluded.company_name,
                        speed_mbps = excluded.speed_mbps,
                        municipality_name = excluded.municipality_name,
                        state = excluded.state,
                        speed_range = excluded.speed_range,
                        technology = excluded.technology,
                        provider_size = excluded.provider_size,
                        person_type = excluded.person_type,
                        product_type = excluded.product_type,
                        municipality_code = excluded.municipality_code,
                        economic_group = excluded.economic_group,
                        access_medium = excluded.access_medium,
                        subscriptions_count = excluded.subscriptions_count,
                        updated_at = now()
                    """
                ),
                row,
            )
            written += 1

        return written
