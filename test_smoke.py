import unittest
from pricing import subtotal, shipping
from documents import get_document
from api import quote
from cache import CatalogCache
from labels import normalize_label

class SmokeTests(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(subtotal([{"price_cents": 100, "quantity": 1}]), 100)
    def test_shipping_above_threshold(self):
        self.assertEqual(shipping(6000), 0)
    def test_owned_document(self):
        self.assertEqual(get_document({"a": {"tenant_id": "north", "body": "hello"}}, "a", "north"), "hello")
    def test_quote_exists(self):
        self.assertIsInstance(quote([{"price_cents": 100, "quantity": 1}]), dict)
    def test_cache_same_tenant(self):
        cache = CatalogCache()
        self.assertEqual(cache.lookup("north", "item", lambda t, i: t), "north")
        self.assertEqual(cache.lookup("north", "item", lambda t, i: "ignored"), "north")
    def test_label(self):
        self.assertEqual(normalize_label(" Hello "), "hello")

if __name__ == "__main__":
    unittest.main()
