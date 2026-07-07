"""Helpers that prepare imported ANATEL records for persistence."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from .anatel_csv import SubscriptionRecord


def build_provider_rows(records: Iterable[SubscriptionRecord]) -> list[dict[str, str]]:
    providers: dict[str, str] = {}
    for record in records:
        providers.setdefault(record.cnpj, record.company_name)

    return [
        {"cnpj": cnpj, "primary_name": primary_name}
        for cnpj, primary_name in sorted(providers.items())
    ]


def build_provider_alias_rows(
    records: Iterable[SubscriptionRecord],
) -> list[dict[str, str]]:
    aliases: set[tuple[str, str]] = set()
    for record in records:
        aliases.add((record.cnpj, record.company_name))

    return [
        {"cnpj": cnpj, "alias_name": alias_name}
        for cnpj, alias_name in sorted(aliases)
    ]


def build_subscription_rows(
    records: Iterable[SubscriptionRecord],
    *,
    provider_ids_by_cnpj: dict[str, int],
    import_batch_id: int,
    import_file_id: int,
) -> list[dict[str, object]]:
    rows = []
    for record in records:
        provider_id = provider_ids_by_cnpj.get(record.cnpj)
        if provider_id is None:
            raise KeyError(f"Missing provider id for CNPJ {record.cnpj}")

        row = asdict(record)
        row["provider_id"] = provider_id
        row["import_batch_id"] = import_batch_id
        row["import_file_id"] = import_file_id
        rows.append(row)

    return rows
