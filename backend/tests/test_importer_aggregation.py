import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.importer.aggregation import (
    aggregate_subscription_records,
    build_aggregated_subscription_rows,
)
from app.importer.anatel_csv import iter_subscription_records


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class ImporterAggregationTest(unittest.TestCase):
    def test_aggregates_duplicate_dashboard_dimensions_without_losing_sum(self):
        records = list(iter_subscription_records(FIXTURES_DIR / "sample_ascii.csv"))
        duplicate = replace(records[0], subscriptions_count=4)

        aggregated = aggregate_subscription_records([records[0], duplicate, records[1]])

        self.assertEqual(len(aggregated), 2)
        self.assertEqual(sum(record.subscriptions_count for record in aggregated), 26)
        self.assertEqual(aggregated[0].subscriptions_count, 14)
        self.assertEqual(aggregated[1].subscriptions_count, 12)

    def test_builds_aggregated_database_rows(self):
        records = list(iter_subscription_records(FIXTURES_DIR / "sample_ascii.csv"))
        aggregated = aggregate_subscription_records(records)

        rows = build_aggregated_subscription_rows(
            aggregated,
            provider_ids_by_cnpj={"12345678000190": 7},
            import_batch_id=3,
            import_file_id=5,
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["provider_id"], 7)
        self.assertEqual(rows[0]["import_batch_id"], 3)
        self.assertEqual(rows[0]["import_file_id"], 5)
        self.assertEqual(rows[0]["person_type"], "Pessoa Fisica")
        self.assertEqual(rows[0]["access_medium"], "Fibra")

    def test_raises_when_provider_id_is_missing(self):
        records = list(iter_subscription_records(FIXTURES_DIR / "sample_ascii.csv"))
        aggregated = aggregate_subscription_records(records)

        with self.assertRaises(KeyError):
            build_aggregated_subscription_rows(
                aggregated,
                provider_ids_by_cnpj={},
                import_batch_id=3,
                import_file_id=5,
            )


if __name__ == "__main__":
    unittest.main()
