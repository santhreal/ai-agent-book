import pytest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from wiki_enhanced import get_article_history


@pytest.mark.asyncio
async def test_get_article_history_invalid_date():
    # Test invalid date type (not a string)
    res = await get_article_history("Python (programming language)", None)
    data = json.loads(res.text)
    assert not data["success"]
    assert "date must be a YYYY/MM/DD string" in data["message"]

    # Test year-only date (less than 2 parts)
    res = await get_article_history("Python (programming language)", "2025")
    data = json.loads(res.text)
    assert not data["success"]
    assert "date format must be YYYY/MM/DD or YYYY/MM" in data["message"]

    # Test non-numeric date parts
    res = await get_article_history("Python (programming language)", "2025/abc/12")
    data = json.loads(res.text)
    assert not data["success"]
    assert "date parts must be valid numeric values" in data["message"]
