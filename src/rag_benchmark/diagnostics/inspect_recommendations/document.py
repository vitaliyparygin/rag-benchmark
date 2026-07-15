from __future__ import annotations
from rag_benchmark.diagnostics.inspect import InspectResult
from rag_benchmark.diagnostics.models import Recommendation
SEVERITY_CRITICAL = "critical"
SEVERITY_WARNING = "warning"
SEVERITY_INFO = "info"
def generate_document_recommendations(
    result: InspectResult,
) -> list[Recommendation]:
    """Generate recommendations for a single inspected document."""

    template = result.question_templates
    recommendations: list[Recommendation] = []

    confidence = result.classified.classification.confidence

    if confidence < 0.5:
        recommendations.append(
            Recommendation(
                context=result.classified.document.filename,
                issue=f"Low classification confidence ({confidence:.2f})",
                suggestion="Improve filename/content classification patterns.",
                severity=SEVERITY_WARNING,
            )
        )

    if result.missing_fields:
        recommendations.append(
            Recommendation(
                context=result.classified.classification.document_type,
                issue=(
                    f"Only {len(result.classified.metadata.fields)}/"
                    f"{len(result.expected_fields)} expected metadata fields were extracted."
                ),
                suggestion="Improve regex extraction coverage.",
                severity=SEVERITY_WARNING,
            )
        )

        for field in result.missing_fields:
            recommendations.append(
                Recommendation(
                    context=field,
                    issue="Metadata field was not extracted.",
                    suggestion=f"Add regex for '{field}'.",
                    severity=SEVERITY_INFO,
                )
            )

    if not result.questions:
        recommendations.append(
            Recommendation(
                context=result.classified.classification.document_type,
                issue="No benchmark questions generated.",
                suggestion="Add question templates or improve metadata extraction.",
                severity=SEVERITY_CRITICAL,
            )
        )

    elif len(result.questions) < len(result.expected_fields):
        recommendations.append(
            Recommendation(
                context=result.classified.classification.document_type,
                issue="Only part of the expected questions were generated.",
                suggestion="Improve metadata extraction to unlock more questions.",
                severity=SEVERITY_INFO,
            )
        )

    if (
        result.classified.classification.document_type
        not in template.question_templates
    ):
        recommendations.append(
            Recommendation(
                context=result.classified.classification.document_type,
                issue="No question templates defined.",
                suggestion="Add question templates for this document type.",
                severity=SEVERITY_WARNING,
            )
        )

    return recommendations