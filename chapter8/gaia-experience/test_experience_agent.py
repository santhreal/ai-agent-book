import sys
import os

# Add paths to sys.path so imports resolve
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "AWorld"))

from aworld.config.conf import AgentConfig  # noqa: E402
from experience_agent import ExperienceAgent  # noqa: E402


def test_is_similar_robustness():
    # Instantiate default AgentConfig using the correct path
    conf = AgentConfig()
    agent = ExperienceAgent(conf=conf)

    # Verify similar method handles None/non-string inputs gracefully
    assert not agent._is_similar(None, "test")
    assert not agent._is_similar("test", None)
    assert not agent._is_similar(None, None)
    assert not agent._is_similar(123, "test")

    # Verify correct string similarity still works
    assert agent._is_similar("what is bitcoin", "tell me what is bitcoin price")
