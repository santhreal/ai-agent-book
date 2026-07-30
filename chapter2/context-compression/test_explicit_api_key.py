import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import ResearchAgent
from compression_strategies import CompressionStrategy
from config import Config


def test_research_agent_uses_explicit_api_key_without_environment_key():
    empty_keys = {
        "MOONSHOT_API_KEY": "",
        "KIMI_API_KEY": "",
        "OPENROUTER_API_KEY": "",
    }
    with (
        patch.dict(os.environ, empty_keys),
        patch("agent.OpenAI") as agent_openai,
        patch("agent.WebTools"),
        patch("compression_strategies.OpenAI") as compressor_openai,
        patch(
            "compression_strategies.tiktoken.encoding_for_model",
            return_value=MagicMock(),
        ),
    ):
        agent = ResearchAgent(
            api_key="documented-explicit-key",
            compression_strategy=CompressionStrategy.NO_COMPRESSION,
            enable_streaming=False,
        )

    expected_client_args = {
        "api_key": "documented-explicit-key",
        "base_url": Config.MOONSHOT_BASE_URL,
    }
    agent_openai.assert_called_once_with(**expected_client_args)
    compressor_openai.assert_called_once_with(**expected_client_args)
    assert agent.model == Config.MODEL_NAME
    assert agent.compressor.model == Config.MODEL_NAME
