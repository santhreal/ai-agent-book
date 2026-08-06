"""Regression test: updating a document in DocumentStore must clear stale metadata index entries."""
import os
import sys

sys.path.insert(0, os.path.abspath("chapter3/retrieval-pipeline"))

from document_store import DocumentStore


def test_add_document_clears_stale_metadata_index():
    store = DocumentStore()
    store.add_document("doc1", "first text", {"author": "Alice", "topic": "AI"})
    assert "author" in store.metadata_index
    assert "doc1" in store.metadata_index["author"]

    # Update doc1 without 'author'
    store.add_document("doc1", "second text", {"topic": "AI"})
    assert "author" not in store.metadata_index, (
        f"Stale metadata key 'author' was not removed from metadata_index: {store.metadata_index}"
    )

    # Delete doc1 and verify no ghost entries remain
    store.delete_document("doc1")
    assert store.metadata_index == {}, (
        f"Expected metadata_index to be empty after deletion, got: {store.metadata_index}"
    )
