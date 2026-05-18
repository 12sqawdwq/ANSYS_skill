"""Workflow configuration loading for the validation platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass(frozen=True)
class ProjectConfig:
    solver: str
    path: Path
    exports: Path | None = None


@dataclass(frozen=True)
class BenchmarkConfig:
    name: str | None = None
    fea_tip_displacement_m: float | None = None
    tolerance_percent: float = 5.0


@dataclass(frozen=True)
class ReportConfig:
    output_dir: Path = Path("reports")
    name: str = "validation-report"
    formats: list[str] = field(default_factory=lambda: ["json", "markdown"])


@dataclass(frozen=True)
class LoggingConfig:
    level: str = "INFO"


@dataclass(frozen=True)
class WorkflowConfig:
    project: ProjectConfig
    benchmark: BenchmarkConfig = field(default_factory=BenchmarkConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def load_workflow_config(path: Path) -> WorkflowConfig:
    raw = _load_mapping(Path(path))
    project_raw = _require_mapping(raw, "project")
    benchmark_raw = _optional_mapping(raw, "benchmark")
    report_raw = _optional_mapping(raw, "report")
    logging_raw = _optional_mapping(raw, "logging")

    project = ProjectConfig(
        solver=str(project_raw.get("solver", "mechanical")).lower(),
        path=Path(_require(project_raw, "path")),
        exports=Path(project_raw["exports"]) if project_raw.get("exports") else None,
    )
    benchmark = BenchmarkConfig(
        name=benchmark_raw.get("name"),
        fea_tip_displacement_m=_optional_float(benchmark_raw.get("fea_tip_displacement_m")),
        tolerance_percent=float(benchmark_raw.get("tolerance_percent", 5.0)),
    )
    report = ReportConfig(
        output_dir=Path(report_raw.get("output_dir", "reports")),
        name=str(report_raw.get("name", "validation-report")),
        formats=[str(item).lower() for item in report_raw.get("formats", ["json", "markdown"])],
    )
    logging_config = LoggingConfig(level=str(logging_raw.get("level", "INFO")).upper())
    return WorkflowConfig(
        project=project,
        benchmark=benchmark,
        report=report,
        logging=logging_config,
    )


def _load_mapping(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = _parse_simple_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("Workflow config must be a mapping.")
    return data


def _parse_simple_yaml(text: str) -> dict[str, object]:
    """Parse the small YAML subset used by the example configs.

    This intentionally avoids a runtime dependency. It supports nested mappings
    with two-space indentation and scalar/list values parsed as JSON-like data.
    """

    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, root)]
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2 != 0:
            raise ValueError(f"Invalid indentation at line {line_number}: {raw_line}")
        if ":" not in line:
            raise ValueError(f"Expected key/value pair at line {line_number}: {raw_line}")
        key, raw_value = line.strip().split(":", 1)
        value = raw_value.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if not value:
            child: dict[str, object] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(value)
    return root


def _parse_scalar(value: str) -> object:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        return json.loads(value.replace("'", '"'))
    try:
        if any(char in value for char in [".", "e", "E"]):
            return float(value)
        return int(value)
    except ValueError:
        return value


def _require_mapping(data: dict[str, object], key: str) -> dict[str, object]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Missing required mapping: {key}")
    return value


def _optional_mapping(data: dict[str, object], key: str) -> dict[str, object]:
    value = data.get(key, {})
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping for: {key}")
    return value


def _require(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    if value in {None, ""}:
        raise ValueError(f"Missing required value: {key}")
    return str(value)


def _optional_float(value: object) -> float | None:
    if value in {None, ""}:
        return None
    return float(value)
