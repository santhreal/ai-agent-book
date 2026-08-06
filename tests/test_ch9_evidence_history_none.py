import sys
from pathlib import Path

ch9_computer_use = Path(__file__).resolve().parent.parent / "chapter9" / "computer-use-open-model"
if str(ch9_computer_use) not in sys.path:
    sys.path.insert(0, str(ch9_computer_use))

from evidence import retain_step_screenshots


def test_retain_step_screenshots_handles_none_history(tmp_path):
    history_data = {"history": None}
    retained, records = retain_step_screenshots(history_data, tmp_path)
    assert retained == {"history": None}
    assert records == []
