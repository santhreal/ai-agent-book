from harness import layer2_discovery, layer4_reuse


def test_harness_robustness_empty_steps():
    task = {"id": "task-01", "goal": "test goal", "tool_name": "test_tool"}
    trajectory = {}  # missing steps

    # Layer 2 should handle empty/missing steps gracefully without crashing
    res2 = layer2_discovery(task, trajectory)
    assert res2["score"] == 0.25

    # Layer 4 should handle empty/missing steps gracefully
    res4 = layer4_reuse(task, trajectory)
    assert res4["score"] == 0.0 or res4["score"] is None


def test_harness_robustness_malformed_steps():
    task = {"id": "task-01", "goal": "test goal", "tool_name": "test_tool"}
    trajectory = {
        "steps": [
            "not a dict",
            {"action": "search"},  # missing query
            {"action": "select_library"},  # missing library
            None,
        ]
    }

    res2 = layer2_discovery(task, trajectory)
    assert "score" in res2

    res4 = layer4_reuse(task, trajectory)
    assert "score" in res4
