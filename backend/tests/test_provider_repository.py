import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.repositories.providers import normalize_search_query


class ProviderRepositoryTest(unittest.TestCase):
    def test_normalizes_search_query_spacing(self):
        self.assertEqual(normalize_search_query("  Exemplo   Telecom  "), "Exemplo Telecom")

    def test_normalizes_empty_search_query(self):
        self.assertEqual(normalize_search_query("   "), "")


if __name__ == "__main__":
    unittest.main()
