"""Metadata extraction: pulls structured fields out of document text.

The extraction interface is generic (field_name -> regex pattern) so new
document types or fields can be supported by adding a mapping entry rather
than writing new code, keeping the extractor open for extension.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

from rules.loader import load_field_rules
from rules.models import FieldRule
from rag_benchmark.logging import get_logger
from rag_benchmark.models import Document as DocumentModel
from rag_benchmark.utils.text import normalize_whitespace

from .models import ExtractedField, ExtractedMetadata

__all__ = ["ExtractedField", "ExtractedMetadata"]
logger = get_logger("extractor")


class MetadataExtractor(ABC):
    """Abstract interface for extracting fields from a classified document."""

    @abstractmethod
    def extract(self, document: DocumentModel, document_type: str) -> ExtractedMetadata:
        """Extract metadata fields for a document of a known type.

        Args:
            document: The document to extract fields from.
            document_type: The classified type, used to select field rules.

        Returns:
            ExtractedMetadata containing whatever fields were found. Fields
            that could not be found are simply omitted (not set to empty).
        """
        raise NotImplementedError


# @dataclass(frozen=True)
# class FieldRule:
#     """A single named field and the regex pattern(s) that can extract it.
#
#     The first capturing group of the first pattern that matches is used as
#     the extracted value.
#     """
#
#     name: str
#     patterns: tuple[str, ...]


class RegexMetadataExtractor(MetadataExtractor):
    """Extracts fields using per-document-type regex rules.

    Args:
        extra_rules: Additional or overriding field rules, keyed by
            document_type, merged on top of DEFAULT_FIELD_RULES. This is
            the extension point used by domain-specific templates (e.g.
            the ERP template can add PO-specific fields).
    """

    def __init__(self, extra_rules: dict[str, tuple[FieldRule, ...]] | None = None) -> None:
        field_rules = load_field_rules()
        self._rules: dict[str, tuple[FieldRule, ...]] = dict(field_rules)
        if extra_rules:
            for doc_type, rules in extra_rules.items():
                base = self._rules.get(doc_type, ())
                # Merge by field name so a template can override a generic
                # rule's regex without producing a duplicate entry for the
                # same field (which would otherwise double-count that field
                # in expected_fields(), coverage stats, and reports).
                merged: dict[str, FieldRule] = {rule.name: rule for rule in base}
                for rule in rules:
                    merged[rule.name] = rule
                self._rules[doc_type] = tuple(merged.values())

    def extract(self, document: DocumentModel, document_type: str) -> ExtractedMetadata:
        rules = self._rules.get(document_type, ())
        fields: dict[str, ExtractedField] = {}

        for rule in rules:
            for pattern in rule.patterns:
                match = re.search(pattern, document.text, flags=re.IGNORECASE)
                if match and match.groups():
                    value = normalize_whitespace(match.group(1))
                    if value:
                        fields[rule.name] = ExtractedField(name=rule.name, value=value)
                        break

        if not fields and rules:
            logger.debug("No fields extracted for %s (type=%s)", document.filename, document_type)

        return ExtractedMetadata(
            document_id=document.id, document_type=document_type, fields=fields
        )

    def expected_fields(self, document_type: str) -> list[str]:
        """Return the field names this extractor knows how to extract for a type.

        Used by the diagnostics subsystem to compute metadata coverage
        (fields expected vs. fields actually extracted) without needing to
        know anything about regex internals.

        Args:
            document_type: The classified document type to look up.

        Returns:
            Field names in rule-definition order, or an empty list if no
            rules are registered for this document type.
        """
        return [rule.name for rule in self._rules.get(document_type, ())]
