from rag_benchmark.config import BenchmarkConfig
from rag_benchmark.diagnostics.analyzer import run_diagnostics
from rag_benchmark.diagnostics.models import PipelineDiagnostics
from rag_benchmark.pipeline import BenchmarkPipeline


class DiagnosticsService:

    def __init__(self, pipeline: BenchmarkPipeline):
        self.pipeline = pipeline

    def run(
        self,
        config: BenchmarkConfig,
        file: str | None = None,
    ) -> PipelineDiagnostics:
        return run_diagnostics(
            pipeline=self.pipeline,
            config=config,
            file=file,
        )
