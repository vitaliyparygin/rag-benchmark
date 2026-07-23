from __future__ import annotations

from rag_benchmark.diagnostics.models import ClassificationScore
from rag_benchmark.models import ClassifiedDocument


class KeywordAnalyzer:

    @staticmethod
    def analyze(
        classified: ClassifiedDocument,
    ) -> list[ClassificationScore]:
        result = []

        for candidate in classified.classification.candidates:
            result.append(
                ClassificationScore(
                    document_type=candidate.document_type,
                    score=candidate.confidence,
                )
            )

        return result
