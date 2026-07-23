from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from rag_benchmark.cli.options import ForceOpt, TemplateOpt
from rag_benchmark.config import BenchmarkConfig
from rag_benchmark.io import ensure_writable
from rag_benchmark.logging import configure_logging, get_logger
from rag_benchmark.templates import available_builtin_templates

console = Console()

logger = get_logger("cli.init")

DEFAULT_CONFIG = {
    "dataset": "datasets",
    "output": "benchmarks",
    "template": "generic",
    "reader": "pdfplumber",
    "question_generator": "template",
    "language": "en",
    "recursive": True,
    "max_questions_per_document": 6,
}


def run_init(
    output: Annotated[Path, typer.Option("--output", help="Directory to scaffold.")] = Path("."),
    template: TemplateOpt = "generic",
    force: ForceOpt = False,
) -> None:
    """Scaffold a benchmark.yaml config file and dataset/output directories."""
    configure_logging(verbose=True)
    config_path = output / "benchmark.yaml"

    ensure_writable(config_path, force)
    dataset_dir = output / "datasets"
    benchmark_dir = output / "benchmarks"
    cfg = BenchmarkConfig(
        dataset=Path("datasets"),
        output=Path("benchmarks"),
        template=template or "generic",
    )
    assert cfg.dataset is not None
    config_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.save(config_path)

    dataset_dir.mkdir(parents=True, exist_ok=True)
    benchmark_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[green]Initialized[/green] config at {config_path}")
    console.print(f"  dataset directory: {cfg.dataset}")
    console.print(f"  output directory:  {cfg.output}")
    console.print(f"  template:          {cfg.template}")
    console.print(f"\nAvailable built-in templates: {', '.join(available_builtin_templates())}")
