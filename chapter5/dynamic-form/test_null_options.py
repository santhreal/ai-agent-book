"""Null select/radio options must render without TypeError."""
from demo import _render_field_html


def test_null_select_options():
    html = _render_field_html({
        "type": "select",
        "name": "cabin",
        "label": "Cabin",
        "options": None,
    })
    assert "select" in html
    assert "Cabin" in html


def test_null_radio_options():
    html = _render_field_html({
        "type": "radio",
        "name": "seat",
        "label": "Seat",
        "options": None,
    })
    assert "Seat" in html
