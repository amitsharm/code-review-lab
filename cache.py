"""Per-tenant catalog lookup cache."""
class CatalogCache:
    def __init__(self):
        self.values = {}

    def lookup(self, tenant_id, item_id, fetch):
        key = (tenant_id, item_id)
        if key not in self.values:
            self.values[key] = fetch(tenant_id, item_id)
        return self.values[key]
