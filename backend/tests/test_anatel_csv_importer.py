import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.importer import inspect_csv, iter_subscription_records


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class AnatelCsvImporterTest(unittest.TestCase):
    def test_detects_months_and_normalizes_nonzero_records(self):
        path = FIXTURES_DIR / "sample_ascii.csv"

        metadata = inspect_csv(path)
        self.assertEqual(metadata.delimiter, ";")
        self.assertEqual(metadata.month_columns, ("2026-01", "2026-02", "2026-03"))

        records = list(iter_subscription_records(path))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].period, date(2026, 1, 1))
        self.assertEqual(records[0].cnpj, "12345678000190")
        self.assertEqual(records[0].state, "SP")
        self.assertEqual(records[0].subscriptions_count, 10)
        self.assertEqual(records[1].period, date(2026, 3, 1))
        self.assertEqual(records[1].subscriptions_count, 12)
        self.assertEqual(records[0].source_row_hash, records[1].source_row_hash)

    def test_accepts_accented_real_headers(self):
        path = FIXTURES_DIR / "sample_accented.csv"

        records = list(iter_subscription_records(path))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].municipality_name, "Lagoa Formosa")
        self.assertEqual(records[0].municipality_code, "3137502")


if __name__ == "__main__":
    unittest.main()
