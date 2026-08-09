import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from gen_star_history import build_series


def test_build_series_iso_formats():
    start = datetime(2026, 7, 15, 0, 0, 0, tzinfo=timezone.utc)
    starred = [
        "2026-07-15T10:00:00Z",
        "2026-07-15T11:00:00.123456Z",
        "2026-07-15T12:00:00+00:00",
        "2026-07-15T14:00:00+02:00",
    ]
    x, y = build_series(starred, start)
    assert len(x) == 5
    assert len(y) == 5
    assert y[0] == 0
    assert y[-1] == 4
