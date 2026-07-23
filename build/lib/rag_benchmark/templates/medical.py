"""Medical RAG domain template (example plugin).

Demonstrates how a second, unrelated domain plugs into the same core
pipeline as the ERP template — no shared code required beyond the
generic interfaces.
"""

from __future__ import annotations

from rules.loader import load_template

TEMPLATE = load_template("medical")

CLASSIFICATION_RULES = TEMPLATE.classification_rules
EXTRACTION_RULES = TEMPLATE.extraction_rules
QUESTION_TEMPLATES = TEMPLATE.question_templates
