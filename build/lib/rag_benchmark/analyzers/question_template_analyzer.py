from __future__ import annotations

from rich.console import Console
from rich.table import Table

from rag_benchmark.diagnostics.models import DocumentDiagnostic, UnusedQuestionTemplate
from rules.models import TemplateDefinition

console = Console()


class QuestionTemplateAnalyzer:

    @staticmethod
    def analyze(
        diagnostics: list[DocumentDiagnostic],
        template: TemplateDefinition,
    ) -> list[UnusedQuestionTemplate]:

        unused = []
        for document_type, specs in template.question_templates.items():
            # generated = {
            #     q.query
            #     for d in diagnostics
            #     if d.document_type == document_type
            #     for q in d.questions
            # }
            for spec in specs:
                used = {q.template_id for d in diagnostics for q in d.questions}
                if not used:
                    unused.append(
                        UnusedQuestionTemplate(
                            document_type=document_type,
                            template=spec.query_template[0],
                        )
                    )
        return unused

    @staticmethod
    def report(
        diagnostics: list[DocumentDiagnostic],
        template: TemplateDefinition,
    ) -> None:

        console.rule("[bold]Unused Question Templates[/bold]")
        unused = QuestionTemplateAnalyzer.analyze(
            diagnostics,
            template,
        )
        if not unused:
            console.print("[green]All templates were used.[/green]")
            return
        table = Table()
        table.add_column("Document")
        table.add_column("Template")

        for item in unused:
            table.add_row(
                item.document_type,
                item.template,
            )
        console.print(table)
