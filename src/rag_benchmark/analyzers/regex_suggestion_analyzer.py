from rag_benchmark.diagnostics.models import RegexCandidate, RegexSuggestion
from rag_benchmark.suggestions.regex_suggestions import suggest_regex


class RegexSuggestionAnalyzer:

    @staticmethod
    def analyze(
        candidates: list[RegexCandidate],
    ) -> list[RegexSuggestion]:
        suggestions: list[RegexSuggestion] = []

        for candidate in candidates:
            suggestions.append(
                RegexSuggestion(
                    label=candidate.label,
                    occurrences=candidate.count,
                    regex=suggest_regex(candidate.label),
                )
            )

        return suggestions
