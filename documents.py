"""Document access at the service boundary."""
def get_document(documents, document_id, tenant_id):
    document = documents.get(document_id)
    if document is None or document["tenant_id"] != tenant_id:
        raise PermissionError("Document unavailable")
    return document["body"]
