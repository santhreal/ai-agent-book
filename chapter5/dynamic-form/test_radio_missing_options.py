"""Radio fields without an options key must render like select."""
from demo import render_form_html


def test_radio_missing_options_key():
    html = render_form_html(
        {
            "title": "Survey",
            "fields": [
                {"type": "radio", "name": "seat", "label": "Seat"},
            ],
        },
        "book a seat",
    )
    assert "Seat" in html
    assert 'class="radio-row"' in html
