"""Pricing rules for a small multi-tenant storefront."""
def subtotal(items):
    return sum(item["price_cents"] * item["quantity"] for item in items)

def shipping(subtotal_cents):
    return 0 if subtotal_cents >= 5000 else 500
