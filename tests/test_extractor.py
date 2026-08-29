"""Tests for rag_benchmark.extractor."""

from __future__ import annotations

from pathlib import Path

from rules.models import DocumentType

from rag_benchmark.extractor import RegexMetadataExtractor
from rag_benchmark.models import Document, DocumentFormat


def _doc(text: str) -> Document:
    return Document(
        id="doc1",
        path=Path("doc.txt"),
        filename="doc.txt",
        format=DocumentFormat.TXT,
        text=text,
        char_count=len(text),
    )


def test_extracts_invoice_fields() -> None:
    extractor = RegexMetadataExtractor()
    doc = _doc(
        "Invoice Number: INV-1001\nBill To: Acme Corp\nTotal Due: $1,250.00\nCurrency: USD\n"
    )
    metadata = extractor.extract(doc, DocumentType.INVOICE)

    fields = metadata.as_plain_dict()
    assert fields["invoice_number"] == "INV-1001"
    assert fields["amount"] == "1,250.00"
    assert "Acme Corp" in fields["customer"]
    assert fields["currency"] == "USD"


def test_extracts_vendor_profile_fields() -> None:
    extractor = RegexMetadataExtractor()
    doc = _doc(
        "Vendor Name: Globex Industries\nPhone: +1-555-0100\n"
        "Email: contact@globex.example\nAddress: 42 Industrial Way\n"
    )
    metadata = extractor.extract(doc, "vendor_profile")
    fields = metadata.as_plain_dict()

    assert "Globex" in fields["vendor"]
    assert fields["email"] == "contact@globex.example"
    assert "555-0100" in fields["phone"]


def test_unknown_document_type_yields_no_fields() -> None:
    extractor = RegexMetadataExtractor()
    doc = _doc("Some unrelated text.")
    metadata = extractor.extract(doc, DocumentType.UNKNOWN)
    assert metadata.fields == {}


def test_missing_field_is_simply_omitted() -> None:
    extractor = RegexMetadataExtractor()
    doc = _doc("Invoice Number: INV-1\n")  # no amount, customer, currency
    metadata = extractor.extract(doc, DocumentType.INVOICE)
    fields = metadata.as_plain_dict()
    assert "invoice_number" in fields
    assert "amount" not in fields
