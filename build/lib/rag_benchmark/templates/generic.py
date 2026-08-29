"""Generic, domain-agnostic template.

Useful as a default and as a starting point to copy when building a new
custom template. Relies entirely on the package's DEFAULT_RULES /
DEFAULT_FIELD_RULES for classification and extraction, and defines a
modest, broadly applicable set of question patterns.
"""

from __future__ import annotations

from rag_benchmark.generators.base import QuestionTemplateMap, QuestionSpec
from rules.models import QuestionField, QuestionTemplateRule

TEMPLATE_NAME = "generic"

QUESTION_TEMPLATES: QuestionTemplateMap = {
    "invoice": [
        QuestionSpec(
            "invoice",
            query_template=[
                "What is the {field} on invoice {filename}?",
                "Extract the {field} from {filename}.",
                "Find the invoice {field}.",
                "Which {field} appears on this invoice?",
            ],
            fields=(
                QuestionField("invoice_number"),
                QuestionField("amount"),
                QuestionField("customer"),
                QuestionField("currency"),
            ),
        ),
    ],
    "vendor_profile": [
        QuestionSpec(
            "vendor_profile",
            [
                "What is the {field} of the vendor described in {filename}?",
            ],
            fields=(
                QuestionField("vendor"),
                QuestionField("phone"),
                QuestionField("email"),
                QuestionField("address"),
            ),
        ),
    ],
    "generic_contract": [
        QuestionSpec(
            "generic_contract",
            [
                "What is the {field} in the contract {filename}?",
            ],
            fields=(
                QuestionField("contract_number"),
                QuestionField("customer"),
                QuestionField("contractor"),
                QuestionField("contend_dateractor"),
                QuestionField("start_date"),
            ),
        ),
    ],
    "bank_statement": [
        QuestionSpec(
            "bank_statement",
            [
                "What is the {field} shown in {filename}?",
            ],
            fields=(
                QuestionField("account_number"),
                QuestionField("statement_period"),
                QuestionField("balance"),
            ),
        ),
    ],
    "meeting_minutes": [
        QuestionSpec(
            "meeting_minutes",
            [
                "Who attended the meeting recorded in {filename}?",
            ],
            fields=(QuestionField("attendees"),),
        ),
    ],
    "project_report": [
        QuestionSpec(
            "project_report",
            [
                "What is the current {field} of the project in {filename}?",
            ],
            fields=(
                QuestionField("project_name"),
                QuestionField("status"),
            ),
        ),
    ],
}
