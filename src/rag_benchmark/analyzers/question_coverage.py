from __future__ import annotations

from rich.console import Console

from rag_benchmark.diagnostics.inspect import InspectResult
from rag_benchmark.diagnostics.models import QuestionCoverageResult

console = Console()


class QuestionCoverageAnalyzer:
    @staticmethod
    def analyze(result: InspectResult) -> QuestionCoverageResult:
        expected_fields = set(result.expected_fields)

        generated_fields = {
            field for question in result.questions for field in question.expected_fields
        }

        generated_fields &= expected_fields

        missing = sorted(expected_fields - generated_fields)

        expected = len(expected_fields)
        generated = len(generated_fields)

        return QuestionCoverageResult(
            expected=expected,
            generated=generated,
            missing=missing,
            coverage=generated / expected if expected else 0.0,
        )
