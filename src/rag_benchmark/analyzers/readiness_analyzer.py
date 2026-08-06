from rag_benchmark.diagnostics.inspect import InspectResult
from rag_benchmark.diagnostics.models import (
    FieldCoverageResult,
    QuestionCoverageResult,
    ReadinessReport,
    RegexCoverage,
)


class ReadinessAnalyzer:

    @staticmethod
    def analyze(
        result: InspectResult,
        metadata: FieldCoverageResult | None,
        questions: QuestionCoverageResult | None,
        regex_score: RegexCoverage | None,
    ) -> ReadinessReport:
        metadata_score = metadata.coverage if metadata is not None else 0.0
        question_score = questions.coverage if questions is not None else 0.0
        regex_score_value = regex_score.coverage if regex_score is not None else 0.0

        classification_score = (
            result.classified.classification.confidence
        )

        overall = (
            classification_score
            + metadata_score
            + question_score
            + regex_score_value
        ) / 4

        return ReadinessReport(
            metadata_score=metadata_score,
            question_score=question_score,
            regex_score=regex_score_value,
            overall_score=overall,
        )
