from __future__ import annotations

from dataclasses import dataclass

from rag_benchmark.config import BenchmarkConfig
from rag_benchmark.models import ScannedFile
from rag_benchmark.templates import TemplateDefinition

from .models import BenchmarkDataset, ClassifiedDocument

__all__ = [
    "BenchmarkConfig",
    "BenchmarkDataset",
    "ClassifiedDocument",
    "TemplateDefinition",
]


@dataclass
class PipelineResult:
    config: BenchmarkConfig
    template: TemplateDefinition
    scanned_files: list[ScannedFile]
    classified_documents: list[ClassifiedDocument]
    dataset: BenchmarkDataset

    # def execute(self, config: BenchmarkConfig) -> PipelineResult:
    #     template = self._resolve_template(config)
    #     scanned = self.scan(
    #         config.dataset,
    #         recursive=config.recursive,
    #     )
    #
    #     classified = self.classify(
    #         scanned,
    #         template,
    #     )
    #
    #     dataset = self.generate(
    #         classified,
    #         template,
    #         config.max_questions_per_document,
    #     )
    #
    #     dataset.source_dataset = config.dataset
    #
    #     return PipelineResult(
    #         config=config,
    #         scanned_files=scanned,
    #         classified_documents=classified,
    #         dataset=dataset,
    #         template=template,
    #     )
