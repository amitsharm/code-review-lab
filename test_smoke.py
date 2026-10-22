import unittest
from unittest.mock import Mock, call
from pricing import subtotal, shipping
from documents import get_document
from api import quote
from cache import CatalogCache
from client import receipt
from labels import normalize_label

class SmokeTests(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(subtotal([{"price_cents": 100, "quantity": 1}]), 100)
    def test_subtotal_with_quantities(self):
        items = [{"price_cents": 100, "quantity": 3}, {"price_cents": 400, "quantity": 2}]
        self.assertEqual(subtotal(items), 1100)
    def test_shipping_above_threshold(self):
        self.assertEqual(shipping(6000), 0)
    def test_shipping_threshold(self):
        for amount, expected in [(4999, 500), (5000, 0), (5001, 0)]:
            with self.subTest(amount=amount):
                self.assertEqual(shipping(amount), expected)
    def test_owned_document(self):
        self.assertEqual(get_document({"a": {"tenant_id": "north", "body": "hello"}}, "a", "north"), "hello")
    def test_missing_document(self):
        with self.assertRaisesRegex(PermissionError, "Document unavailable"):
            get_document({}, "missing", "north")
    def test_cross_tenant_document(self):
        documents = {"a": {"tenant_id": "north", "body": "hello"}}
        with self.assertRaisesRegex(PermissionError, "Document unavailable"):
            get_document(documents, "a", "south")
    def test_quote_exists(self):
        self.assertIsInstance(quote([{"price_cents": 100, "quantity": 1}]), dict)
    def test_quote_receipt(self):
        for price, quantity, total in [(100, 2, 700), (2500, 2, 5000), (3000, 2, 6000)]:
            with self.subTest(price=price, quantity=quantity):
                response = quote([{"price_cents": price, "quantity": quantity}])
                self.assertEqual(response, {"total_cents": total})
                self.assertEqual(receipt(response), f"Total: ${total / 100:.2f}")
    def test_cache_same_tenant(self):
        cache = CatalogCache()
        self.assertEqual(cache.lookup("north", "item", lambda t, i: t), "north")
        self.assertEqual(cache.lookup("north", "item", lambda t, i: "ignored"), "north")
    def test_cache_cross_tenant(self):
        cache = CatalogCache()
        fetch = Mock(side_effect=lambda tenant, item: f"{tenant}:{item}")
        for tenant in ["north", "south", "north", "south"]:
            self.assertEqual(cache.lookup(tenant, "item", fetch), f"{tenant}:item")
        self.assertEqual(fetch.call_args_list, [call("north", "item"), call("south", "item")])
    def test_label(self):
        self.assertEqual(normalize_label(" Hello "), "hello")

if __name__ == "__main__":
    unittest.main()
