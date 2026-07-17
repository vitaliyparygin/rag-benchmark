from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from rag_benchmark.models import ClassifiedDocument
from rag_benchmark.templates import TemplateDefinition

console = Console()


def diagnose_documents(
    classified_documents: Sequence[ClassifiedDocument],
    template: TemplateDefinition,
    max_questions_per_document: int,
) -> None:
    missing_counter: Counter[str] = Counter()
    unknown_counter: Counter[str] = Counter()
    total_questions = 0
    console.print()
    for doc in classified_documents:
        console.print(Rule(f"[bold blue]{doc.document.filename}"))
        console.print(f"[cyan]Type:[/] {doc.classification.document_type}")
        metadata = doc.metadata.as_plain_dict()
        if metadata:
            table = Table(title="Extracted Metadata")
            table.add_column("Field")
            table.add_column("Value")
            for k, v in metadata.items():
                table.add_row(
                    f"[green]✓ {k}",
                    str(v),
                )
            console.print(table)
        else:
            console.print("[red]No metadata extracted[/]")
        specs = template.question_templates.get(
            doc.classification.document_type,
            [],
        )
        if not specs:
            console.print("[yellow]No template available[/]")
            unknown_counter[doc.classification.document_type] += 1
            continue
        generated = 0
        skipped = []
        console.print("\n[bold]Question generation[/]")
        for spec in specs:
            for question_field in spec.fields:
                if generated >= max_questions_per_document:
                    break
                field_name = question_field.name
                if field_name not in metadata:
                    skipped.append(field_name)
                    missing_counter[field_name] += 1
                    console.print(f"[red]✗ {question_field:<20} missing")
                    continue
                question = spec.query_template.format(
                    field=field_name.replace("_", " "),
                    filename=doc.document.filename,
                    **metadata,
                )
                generated += 1
                total_questions += 1
                console.print(f"[green]✓ {question}")
        console.print()
        console.print(f"[bold]Generated:[/] {generated}")
        console.print(f"[bold]Skipped:[/] {len(skipped)}")
        if skipped:
            console.print("Missing fields: " + ", ".join(skipped))
    console.print()
    console.print(Rule("[bold green]SUMMARY"))
    summary = Table()
    summary.add_column("Metric")
    summary.add_column("Value")
    summary.add_row(
        "Documents",
        str(len(classified_documents)),
    )
    summary.add_row(
        "Questions",
        str(total_questions),
    )
    console.print(summary)
    if missing_counter:
        console.print()
        table = Table(title="Most Missing Fields")
        table.add_column("Field")
        table.add_column("Count")
        for missing_field, count in missing_counter.most_common():
            table.add_row(
                missing_field,
                str(count),
            )
        console.print(table)
    if unknown_counter:
        console.print()
        table = Table(title="Unknown document types")
        table.add_column("Type")
        table.add_column("Count")
        for t, c in unknown_counter.items():
            table.add_row(
                t,
                str(c),
            )
        console.print(table)
