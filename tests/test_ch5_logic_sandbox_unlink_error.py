import importlib.util
from pathlib import Path
import pytest

logic_sandbox_path = Path(__file__).resolve().parent.parent / "chapter5" / "code-for-logic" / "sandbox.py"
spec = importlib.util.spec_from_file_location("logic_sandbox", logic_sandbox_path)
logic_sandbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic_sandbox)
run_python = logic_sandbox.run_python


def test_logic_sandbox_handles_unlink_error(monkeypatch):
    def fake_unlink(path):
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")

    monkeypatch.setattr("os.unlink", fake_unlink)

    output = run_python("print('test output')")
    assert output == "test output"
