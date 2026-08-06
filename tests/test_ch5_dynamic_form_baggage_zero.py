import importlib.util
from pathlib import Path

demo_path = Path(__file__).resolve().parent.parent / "chapter5" / "dynamic-form" / "demo.py"
spec = importlib.util.spec_from_file_location("dynamic_form_demo", demo_path)
demo_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo_module)
summarize_offline = demo_module.summarize_offline


def test_summarize_offline_handles_integer_zero_baggage_count():
    submitted = {
        "departure_city": "上海",
        "destination_city": "北京",
        "departure_date": "2026-08-10",
        "cabin_class": "economy",
        "baggage_count": 0,
    }
    summary = summarize_offline(submitted)
    assert "无免费托运" in summary
    assert "免费托运 0 件" not in summary
