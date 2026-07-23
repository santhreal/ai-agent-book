"""Regression: chunk_size=0 or chunk_size==overlap must not crash range()."""
import sys
import types
from dataclasses import dataclass


def _stub():
    sys.modules.setdefault("requests", types.ModuleType("requests"))
    cfg = types.ModuleType("config")

    @dataclass
    class ChunkingConfig:
        chunk_size: int = 1000
        chunk_overlap: int = 100
        max_chunk_size: int = 2000
        min_chunk_size: int = 1
        respect_paragraph_boundary: bool = True

    cfg.ChunkingConfig = ChunkingConfig
    cfg.KnowledgeBaseConfig = object
    cfg.KnowledgeBaseType = object
    sys.modules["config"] = cfg


_stub()

from chunking import ChunkingConfig, DocumentChunker  # noqa: E402


def test_chunk_size_zero_long_unsplittable_sentence():
    cfg = ChunkingConfig(chunk_size=0, max_chunk_size=40, min_chunk_size=1)
    chunker = DocumentChunker(cfg)
    text = "alpha" * 80
    chunks = chunker.chunk_text(text, doc_id="d1")
    assert isinstance(chunks, list)
    assert len(chunks) >= 1


def test_chunk_size_equals_overlap_size_based():
    cfg = ChunkingConfig(
        chunk_size=50,
        chunk_overlap=50,
        min_chunk_size=1,
        respect_paragraph_boundary=False,
    )
    chunker = DocumentChunker(cfg)
    chunks = chunker.chunk_text("hello world " * 20, doc_id="d2")
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    assert all(c["text"] for c in chunks)
