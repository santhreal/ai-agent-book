import pytest
pytest.importorskip("numpy")
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chapter4" / "active-tool-selection"))

import semantic_router
from tool_knowledge_base import ServerDefinition, ToolDefinition
from semantic_router import SemanticRouter


def test_semantic_router_stop_words_query_produces_zero_similarity(monkeypatch):
    tool = ToolDefinition(
        name="test_tool",
        description="performs testing operations on database",
        parameters={},
        server="test_server",
    )
    server = ServerDefinition(
        name="test_server",
        description="server for database search and query operations",
        tools=[tool],
    )

    router = SemanticRouter([server])

    # Monkeypatch cosine_similarity to return NaN, simulating zero-norm TF-IDF vector similarity
    monkeypatch.setattr(
        semantic_router,
        "cosine_similarity",
        lambda req, emb: np.array([[np.nan]]),
    )

    stop_words_query = "the a in on at"

    server_routes = router._route_to_servers(stop_words_query, top_k=1)
    assert len(server_routes) == 1
    srv, srv_score = server_routes[0]
    assert not np.isnan(srv_score)
    assert srv_score == 0.0

    tool_routes = router._route_to_tools(server, stop_words_query, top_k=1)
    assert len(tool_routes) == 1
    tl, tl_score = tool_routes[0]
    assert not np.isnan(tl_score)
    assert tl_score == 0.0
