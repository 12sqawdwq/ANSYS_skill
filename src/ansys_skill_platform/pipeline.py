"""Workflow orchestration for simulation validation."""

from __future__ import annotations

from pathlib import Path
import logging

from .benchmarks import CantileverBenchmark
from .config import WorkflowConfig, load_workflow_config
from .report import PipelineReport, write_report
from .validators import MechanicalValidator


LOGGER = logging.getLogger("ansys_skill_platform")


class PipelineRunner:
    """Run a configured validation workflow."""

    def __init__(self, config: WorkflowConfig, config_path: Path | None = None) -> None:
        self.config = config
        self.config_path = config_path

    @classmethod
    def from_file(cls, path: Path) -> "PipelineRunner":
        return cls(load_workflow_config(path), config_path=Path(path))

    def run(self) -> PipelineReport:
        workflow_name = str(self.config_path) if self.config_path else "in-memory"
        report = PipelineReport(workflow=workflow_name)
        LOGGER.info("Starting validation workflow: %s", workflow_name)

        self._run_validation(report)
        self._run_benchmark(report)

        written = write_report(
            report,
            self.config.report.output_dir,
            self.config.report.name,
            self.config.report.formats,
        )
        for path in written:
            LOGGER.info("Wrote report: %s", path)
        report.add_step(
            "report",
            "OK",
            "Wrote reports: " + ", ".join(str(path) for path in written),
        )
        return report

    def _run_validation(self, report: PipelineReport) -> None:
        solver = self.config.project.solver
        if solver != "mechanical":
            report.add_step("validate", "FAIL", f"Unsupported solver: {solver}")
            return

        validation = MechanicalValidator(
            self.config.project.path,
            self.config.project.exports,
        ).validate()
        report.validation = validation.as_dict()
        status = "OK" if validation.passed else "FAIL"
        report.add_step("validate", status, f"Mechanical validator pass={validation.passed}")

    def _run_benchmark(self, report: PipelineReport) -> None:
        benchmark_name = self.config.benchmark.name
        if not benchmark_name:
            report.add_step("benchmark", "SKIP", "No benchmark configured.")
            return
        if benchmark_name != "cantilever":
            report.add_step("benchmark", "FAIL", f"Unsupported benchmark: {benchmark_name}")
            return

        benchmark = CantileverBenchmark()
        result: dict[str, object] = benchmark.as_dict()
        fea_value = self.config.benchmark.fea_tip_displacement_m
        if fea_value is None:
            result["status"] = "WARN"
            result["message"] = "No FEA tip displacement supplied for comparison."
            report.benchmark = result
            report.add_step("benchmark", "WARN", str(result["message"]))
            return

        error = benchmark.relative_error_percent(fea_value)
        tolerance = self.config.benchmark.tolerance_percent
        result.update(
            {
                "fea_tip_displacement_m": fea_value,
                "relative_error_percent": error,
                "tolerance_percent": tolerance,
                "within_tolerance": error <= tolerance,
            }
        )
        report.benchmark = result
        if error <= tolerance:
            report.add_step("benchmark", "OK", f"Cantilever error {error:.4g}% <= {tolerance:.4g}%.")
        else:
            report.add_step("benchmark", "FAIL", f"Cantilever error {error:.4g}% > {tolerance:.4g}%.")


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
