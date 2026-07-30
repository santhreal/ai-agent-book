import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "user_request",
    [
        "我想订一张去北京的机票",
        "我想订一张去北京的往返机票",
    ],
)
def test_offline_cli_extracts_only_the_destination(user_request, tmp_path):
    demo = Path(__file__).with_name("demo.py")
    result = subprocess.run(
        [
            sys.executable,
            str(demo),
            "--offline",
            "--request",
            user_request,
            "--output",
            str(tmp_path / "form.html"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert '"destination_city": "北京"' in result.stdout
