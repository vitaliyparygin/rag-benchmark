from __future__ import annotations

from rules.loader import load_field_rules


def test_detect_field_rules():
    rules = load_field_rules()

    assert "invoice" in rules
    assert rules["invoice"][0].name == "invoice_number"
    assert rules["invoice"][0].patterns
