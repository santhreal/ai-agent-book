import pytest
from multilang_executor import LanguageExecutor, ExecutionStatus


@pytest.mark.asyncio
async def test_large_output_preservation():
    executor = LanguageExecutor()
    code = "import sys\nfor i in range(5000):\n    print(f'Line {i}')"
    result = await executor.execute_code(code, "python", timeout=10.0)
    assert result["status"] == ExecutionStatus.SUCCESS
    stdout = result["stdout"]
    assert len(stdout.splitlines()) == 5000
    assert "Line 0" in stdout
    assert "Line 4999" in stdout


@pytest.mark.asyncio
async def test_timeout_output_preservation():
    executor = LanguageExecutor()
    code = "import time\nimport sys\nprint('starting')\nsys.stdout.flush()\ntime.sleep(20)\nprint('ending')"
    result = await executor.execute_code(code, "python", timeout=2.0)
    assert result["status"] == ExecutionStatus.TIMEOUT
    assert "starting" in result["stdout"]
    assert "ending" not in result["stdout"]
