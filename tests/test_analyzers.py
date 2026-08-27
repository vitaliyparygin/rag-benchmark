"""Tests for rag_benchmark.extractor."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from rag_benchmark.analyzers.field_coverage import FieldCoverageAnalyzer
from rag_benchmark.analyzers.question_coverage import QuestionCoverageAnalyzer
from rag_benchmark.analyzers.regex_analyzer import RegexAnalyzer
from rag_benchmark.diagnostics.analyzers.missing_improvements_analyzer import (
    MissingImprovementsAnalyzer,
)
from rag_benchmark.diagnostics.models import DocumentSummary
from rag_benchmark.models import BenchmarkQuery, Difficulty


def test_field_coverage():
    classified = SimpleNamespace(
        metadata=SimpleNamespace(
            fields={
                "vendor": "Tech Ltd",
                "amount": "100",
            }
        )
    )

    result = FieldCoverageAnalyzer.analyze(
        classified,
        [
            "vendor",
            "amount",
            "date",
        ],
    )

    assert result.expected == [
        "vendor",
        "amount",
        "date",
    ]

    assert result.extracted == [
        "vendor",
        "amount",
    ]

    assert result.missing == [
        "date",
    ]

    assert result.coverage == 2 / 3


class Rule:
    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns


def test_regex_analyzer():
    document = SimpleNamespace(
        classification=SimpleNamespace(
            document_type="vendor_profile",
        ),
        document=SimpleNamespace(text="""
Vendor Name: Tech Supplies Ltd
Phone: +380671234567
Email: sales@test.com
"""),
    )

    template = SimpleNamespace(
        extraction_rules={
            "vendor_profile": (
                Rule(
                    "vendor",
                    (r"Vendor\s*Name:\s*(.+)",),
                ),
                Rule(
                    "phone",
                    (r"Phone:\s*([+\d]+)",),
                ),
                Rule(
                    "email",
                    (r"Email:\s*(.+)",),
                ),
            )
        }
    )

    result = RegexAnalyzer.analyze(
        document,
        template,
    )
    assert len(result) == 3

    assert result[0].field == "vendor"
    assert result[0].matches == 1

    assert result[1].field == "phone"
    assert result[1].matches == 1

    assert result[2].field == "email"
    assert result[2].matches == 1


def test_question_coverage():
    result = SimpleNamespace(
        expected_fields=[
            "vendor",
            "amount",
            "date",
        ],
        questions=[
            BenchmarkQuery(
                id=1,
                query="What is the vendor?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["vendor"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=["metadata"],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=2,
                query="What is the amount?",
                expected_document="Invoice.pdf",
                expected_fields=["amount"],
                document_type="invoice",
                difficulty=Difficulty.EASY,
                tags=["metadata"],
                template_id="invoice",
            ),
        ],
    )

    coverage = QuestionCoverageAnalyzer.analyze(result)

    assert coverage.expected == 3
    assert coverage.generated == 2
    assert coverage.missing == ["date"]

    # Coverage is stored as a ratio.
    # Presentation layer converts it to a percentage.
    assert coverage.coverage == pytest.approx(2 / 3)


def test_document_summary():
    summary = DocumentSummary(
        filename="Invoice.pdf",
        document_type="invoice",
        extracted_fields=["invoice_number", "amount"],
        missing_fields=["customer"],
        regex_stats=[],
        field_coverage=2 / 3,
    )

    assert summary.filename == "Invoice.pdf"
    assert summary.document_type == "invoice"
    assert summary.extracted_fields == [
        "invoice_number",
        "amount",
    ]
    assert summary.missing_fields == ["customer"]
    assert summary.field_coverage == 2 / 3


def test_question_coverage_all_fields_generated():
    result = SimpleNamespace(
        expected_fields=[
            "vendor",
            "vendor_id",
            "phone",
            "email",
            "address",
        ],
        questions=[
            BenchmarkQuery(
                id=1,
                query="What is the vendor name?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["vendor"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=[],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=2,
                query="What is the vendor ID?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["vendor_id"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=[],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=3,
                query="What is the phone?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["phone"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=[],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=4,
                query="What is the email?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["email"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=[],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=5,
                query="What is the address?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["address"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=[],
                template_id="vendor_profile",
            ),
        ],
    )

    coverage = QuestionCoverageAnalyzer.analyze(result)

    assert coverage.expected == 5
    assert coverage.generated == 5
    assert coverage.missing == []
    assert coverage.coverage == pytest.approx(1.0)


def test_question_coverage_uses_expected_fields_from_questions():
    result = SimpleNamespace(
        expected_fields=[
            "vendor",
            "vendor_id",
            "phone",
        ],
        questions=[
            BenchmarkQuery(
                id=1,
                query="What is the vendor?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["vendor"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=["metadata"],
                template_id="vendor_profile",
            ),
            BenchmarkQuery(
                id=2,
                query="What is the vendor ID?",
                expected_document="Vendor Profile.pdf",
                expected_fields=["vendor_id"],
                document_type="vendor_profile",
                difficulty=Difficulty.EASY,
                tags=["metadata"],
                template_id="vendor_profile",
            ),
        ],
    )

    coverage = QuestionCoverageAnalyzer.analyze(result)

    assert coverage.expected == 3
    assert coverage.generated == 2
    assert coverage.missing == ["phone"]
    assert coverage.coverage == pytest.approx(2 / 3)


def test_missing_field_does_not_produce_regex_improvement_when_field_is_absent_from_document():
    result = SimpleNamespace(
        expected_fields=[
            "vendor",
            "vendor_id",
            "phone",
            "email",
            "address",
        ],
        extracted_metadata=[
            "vendor",
            "vendor_id",
            "phone",
            "email",
        ],
        missing_fields=["address"],
        regex_stats=[
            SimpleNamespace(
                field="vendor",
                matched=True,
                pattern=r"vendor\s*[:\-]\s*([^\n]+)",
            ),
            SimpleNamespace(
                field="vendor_id",
                matched=True,
                pattern=r"vendor\s+id\s*[:\-]?\s*([A-Za-z0-9\-]+)",
            ),
            SimpleNamespace(
                field="phone",
                matched=True,
                pattern=r"(?:phone|tel|telephone)\s*[:\-]?\s*([\d\-\+\(\) ]{7,})",
            ),
            SimpleNamespace(
                field="email",
                matched=True,
                pattern=r"(?:email|e-mail)\s*[:\-]?\s*([\w.\-]+@[\w.\-]+\.\w+)",
            ),
            SimpleNamespace(
                field="address",
                matched=False,
                pattern=r"address\s*[:\-]?\s*([^\n]+)",
            ),
        ],
        question_templates={},
        questions=[],
        classified=SimpleNamespace(
            classification=SimpleNamespace(
                document_type="vendor_profile",
            ),
        ),
    )

    improvements = MissingImprovementsAnalyzer.analyze(result)

    assert improvements == []
