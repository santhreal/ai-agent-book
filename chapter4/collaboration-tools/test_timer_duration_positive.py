"""One-shot timers with duration_seconds <= 0 must be rejected."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import timer_tools as t


async def _probe(duration):
    t._active_timers.clear()
    t._timer_tasks.clear()
    result = await t.set_timer(duration, timer_name="probe")
    await asyncio.sleep(0.05)
    for task in list(t._timer_tasks.values()):
        task.cancel()
    await asyncio.sleep(0)
    return result


def test_zero_duration_rejected():
    result = asyncio.run(_probe(0))
    assert result["success"] is False
    assert "positive" in result["error"]
    assert t._active_timers == {}


def test_negative_duration_rejected():
    result = asyncio.run(_probe(-5))
    assert result["success"] is False
    assert t._active_timers == {}


def test_none_duration_rejected():
    result = asyncio.run(_probe(None))
    assert result["success"] is False
    assert "positive" in result["error"]
    assert t._active_timers == {}


def test_positive_duration_accepted():
    async def run():
        t._active_timers.clear()
        t._timer_tasks.clear()
        result = await t.set_timer(60, timer_name="ok")
        for task in list(t._timer_tasks.values()):
            task.cancel()
        await asyncio.sleep(0)
        return result

    result = asyncio.run(run())
    assert result["success"] is True
    assert result["duration_seconds"] == 60
