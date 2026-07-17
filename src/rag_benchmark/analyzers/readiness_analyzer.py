from rag_benchmark.diagnostics.inspect import InspectResult
from rag_benchmark.diagnostics.models import (
    FieldCoverageStatistic,
    QuestionCoverageResult,
    ReadinessReport,
    RegexCoverage,
)


class ReadinessAnalyzer:

    @staticmethod
    def analyze(
        result: InspectResult,
        metadata: FieldCoverageStatistic | None,
        questions: QuestionCoverageResult | None,
        regex_score: RegexCoverage | None,
    ) -> ReadinessReport:
        metadata_score = metadata.coverage_percent if metadata is not None else 0.0
        question_score = questions.coverage if questions is not None else 0.0

        regex_score_value = regex_score.coverage if regex_score is not None else 0.0

        classification = result.classified.classification.confidence
        overall = (classification + metadata_score + question_score + regex_score_value) / 4

        return ReadinessReport(
            metadata_score=metadata_score,
            question_score=question_score,
            overall_score=overall,
            regex_score=regex_score_value,
        )
