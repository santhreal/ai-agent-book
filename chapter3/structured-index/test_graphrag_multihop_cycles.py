"""Regression: multi_hop_search must avoid cyclic paths and self-target loops."""
import sys
import types
from dataclasses import dataclass
import networkx as nx


def _stub_graphrag_deps() -> None:
    mods = [
        "openai",
        "sentence_transformers",
        "loguru",
        "pandas",
        "tqdm",
        "sklearn",
        "sklearn.metrics",
        "sklearn.metrics.pairwise",
        "config",
    ]
    for name in mods:
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["sklearn.metrics.pairwise"].cosine_similarity = lambda *a, **k: [[1.0]]
    sys.modules["openai"].OpenAI = object
    sys.modules["sentence_transformers"].SentenceTransformer = object
    sys.modules["loguru"].logger = types.SimpleNamespace(
        info=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        error=lambda *a, **k: None,
    )
    sys.modules["tqdm"].tqdm = lambda x, **k: x

    @dataclass
    class GraphRAGConfig:
        pass

    sys.modules["config"].GraphRAGConfig = GraphRAGConfig


_stub_graphrag_deps()

from graphrag_indexer import GraphRAGIndexer, Entity  # noqa: E402


def test_multi_hop_search_prevents_cycles_and_self_target():
    indexer = GraphRAGIndexer.__new__(GraphRAGIndexer)
    indexer.entities = {
        "e1": Entity("e1", "Intel CPU", "component", "desc1", None, {}),
        "e2": Entity("e2", "RAX Register", "register", "desc2", None, {}),
        "e3": Entity("e3", "ALU", "component", "desc3", None, {}),
    }
    indexer.graph = nx.Graph()
    for eid in indexer.entities:
        indexer.graph.add_node(eid)
    indexer.graph.add_edge("e1", "e2", type="uses")
    indexer.graph.add_edge("e2", "e3", type="uses")
    indexer.graph.add_edge("e3", "e1", type="connects_to")

    results = indexer.multi_hop_search("Intel CPU", max_hops=4)

    # 1. Start entity should never appear as a target
    target_names = [r["target"] for r in results]
    assert "Intel CPU" not in target_names

    # 2. Each path must be simple (no node revisited)
    for r in results:
        visited = ["Intel CPU"] + [step["target"] for step in r["path"]]
        assert len(visited) == len(set(visited)), f"Cycle detected in path: {visited}"

    # 3. Check exact valid acyclic paths
    expected_targets = {"RAX Register", "ALU"}
    assert set(target_names) == expected_targets
