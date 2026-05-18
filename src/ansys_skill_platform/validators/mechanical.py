"""Filesystem and solver-input checks for Workbench Mechanical deliveries.

These checks intentionally do not claim engineering correctness. They separate
"project/setup/solver-input exists" from the final GUI acceptance gate:
Mechanical must show contours, legend, and non-empty Min/Max values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re


@dataclass(frozen=True)
class ValidationFinding:
    level: str
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass
class ValidationReport:
    project: str
    findings: list[ValidationFinding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(f.level == "FAIL" for f in self.findings)

    def add(self, level: str, code: str, message: str, path: Path | str | None = None) -> None:
        self.findings.append(
            ValidationFinding(
                level=level,
                code=code,
                message=message,
                path=str(path) if path is not None else None,
            )
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "project": self.project,
            "passed": self.passed,
            "findings": [finding.as_dict() for finding in self.findings],
            "acceptance_gate": (
                "Open Mechanical and verify contour, legend, and non-empty "
                "Minimum/Maximum values."
            ),
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)

    def to_text(self) -> str:
        lines = [f"Project: {self.project}", f"Filesystem pass: {self.passed}"]
        for finding in self.findings:
            location = f" ({finding.path})" if finding.path else ""
            lines.append(f"{finding.level}: {finding.code}: {finding.message}{location}")
        lines.append(
            "NOTE: final acceptance still requires Mechanical contour, legend, "
            "and non-empty Min/Max values."
        )
        return "\n".join(lines)


class MechanicalValidator:
    """Validate the delivery envelope around a Workbench Mechanical project."""

    def __init__(self, project: Path, exports: Path | None = None) -> None:
        self.project = Path(project)
        self.exports = Path(exports) if exports else None

    def validate(self) -> ValidationReport:
        report = ValidationReport(project=str(self.project))
        self._check_project(report)
        files_dir = self.project.with_name(self.project.stem + "_files")
        self._check_workbench_files(report, files_dir)
        self._check_exports(report)
        return report

    def _check_project(self, report: ValidationReport) -> None:
        if not self.project.exists():
            report.add("FAIL", "PROJECT_MISSING", "Workbench project file is missing.", self.project)
            return
        report.add("OK", "PROJECT_FOUND", "Workbench project file exists.", self.project)
        if self.project.suffix.lower() != ".wbpj":
            report.add("WARN", "PROJECT_SUFFIX", "Project file does not use .wbpj suffix.", self.project)

    def _check_workbench_files(self, report: ValidationReport, files_dir: Path) -> None:
        if not files_dir.exists():
            report.add("FAIL", "FILES_DIR_MISSING", "Workbench _files directory is missing.", files_dir)
            return
        report.add("OK", "FILES_DIR_FOUND", "Workbench _files directory exists.", files_dir)

        mechdb_files = sorted(files_dir.rglob("*.mechdb"))
        if mechdb_files:
            newest = max(mechdb_files, key=lambda path: path.stat().st_mtime)
            report.add("OK", "MECHDB_FOUND", "Mechanical database found.", newest)
        else:
            report.add("WARN", "MECHDB_MISSING", "No Mechanical database found.", files_dir)

        dsdat_files = sorted(files_dir.rglob("ds.dat"))
        if not dsdat_files:
            report.add("WARN", "DSDAT_MISSING", "No Mechanical solver input ds.dat found.", files_dir)
            return

        newest_dsdat = max(dsdat_files, key=lambda path: path.stat().st_mtime)
        report.add("OK", "DSDAT_FOUND", "Mechanical solver input ds.dat found.", newest_dsdat)
        self._check_dsdat(report, newest_dsdat)

    def _check_dsdat(self, report: ValidationReport, dsdat: Path) -> None:
        text = dsdat.read_text(errors="ignore")
        lower = text.lower()
        required_tokens = {
            "SOLVE_COMMAND": "solve",
            "FINISHED_SOLVE_MARKER": "finished solve",
            "MATERIAL_EX": "mp,ex",
            "FIXED_SUPPORT": "d,all,all",
        }
        for code, token in required_tokens.items():
            if token in lower:
                report.add("OK", code, f"ds.dat contains token: {token}", dsdat)
            else:
                report.add("WARN", code, f"ds.dat does not contain token: {token}", dsdat)

        solid_match = re.search(r"Number of solid elements\s*=\s*(\d+)", text, re.IGNORECASE)
        if solid_match:
            report.add("OK", "SOLID_ELEMENT_COUNT", f"Solid elements: {solid_match.group(1)}", dsdat)
        else:
            report.add("WARN", "SOLID_ELEMENT_COUNT", "Could not read solid element count.", dsdat)

        if " f," in lower or "\nf," in lower or "f,all," in lower:
            report.add("OK", "FORCE_COMMAND", "Force command appears in solver input.", dsdat)
        else:
            report.add("WARN", "FORCE_COMMAND", "No obvious nodal force command found in ds.dat.", dsdat)

    def _check_exports(self, report: ValidationReport) -> None:
        if self.exports is None:
            return
        if not self.exports.exists():
            report.add("WARN", "EXPORT_DIR_MISSING", "Export directory is missing.", self.exports)
            return
        avz_files = sorted(self.exports.rglob("*.avz"))
        if not avz_files:
            report.add("WARN", "AVZ_MISSING", "No AVZ exports found.", self.exports)
            return
        for avz in avz_files:
            size = avz.stat().st_size
            if size < 100_000:
                report.add("WARN", "AVZ_SMALL", f"AVZ export is suspiciously small: {size} bytes.", avz)
            else:
                report.add("OK", "AVZ_SIZE", f"AVZ export size looks plausible: {size} bytes.", avz)
