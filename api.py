"""Quote API response consumed by client.py."""
from pricing import subtotal, shipping

def quote(items):
    amount = subtotal(items)
    return {"total_cents": amount + shipping(amount)}
