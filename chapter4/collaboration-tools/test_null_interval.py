"""Null interval_seconds must fail before scheduling a background task."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from timer_tools import set_recurring_timer, _active_timers, _timer_tasks


def test_null_interval_rejects_without_scheduling():
    before_timers = set(_active_timers)
    before_tasks = set(_timer_tasks)

    async def run():
        return await set_recurring_timer(None, max_occurrences=1)

    result = asyncio.run(run())
    assert result["success"] is False
    assert set(_active_timers) == before_timers
    assert set(_timer_tasks) == before_tasks
