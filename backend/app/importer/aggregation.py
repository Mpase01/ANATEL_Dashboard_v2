"""Build dashboard-friendly aggregate rows from normalized ANATEL records."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from .anatel_csv import SubscriptionRecord


@dataclass(frozen=True)
class AggregatedSubscriptionRecord:
    cnpj: str
    company_name: str
    period: date
    municipality_code: str
    municipality_name: str
    state: str
    technology: str
    access_medium: str
    person_type: str
    subscriptions_count: int


def aggregate_subscription_records(
    records: Iterable[SubscriptionRecord],
) -> list[AggregatedSubscriptionRecord]:
    totals: defaultdict[tuple[object, ...], int] = defaultdict(int)

    for record in records:
        key = (
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
        totals[key] += record.subscriptions_count

    return [
        AggregatedSubscriptionRecord(
            cnpj=str(cnpj),
            company_name=str(company_name),
            period=period,
            municipality_code=str(municipality_code),
            municipality_name=str(municipality_name),
            state=str(state),
            technology=str(technology),
            access_medium=str(access_medium),
            person_type=str(person_type),
            subscriptions_count=subscriptions_count,
        )
        for (
            cnpj,
            company_name,
            period,
            municipality_code,
            municipality_name,
            state,
            technology,
            access_medium,
            person_type,
        ), subscriptions_count in sorted(totals.items())
    ]


def build_aggregated_subscription_rows(
    records: Iterable[AggregatedSubscriptionRecord],
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

        rows.append(
            {
                "provider_id": provider_id,
                "import_batch_id": import_batch_id,
                "import_file_id": import_file_id,
                "cnpj": record.cnpj,
                "company_name": record.company_name,
                "period": record.period,
                "municipality_code": record.municipality_code,
                "municipality_name": record.municipality_name,
                "state": record.state,
                "technology": record.technology,
                "access_medium": record.access_medium,
                "person_type": record.person_type,
                "subscriptions_count": record.subscriptions_count,
            }
        )

    return rows
