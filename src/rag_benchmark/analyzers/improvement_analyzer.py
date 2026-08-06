from dataclasses import dataclass


@dataclass(frozen=True)
class Improvement:
    category: str
    item: str
    suggestion: str


class ImprovementAnalyzer:
    @staticmethod
    def analyze(
        *,
        expected_fields: list[str],
        extracted_fields: set[str],
        regex_fields: set[str],
        raw_text: str,
    ) -> list[Improvement]:
        text = raw_text.lower()
        improvements: list[Improvement] = []

        for field in expected_fields:
            if field in extracted_fields:
                continue

            if field not in regex_fields:
                improvements.append(
                    Improvement(
                        category="Regex",
                        item=field,
                        suggestion=f"Add regex for '{field}'",
                    )
                )
                continue

            if field.lower() not in text:
                improvements.append(
                    Improvement(
                        category="Metadata",
                        item=field,
                        suggestion="Field is not present in document",
                    )
                )
                continue

            improvements.append(
                Improvement(
                    category="Regex",
                    item=field,
                    suggestion=f"Regex does not match '{field}'",
                )
            )

        return improvements
