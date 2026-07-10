"""Build dashboard-friendly aggregate rows from normalized ANATEL records."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
import unicodedata

from .anatel_csv import SubscriptionRecord


@dataclass(frozen=True)
class AggregatedSubscriptionRecord:
    cnpj: str
    company_name: str
    economic_group: str
    period: date
    municipality_code: str
    municipality_name: str
    state: str
    access_medium: str
    person_type: str
    subscriptions_count: int


@dataclass(frozen=True)
class AggregationResult:
    records: list[AggregatedSubscriptionRecord]
    raw_records_count: int
    subscriptions_sum: int


def aggregate_subscription_records(
    records: Iterable[SubscriptionRecord],
) -> list[AggregatedSubscriptionRecord]:
    return aggregate_subscription_records_with_stats(records).records


def aggregate_subscription_records_with_stats(
    records: Iterable[SubscriptionRecord],
) -> AggregationResult:
    totals: defaultdict[tuple[object, ...], int] = defaultdict(int)
    raw_records_count = 0
    subscriptions_sum = 0

    for record in records:
        raw_records_count += 1
        subscriptions_sum += record.subscriptions_count
        key = (
            record.cnpj,
            record.company_name,
            record.economic_group,
            record.period,
            record.municipality_code,
            record.municipality_name,
            record.state,
            simplify_access_medium(record.access_medium),
            record.person_type,
        )
        totals[key] += record.subscriptions_count

    aggregated_records = [
        AggregatedSubscriptionRecord(
            cnpj=str(cnpj),
            company_name=str(company_name),
            economic_group=str(economic_group),
            period=period,
            municipality_code=str(municipality_code),
            municipality_name=str(municipality_name),
            state=str(state),
            access_medium=str(access_medium),
            person_type=str(person_type),
            subscriptions_count=subscriptions_count,
        )
        for (
            cnpj,
            company_name,
            economic_group,
            period,
            municipality_code,
            municipality_name,
            state,
            access_medium,
            person_type,
        ), subscriptions_count in sorted(totals.items())
    ]

    return AggregationResult(
        records=aggregated_records,
        raw_records_count=raw_records_count,
        subscriptions_sum=subscriptions_sum,
    )


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
                "economic_group": record.economic_group,
                "period": record.period,
                "municipality_code": record.municipality_code,
                "municipality_name": record.municipality_name,
                "state": record.state,
                "access_medium": record.access_medium,
                "person_type": record.person_type,
                "subscriptions_count": record.subscriptions_count,
            }
        )

    return rows


def simplify_access_medium(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().lower())
    text = normalized.encode("ascii", "ignore").decode("ascii")
    if "fibra" in text:
        return "Fibra"
    if "radio" in text:
        return "Radio"
    if "coaxial" in text or "cabo" in text:
        return "Cabo coaxial"
    return "Outros"
