from replay import _eval_assertion


def test_eval_assertion_latency_under_robustness():
    # Case 1: missing threshold parameter
    assertion = {"type": "latency_under", "params": {"tool": "test_tool"}}
    traj = {"turns": [{"tool": "test_tool", "latency_ms": 100}]}
    ok, msg = _eval_assertion(assertion, traj)
    assert not ok
    assert "断言缺失阈值设置" in msg

    # Case 2: invalid threshold parameter type
    assertion = {
        "type": "latency_under",
        "params": {"tool": "test_tool", "threshold": "invalid"},
    }
    ok, msg = _eval_assertion(assertion, traj)
    assert not ok
    assert "阈值非法" in msg

    # Case 3: latency_ms is None in one of the turns
    assertion = {
        "type": "latency_under",
        "params": {"tool": "test_tool", "threshold": 150},
    }
    traj = {
        "turns": [
            {"tool": "test_tool", "latency_ms": None},
            {"tool": "test_tool", "latency_ms": 120},
        ]
    }
    ok, msg = _eval_assertion(assertion, traj)
    assert ok
    assert "最大延迟 120.0ms" in msg

    # Case 4: latency_ms is None in all turns
    traj = {"turns": [{"tool": "test_tool", "latency_ms": None}]}
    ok, msg = _eval_assertion(assertion, traj)
    assert ok
    assert "最大延迟 0.0ms" in msg
