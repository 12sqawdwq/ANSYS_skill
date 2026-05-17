#!/usr/bin/env python3
"""Filesystem sanity check for an Ansys Workbench Mechanical delivery.

This script does not prove that Mechanical results are evaluated. It catches
missing project pieces and warns when exported result views are suspiciously
small or solver input files are missing.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def find_files(root: Path, pattern: str) -> list[Path]:
    return sorted(root.rglob(pattern)) if root.exists() else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path, help="Path to a .wbpj file")
    parser.add_argument(
        "--exports",
        type=Path,
        default=None,
        help="Optional directory containing exported result views such as .avz",
    )
    args = parser.parse_args()

    project = args.project
    ok = True

    if not project.exists():
        print(f"FAIL: project not found: {project}")
        return 2

    if project.suffix.lower() != ".wbpj":
        print(f"WARN: project does not end in .wbpj: {project}")

    files_dir = project.with_name(project.stem + "_files")
    if files_dir.exists():
        print(f"OK: Workbench files directory found: {files_dir}")
    else:
        print(f"FAIL: Workbench files directory missing: {files_dir}")
        ok = False

    mechdb = find_files(files_dir, "*.mechdb")
    dsdat = find_files(files_dir, "ds.dat")

    if mechdb:
        newest = max(mechdb, key=lambda path: path.stat().st_mtime)
        print(f"OK: Mechanical database found: {newest}")
    else:
        print("WARN: no .mechdb file found")

    if dsdat:
        newest = max(dsdat, key=lambda path: path.stat().st_mtime)
        text = newest.read_text(errors="ignore")
        print(f"OK: solver input found: {newest}")
        for token in ["SOLVE", "FINISHED SOLVE", "MP,EX", "d,all,all"]:
            status = "OK" if token.lower() in text.lower() else "WARN"
            print(f"{status}: ds.dat token check: {token}")
    else:
        print("WARN: no ds.dat solver input found")

    if args.exports:
        avz_files = find_files(args.exports, "*.avz")
        if not avz_files:
            print(f"WARN: no .avz files found in {args.exports}")
        for avz in avz_files:
            size = avz.stat().st_size
            level = "WARN" if size < 100_000 else "OK"
            print(f"{level}: AVZ export {avz.name} size={size} bytes")

    print(
        "NOTE: final acceptance still requires opening Mechanical and checking "
        "contours, legend, and non-empty Min/Max values."
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
