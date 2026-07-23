from __future__ import annotations

from rules.loader import load_field_rules


def test_detect_field_rules():
    rules = load_field_rules()

    assert "Invoice" in rules
    assert rules["Invoice"][0].name == "invoice_number"
    assert rules["Invoice"][0].patterns
