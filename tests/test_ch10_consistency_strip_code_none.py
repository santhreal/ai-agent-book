import sys
from pathlib import Path

ch10_bt = Path(__file__).resolve().parent.parent / "chapter10" / "book-translation"
if str(ch10_bt) not in sys.path:
    sys.path.insert(0, str(ch10_bt))

from consistency import analyze, check_adherence


def test_consistency_handles_none_translation_value():
    # When a chapter translation fails or evaluates to None in translations dictionary,
    # analyze and check_adherence should safely handle None without crashing with TypeError in _strip_code.
    translations = {
        "chapter1": "Transformer is a great architecture.",
        "chapter2": None,
    }

    result = analyze(translations)
    assert isinstance(result, dict)
    assert result["total_terms"] >= 0

    adh = check_adherence(translations)
    assert isinstance(adh, dict)
    assert "rate" in adh
