"""Document classification: assigns a document_type to each Document.

Classification combines filename signals and content signals so it does
not depend solely on naming conventions. The architecture is open for
extension: callers can supply any object implementing DocumentClassifier
(e.g. an LLM-backed or ML-based classifier) instead of DefaultClassifier.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from rich.console import Console
from rules.models import ClassificationRule, DocumentType

from rag_benchmark.logging import get_logger

from .models import ClassificationCandidate, ClassificationResult, Document

__all__ = [
    "ClassificationResult",
    "ClassificationCandidate",
    "DocumentClassifier",
]
logger = get_logger("classifier")
console = Console()

UNKNOWN_TYPE = DocumentType.UNKNOWN


class DocumentClassifier(ABC):
    """Abstract interface for classifying a Document into a document_type."""

    @abstractmethod
    def classify(self, document: Document) -> ClassificationResult:
        """Classify a single document.

        Args:
            document: The document to classify.

        Returns:
            A ClassificationResult with a document_type, confidence in
            [0, 1], and the signals that contributed to the decision.
        """
        raise NotImplementedError


# @dataclass(frozen=True)
# class ClassificationRule:
#     """A single rule mapping filename/content signals to a document type.
#
#     Attributes:
#         document_type: The label produced when this rule matches.
#         filename_patterns: Regex patterns checked against the filename.
#         content_patterns: Regex patterns checked against document text.
#         content_weight: Relative importance of a content match vs filename.
#     """
#
#     document_type: str
#     filename_patterns: tuple[str, ...] = field(default_factory=tuple)
#     content_patterns: tuple[str, ...] = field(default_factory=tuple)
#     content_weight: float = 0.7


# Generic, domain-agnostic default rule set. Callers/templates can supply
# their own rule list for domain-specific classification (see templates/).
DEFAULT_RULES: tuple[ClassificationRule, ...] = (
    ClassificationRule(
        document_type="invoice",
        filename_patterns=(r"invoice", r"\binv[-_]?\d+"),
        content_patterns=(r"invoice\s*(no|number|#)", r"total\s*due", r"bill\s*to"),
    ),
    ClassificationRule(
        document_type="purchase_order",
        filename_patterns=(r"purchase[-_ ]?order", r"\bpo[-_]?\d+"),
        content_patterns=(r"purchase\s*order", r"\bp\.?o\.?\s*(no|number|#)"),
    ),
    ClassificationRule(
        document_type="vendor_profile",
        filename_patterns=(r"vendor", r"supplier"),
        content_patterns=(r"vendor\s*(name|profile|id)", r"supplier\s*information"),
    ),
    ClassificationRule(
        document_type="employment_contract",
        filename_patterns=(r"employment[-_ ]?contract", r"offer[-_ ]?letter"),
        content_patterns=(r"employment\s*agreement", r"employee\s*and\s*employer"),
    ),
    ClassificationRule(
        document_type="insurance_policy",
        filename_patterns=(r"insurance", r"policy"),
        content_patterns=(r"policy\s*(number|holder)", r"coverage\s*period"),
    ),
    ClassificationRule(
        document_type="meeting_minutes",
        filename_patterns=(r"minutes", r"meeting[-_ ]?notes"),
        content_patterns=(r"meeting\s*minutes", r"attendees\s*:", r"action\s*items"),
    ),
    ClassificationRule(
        document_type="crm_opportunity",
        filename_patterns=(r"opportunity", r"\bcrm\b"),
        content_patterns=(r"opportunity\s*(name|stage|value)", r"deal\s*stage"),
    ),
    ClassificationRule(
        document_type="service _ticket",
        filename_patterns=(r"ticket", r"service[-_ ]?request"),
        content_patterns=(r"ticket\s*(no|number|#)", r"assigned\s*engineer", r"priority\s*:"),
    ),
    ClassificationRule(
        document_type="bank_statement",
        filename_patterns=(r"bank[-_ ]?statement", r"statement"),
        content_patterns=(r"account\s*(number|balance)", r"statement\s*period"),
    ),
    ClassificationRule(
        document_type="project_report",
        filename_patterns=(r"project[-_ ]?report", r"status[-_ ]?report"),
        content_patterns=(r"project\s*status", r"milestones?", r"deliverables?"),
    ),
    ClassificationRule(
        document_type="generic_contract",
        filename_patterns=(r"contract", r"agreement"),
        content_patterns=(r"this\s*agreement", r"terms\s*and\s*conditions", r"parties\s*hereto"),
    ),
)


class DefaultClassifier(DocumentClassifier):
    """Rule-based classifier combining filename and content regex signals.

    Confidence is computed as a weighted blend of filename and content
    matches so that a document only needs partial signal to be classified,
    but strong dual-signal matches score higher.
    """

    def __init__(self, rules: tuple[ClassificationRule, ...] | None = None) -> None:
        self._rules = rules if rules is not None else DEFAULT_RULES

    def classify(self, document: Document) -> ClassificationResult:
        filename_lower = document.filename.lower()
        text_lower = document.text.lower()

        best_type = UNKNOWN_TYPE
        best_score = 0.0
        best_signals: list[str] = []
        all_scores: list[ClassificationCandidate] = []
        for rule in self._rules:
            signals: list[str] = []
            filename_hit = any(
                re.search(pattern, filename_lower) for pattern in rule.filename_patterns
            )
            content_hits = [
                pattern for pattern in rule.content_patterns if re.search(pattern, text_lower)
            ]

            if not filename_hit and not content_hits:
                continue

            if filename_hit:
                signals.append(f"filename:{rule.document_type}")
            signals.extend(f"content:{pattern}" for pattern in content_hits)

            filename_score = 1.0 if filename_hit else 0.0
            content_score = min(len(content_hits) / max(len(rule.content_patterns), 1), 1.0)
            score = (1 - rule.content_weight) * filename_score + rule.content_weight * content_score

            if score > best_score:
                best_score = score
                best_type = DocumentType(rule.document_type)
                best_signals = signals

            all_scores.append(
                ClassificationCandidate(
                    document_type=best_type,
                    confidence=round(score, 3),
                    matched_signals=signals,
                )
            )

        if best_type == UNKNOWN_TYPE:
            logger.debug("Could not classify document: %s", document.filename)
        all_scores.sort(
            key=lambda x: x.confidence,
            reverse=True,
        )
        logger.info("%s -> %s, confidence {%.2f}", document.filename, best_type, best_score)

        return ClassificationResult(
            document_id=document.id,
            document_type=best_type,
            confidence=round(best_score, 3),
            matched_signals=best_signals,
            candidates=all_scores,
        )
