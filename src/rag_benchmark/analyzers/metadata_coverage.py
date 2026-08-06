from rag_benchmark.diagnostics.inspect import InspectResult
from rag_benchmark.diagnostics.models import FieldCoverageResult


class MetadataCoverageAnalyzer:

    @staticmethod
    def analyze(result: InspectResult) -> FieldCoverageResult:
        expected = list(result.expected_fields)
        extracted = list(result.classified.metadata.fields.keys())
        missing = [field for field in expected if field not in extracted]

        coverage = (
            len(extracted) / len(expected)
            if expected
            else 0.0
        )

        return FieldCoverageResult(
            expected=expected,
            extracted=extracted,
            missing=missing,
            coverage=coverage,
        )
