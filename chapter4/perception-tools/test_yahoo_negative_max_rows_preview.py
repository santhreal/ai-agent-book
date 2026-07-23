"""Regression: negative max_rows_preview must not drop the tail via Python slice."""
import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import yahoo_finance_tools as yft


def _history_df(n=10):
    idx = pd.date_range("2024-01-01", periods=n, freq="D", name="Date")
    return pd.DataFrame({"Open": range(n), "Close": range(n)}, index=idx)


def _payload(text_content):
    return json.loads(text_content.text)


def test_negative_preview_returns_all(monkeypatch):
    ticker = MagicMock()
    ticker.history.return_value = _history_df(10)
    monkeypatch.setattr(yft.yf, "Ticker", lambda symbol: ticker)

    result = asyncio.run(
        yft.get_historical_data(
            "AAPL", "2024-01-01", "2024-01-15", max_rows_preview=-1
        )
    )
    payload = _payload(result)
    assert payload["success"] is True
    assert payload["message"]["total_records"] == 10
    assert len(payload["message"]["data"]) == 10


def test_zero_preview_returns_all(monkeypatch):
    ticker = MagicMock()
    ticker.history.return_value = _history_df(4)
    monkeypatch.setattr(yft.yf, "Ticker", lambda symbol: ticker)

    result = asyncio.run(
        yft.get_historical_data(
            "AAPL", "2024-01-01", "2024-01-15", max_rows_preview=0
        )
    )
    payload = _payload(result)
    assert payload["success"] is True
    assert len(payload["message"]["data"]) == 4


def test_positive_preview_keeps_head(monkeypatch):
    ticker = MagicMock()
    ticker.history.return_value = _history_df(10)
    monkeypatch.setattr(yft.yf, "Ticker", lambda symbol: ticker)

    result = asyncio.run(
        yft.get_historical_data(
            "AAPL", "2024-01-01", "2024-01-15", max_rows_preview=3
        )
    )
    payload = _payload(result)
    assert payload["success"] is True
    assert len(payload["message"]["data"]) == 3
