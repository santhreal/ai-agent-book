import pytest
import sys
import os

sys.path.insert(0, os.path.abspath("chapter8/trajectory-verifier"))

from verifier import ProcessVerifier, FAIL, PASS


def test_process_verifier_privacy_numeric_zero_sensitive_value():
    """Contract: ProcessVerifier detects privacy leaks of numeric zero sensitive values."""
    trajectory = {
        "messages": [
            {"role": "assistant", "content": "Your security code is 0."}
        ],
        "sensitive_values": [
            {"label": "security code", "value": 0}
        ]
    }
    pv = ProcessVerifier()
    res = pv._privacy(trajectory)
    assert res.verdict == FAIL
    assert res.evidence == ["assistant exposed security code"]
