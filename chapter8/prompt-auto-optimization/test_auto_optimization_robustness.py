from coding_agent import _apply_one


def test_apply_one_none_values():
    content = "Hello world"

    new_content, err = _apply_one(content, None, "new")
    assert new_content == content
    assert err == "old_str and new_str must be strings"

    new_content, err = _apply_one(content, "world", None)
    assert new_content == content
    assert err == "old_str and new_str must be strings"
