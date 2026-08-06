import sys
from pathlib import Path

cot_dir = Path(__file__).resolve().parent.parent / "chapter7" / "cot-distillation"
if str(cot_dir) not in sys.path:
    sys.path.insert(0, str(cot_dir))

import generate_data as gd


def test_extract_predicted_number_handles_none_and_non_string():
    assert gd.extract_predicted_number(None) is None
    assert gd.extract_predicted_number(12345) is None


def test_verify_handles_none_and_non_string():
    assert gd.verify(None, 42.0) is False
    assert gd.verify(12345, 42.0) is False
