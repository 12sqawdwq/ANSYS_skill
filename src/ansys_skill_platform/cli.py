"""Command line interface for the Ansys skill platform."""

from __future__ import annotations

import argparse
from pathlib import Path

from .benchmarks import CantileverBenchmark
from .validators import MechanicalValidator


def _validate(args: argparse.Namespace) -> int:
    report = MechanicalValidator(Path(args.project), Path(args.exports) if args.exports else None).validate()
    if args.json:
        output = Path(args.json)
        output.write_text(report.to_json(), encoding="utf-8")
        print(f"Wrote validation report: {output}")
    print(report.to_text())
    return 0 if report.passed else 1


def _benchmark(args: argparse.Namespace) -> int:
    benchmark = CantileverBenchmark()
    print("Cantilever benchmark:")
    for key, value in benchmark.as_dict().items():
        print(f"  {key}: {value:.12g}")
    if args.fea_displacement is not None:
        error = benchmark.relative_error_percent(args.fea_displacement)
        print(f"  fea_tip_displacement_m: {args.fea_displacement:.12g}")
        print(f"  relative_error_percent: {error:.6g}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ansys-skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a Workbench Mechanical delivery envelope.")
    validate.add_argument("project", help="Path to a .wbpj file.")
    validate.add_argument("--exports", help="Optional directory containing exported result views.")
    validate.add_argument("--json", help="Optional path for a JSON validation report.")
    validate.set_defaults(func=_validate)

    benchmark = subparsers.add_parser("benchmark", help="Print benchmark references.")
    benchmark.add_argument("name", choices=["cantilever"], help="Benchmark name.")
    benchmark.add_argument("--fea-displacement", type=float, help="FEA tip displacement in meters.")
    benchmark.set_defaults(func=_benchmark)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
