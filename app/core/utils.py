def serialize_document(document):
    if document:
        document.pop("_id", None)

    return document