from __future__ import annotations

from rich.console import Console
from rich.tree import Tree

from rag_benchmark.diagnostics.models import DocumentDiagnostic, QuestionCoverageResult
from rag_benchmark.diagnostics.inspect import InspectResult
console = Console()


class QuestionCoverageAnalyzer:
    """Analyze question generation coverage."""

    @staticmethod
    def analyze(
        result: InspectResult,
    ) -> QuestionCoverageResult:
        expected = len(result.expected_fields)
        generated = len(result.questions)

        return QuestionCoverageResult(
            expected=expected,
            generated=generated,
            coverage=generated / expected if expected else 0.0,
        )

    # @staticmethod
    # def report(
    #     diagnostics: list[DocumentDiagnostic],
    # ) -> None:
    #
    #     console.rule("[bold]Question Coverage[/bold]")
    #     for diag in diagnostics:
    #         result = QuestionCoverageAnalyzer.analyze(
    #             diag,
    #         )
    #         tree = Tree(
    #             f"[cyan]{diag.classified.document.filename}[/cyan] " f"({result.coverage:.0%})"
    #         )
    #
    #         tree.add(f"Expected questions : {result.expected}")
    #         tree.add(f"Generated questions: {result.generated}")
    #         tree.add(f"Coverage           : {result.coverage:.0%}")
    #         console.print(tree)
