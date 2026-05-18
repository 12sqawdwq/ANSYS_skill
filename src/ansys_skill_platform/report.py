"""Report objects and writers for validation workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass(frozen=True)
class PipelineStep:
    name: str
    status: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
        }


@dataclass
class PipelineReport:
    workflow: str
    passed: bool = True
    steps: list[PipelineStep] = field(default_factory=list)
    validation: dict[str, object] | None = None
    benchmark: dict[str, object] | None = None

    def add_step(self, name: str, status: str, message: str) -> None:
        if status in {"FAIL", "ERROR"}:
            self.passed = False
        self.steps.append(PipelineStep(name=name, status=status, message=message))

    def as_dict(self) -> dict[str, object]:
        return {
            "workflow": self.workflow,
            "passed": self.passed,
            "steps": [step.as_dict() for step in self.steps],
            "validation": self.validation,
            "benchmark": self.benchmark,
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)

    def to_markdown(self) -> str:
        lines = [
            f"# Simulation Validation Report",
            "",
            f"- Workflow: `{self.workflow}`",
            f"- Passed: `{self.passed}`",
            "",
            "## Pipeline Steps",
            "",
            "| Step | Status | Message |",
            "| --- | --- | --- |",
        ]
        for step in self.steps:
            lines.append(f"| {step.name} | {step.status} | {step.message} |")

        if self.validation:
            lines.extend(["", "## Validation Findings", "", "| Level | Code | Message | Evidence |", "| --- | --- | --- | --- |"])
            for finding in self.validation.get("findings", []):
                lines.append(
                    "| {level} | {code} | {message} | {path} |".format(
                        level=finding.get("level", ""),
                        code=finding.get("code", ""),
                        message=finding.get("message", "").replace("|", "\\|"),
                        path=finding.get("path", "") or "",
                    )
                )

        if self.benchmark:
            lines.extend(["", "## Benchmark", ""])
            for key, value in self.benchmark.items():
                lines.append(f"- `{key}`: `{value}`")

        lines.extend(
            [
                "",
                "## Manual Acceptance Gate",
                "",
                "Open the solver UI or use a trusted solver API to confirm contours, "
                "legend, units, and non-empty numeric result ranges before engineering acceptance.",
            ]
        )
        return "\n".join(lines) + "\n"


def write_report(report: PipelineReport, output_dir: Path, name: str, formats: list[str]) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    if "json" in formats:
        path = output_dir / f"{name}.json"
        path.write_text(report.to_json(), encoding="utf-8")
        written.append(path)
    if "markdown" in formats or "md" in formats:
        path = output_dir / f"{name}.md"
        path.write_text(report.to_markdown(), encoding="utf-8")
        written.append(path)
    return written
