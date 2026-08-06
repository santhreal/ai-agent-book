from scripts.sync_chapter2_figures import replace_text_nodes


def test_replace_text_nodes_rtl_overrides_existing_direction_attribute():
    svg = '<svg><text x="10" direction="ltr">Hello</text></svg>'
    values = ["مرحبا"]
    result = replace_text_nodes(svg, values, rtl=True)
    assert 'direction="rtl"' in result
    assert 'direction="ltr"' not in result
    assert 'unicode-bidi="plaintext"' in result
