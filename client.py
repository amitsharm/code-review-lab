"""Receipt rendering for the existing quote contract."""
def receipt(quote_response):
    return f"Total: ${quote_response['total_cents'] / 100:.2f}"
