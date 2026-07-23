"""Empty Grep pattern must error, not match every file (ripgrep parity)."""


def test_empty_pattern_rejected(system_state, sample_files):
    from tools.grep_tool import GrepTool

    result = GrepTool(system_state).execute(
        {
            "pattern": "",
            "path": str(sample_files["text_file1"].parent),
            "output_mode": "files_with_matches",
        }
    )
    assert result.data.get("error") == "Empty pattern not allowed"
    assert result.data.get("matches") is None or "matches" not in result.data


def test_nonempty_pattern_still_matches(system_state, sample_files):
    from tools.grep_tool import GrepTool

    result = GrepTool(system_state).execute(
        {
            "pattern": "ERROR",
            "path": str(sample_files["text_file1"].parent),
            "output_mode": "files_with_matches",
        }
    )
    assert result.data["matches"] >= 1
    assert "error" not in result.data
