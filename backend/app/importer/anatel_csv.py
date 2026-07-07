"""CSV importer utilities for ANATEL fixed broadband access files."""

from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Iterator


MONTH_COLUMN_PATTERN = re.compile(r"^\d{4}-\d{2}$")


HEADER_ALIASES = {
    "cnpj": "cnpj",
    "velocidade": "speed_mbps",
    "municipio": "municipality_name",
    "uf": "state",
    "faixa de velocidade": "speed_range",
    "tecnologia": "technology",
    "empresa": "company_name",
    "porte da prestadora": "provider_size",
    "tipo de pessoa": "person_type",
    "tipo de produto": "product_type",
    "codigo ibge municipio": "municipality_code",
    "grupo economico": "economic_group",
    "meio de acesso": "access_medium",
}


SOURCE_HASH_FIELDS = (
    "cnpj",
    "speed_mbps",
    "municipality_name",
    "state",
    "speed_range",
    "technology",
    "company_name",
    "provider_size",
    "person_type",
    "product_type",
    "municipality_code",
    "economic_group",
    "access_medium",
)


@dataclass(frozen=True)
class AnatelCsvMetadata:
    path: str
    delimiter: str
    encoding: str
    columns: tuple[str, ...]
    fixed_columns: tuple[str, ...]
    month_columns: tuple[str, ...]


@dataclass(frozen=True)
class SubscriptionRecord:
    period: date
    source_row_hash: str
    cnpj: str
    company_name: str
    speed_mbps: float | None
    municipality_name: str
    state: str
    speed_range: str
    technology: str
    provider_size: str
    person_type: str
    product_type: str
    municipality_code: str
    economic_group: str
    access_medium: str
    subscriptions_count: int


class AnatelCsvError(ValueError):
    """Raised when the ANATEL CSV does not match the expected structure."""


def inspect_csv(path: str | Path) -> AnatelCsvMetadata:
    csv_path = Path(path)
    encoding = detect_encoding(csv_path)
    delimiter = detect_delimiter(csv_path, encoding)

    with csv_path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        try:
            columns = tuple(next(reader))
        except StopIteration as exc:
            raise AnatelCsvError("CSV file is empty.") from exc

    month_columns = tuple(column for column in columns if is_month_column(column))
    fixed_columns = tuple(column for column in columns if not is_month_column(column))

    if not month_columns:
        raise AnatelCsvError("No month columns were found in YYYY-MM format.")

    return AnatelCsvMetadata(
        path=str(csv_path),
        delimiter=delimiter,
        encoding=encoding,
        columns=columns,
        fixed_columns=fixed_columns,
        month_columns=month_columns,
    )


def iter_subscription_records(path: str | Path) -> Iterator[SubscriptionRecord]:
    metadata = inspect_csv(path)

    with Path(path).open("r", encoding=metadata.encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=metadata.delimiter)
        header_map = build_header_map(reader.fieldnames or [])
        validate_required_headers(header_map)

        for source_row in reader:
            normalized = normalize_source_row(source_row, header_map)
            source_row_hash = build_source_row_hash(normalized)

            for month_column in metadata.month_columns:
                subscriptions_count = parse_int(source_row.get(month_column, ""))
                if subscriptions_count <= 0:
                    continue

                yield SubscriptionRecord(
                    period=parse_period(month_column),
                    source_row_hash=source_row_hash,
                    cnpj=normalized["cnpj"],
                    company_name=normalized["company_name"],
                    speed_mbps=parse_float(normalized["speed_mbps"]),
                    municipality_name=normalized["municipality_name"],
                    state=normalized["state"],
                    speed_range=normalized["speed_range"],
                    technology=normalized["technology"],
                    provider_size=normalized["provider_size"],
                    person_type=normalized["person_type"],
                    product_type=normalized["product_type"],
                    municipality_code=normalized["municipality_code"],
                    economic_group=normalized["economic_group"],
                    access_medium=normalized["access_medium"],
                    subscriptions_count=subscriptions_count,
                )


def read_preview(path: str | Path, limit: int = 1000) -> list[SubscriptionRecord]:
    records = []
    for index, record in enumerate(iter_subscription_records(path)):
        if index >= limit:
            break
        records.append(record)
    return records


def detect_encoding(path: Path) -> str:
    raw = path.read_bytes()[:20000]
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            raw.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return "latin1"


def detect_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, newline="") as handle:
        sample = handle.read(5000)

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ";"


def is_month_column(column: str) -> bool:
    return bool(MONTH_COLUMN_PATTERN.fullmatch(column.strip()))


def normalize_header(header: str) -> str:
    without_accents = unicodedata.normalize("NFKD", header.strip())
    ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().split())


def build_header_map(headers: Iterable[str]) -> dict[str, str]:
    header_map = {}
    for header in headers:
        canonical_name = HEADER_ALIASES.get(normalize_header(header))
        if canonical_name:
            header_map[canonical_name] = header
    return header_map


def validate_required_headers(header_map: dict[str, str]) -> None:
    missing = [field for field in SOURCE_HASH_FIELDS if field not in header_map]
    if missing:
        joined = ", ".join(missing)
        raise AnatelCsvError(f"Missing required ANATEL columns: {joined}")


def normalize_source_row(row: dict[str, str], header_map: dict[str, str]) -> dict[str, str]:
    normalized = {}
    for canonical_name in SOURCE_HASH_FIELDS:
        source_header = header_map[canonical_name]
        normalized[canonical_name] = clean_text(row.get(source_header, ""))

    normalized["cnpj"] = only_digits(normalized["cnpj"])
    normalized["state"] = normalized["state"].upper()
    normalized["municipality_code"] = only_digits(normalized["municipality_code"])
    return normalized


def clean_text(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def only_digits(value: str) -> str:
    return "".join(character for character in value if character.isdigit())


def build_source_row_hash(normalized_row: dict[str, str]) -> str:
    values = [normalized_row[field] for field in SOURCE_HASH_FIELDS]
    text = "\x1f".join(values)
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def parse_period(month_column: str) -> date:
    year, month = month_column.split("-", 1)
    return date(int(year), int(month), 1)


def parse_int(value: str | None) -> int:
    text = clean_text(value)
    if not text:
        return 0

    normalized = text.replace(".", "").replace(",", ".")
    try:
        return int(round(float(normalized)))
    except ValueError:
        return 0


def parse_float(value: str | None) -> float | None:
    text = clean_text(value)
    if not text:
        return None

    normalized = text.replace(".", "").replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None
