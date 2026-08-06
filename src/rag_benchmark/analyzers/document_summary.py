from typing import TYPE_CHECKING

from rag_benchmark.diagnostics.models import (
    DocumentSummary,
)

if TYPE_CHECKING:
    from rag_benchmark.diagnostics.inspect import InspectResult
UNKNOWN_TYPE = "Unknown"


class DocumentSummaryAnalyzer:

    @staticmethod
    def analyze(result: InspectResult) -> DocumentSummary:
        field_coverage = (
            result.field_coverage.coverage if result.field_coverage is not None else 0.0
        )
        summary = DocumentSummary(
            filename=result.classified.document.filename,
            document_type=result.classified.classification.document_type,
            extracted_fields=list(result.classified.metadata.fields.keys()),
            missing_fields=result.missing_fields,
            regex_stats=result.regex_stats,
            field_coverage=field_coverage,
        )
        return summary
