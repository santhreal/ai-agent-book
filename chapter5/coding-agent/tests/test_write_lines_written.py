"""Write lines_written must use splitlines (empty file is 0 lines)."""
from tools.write_tool import WriteTool


def test_empty_content_reports_zero_lines(system_state, temp_dir):
    path = temp_dir / "empty.txt"
    result = WriteTool(system_state).execute(
        {"file_path": str(path), "content": ""}
    )
    assert result.success
    assert path.read_text(encoding="utf-8") == ""
    assert result.data["bytes_written"] == 0
    assert result.data["lines_written"] == 0


def test_trailing_newline_does_not_invent_extra_line(system_state, temp_dir):
    path = temp_dir / "lines.txt"
    content = "a\nb\n"
    result = WriteTool(system_state).execute(
        {"file_path": str(path), "content": content}
    )
    assert result.success
    assert result.data["lines_written"] == 2
    assert path.read_text(encoding="utf-8") == content


def test_single_line_without_newline(system_state, temp_dir):
    path = temp_dir / "one.txt"
    result = WriteTool(system_state).execute(
        {"file_path": str(path), "content": "hello"}
    )
    assert result.success
    assert result.data["lines_written"] == 1
