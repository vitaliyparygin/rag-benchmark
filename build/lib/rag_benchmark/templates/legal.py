"""Legal Assistant domain template (example plugin)."""

from __future__ import annotations

from rules.loader import load_template

TEMPLATE = load_template("legal")

CLASSIFICATION_RULES = TEMPLATE.classification_rules
EXTRACTION_RULES = TEMPLATE.extraction_rules
QUESTION_TEMPLATES = TEMPLATE.question_templates
