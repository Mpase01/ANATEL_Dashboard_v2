import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.importer import iter_subscription_records
from app.importer.persistence import (
    build_provider_alias_rows,
    build_provider_rows,
    build_subscription_rows,
)


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class ImporterPersistenceTest(unittest.TestCase):
    def test_builds_provider_and_subscription_rows(self):
        records = list(iter_subscription_records(FIXTURES_DIR / "sample_ascii.csv"))

        provider_rows = build_provider_rows(records)
        alias_rows = build_provider_alias_rows(records)
        subscription_rows = build_subscription_rows(
            records,
            provider_ids_by_cnpj={"12345678000190": 7},
            import_batch_id=3,
            import_file_id=5,
        )

        self.assertEqual(
            provider_rows,
            [{"cnpj": "12345678000190", "primary_name": "Exemplo Telecom"}],
        )
        self.assertEqual(
            alias_rows,
            [{"cnpj": "12345678000190", "alias_name": "Exemplo Telecom"}],
        )
        self.assertEqual(len(subscription_rows), 2)
        self.assertEqual(subscription_rows[0]["provider_id"], 7)
        self.assertEqual(subscription_rows[0]["import_batch_id"], 3)
        self.assertEqual(subscription_rows[0]["import_file_id"], 5)
        self.assertEqual(subscription_rows[0]["subscriptions_count"], 10)

    def test_raises_when_provider_id_is_missing(self):
        records = list(iter_subscription_records(FIXTURES_DIR / "sample_ascii.csv"))

        with self.assertRaises(KeyError):
            build_subscription_rows(
                records,
                provider_ids_by_cnpj={},
                import_batch_id=3,
                import_file_id=5,
            )


if __name__ == "__main__":
    unittest.main()
