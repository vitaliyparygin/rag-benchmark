from __future__ import annotations

from rich.console import Console
from rich.tree import Tree

from rag_benchmark.diagnostics.models import DocumentDiagnostic, QuestionGeneration
from rag_benchmark.models import BenchmarkQuery, ClassifiedDocument
from rules.models import TemplateDefinition

console = Console()


class QuestionGenerationAnalyzer:

    @staticmethod
    def analyze(
        classified: ClassifiedDocument,
        template: TemplateDefinition,
        questions: list[BenchmarkQuery],
    ) -> QuestionGeneration:

        specs = template.question_templates.get(
            classified.classification.document_type,
            (),
        )
        available = classified.metadata.as_plain_dict()
        generated_fields = {field for q in questions for field in q.expected_fields}

        possible = 0
        missing_fields: list[str] = []
        unused_templates: list[str] = []

        for spec in specs:
            template_used = False
            for questions_field in spec.fields:
                possible += 1
                field_name = questions_field.name
                if field_name in available:
                    template_used = True
                else:
                    missing_fields.append(field_name)

            if not template_used:
                unused_templates.append(spec.query_template[0])

        generated = len(questions)
        skipped = max(
            possible - generated,
            0,
        )
        coverage = generated / possible if possible else 1.0

        return QuestionGeneration(
            possible=possible,
            generated=generated,
            skipped=skipped,
            generated_fields=sorted(generated_fields),
            missing_fields=sorted(set(missing_fields)),
            unused_templates=unused_templates,
            coverage=coverage,
        )

    @staticmethod
    def report(
        diagnostics: list[DocumentDiagnostic],
    ) -> None:
        console.print()
        tree = Tree("[bold]Generated Questions[/bold]")
        for diag in diagnostics:
            if not diag.questions:
                continue
            doc = tree.add(diag.filename)
            for q in diag.questions:
                doc.add(q.query)

        console.print(tree)
