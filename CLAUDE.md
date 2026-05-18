# CLAUDE.md

When working on Ansys Discovery / SpaceClaim / Workbench / Mechanical deliverables in this repository, read and follow:

- `ansys-mechanical-mvp/SKILL.md`
- `ansys-mechanical-mvp/references/mechanical-mvp.md`

For automation work, also inspect:

- `src/ansys_skill_platform/validators/mechanical.py`
- `src/ansys_skill_platform/benchmarks/cantilever.py`
- `benchmarks/cantilever/benchmark.json`

## Core Rule

Use this minimum viable path:

```text
Discovery / SpaceClaim geometry -> Workbench project -> Mechanical mesh/load/solve/evaluate/save
```

Discovery / SpaceClaim is the geometry authoring layer. Workbench Mechanical is the real FEA solver and postprocessing layer.

## Acceptance Standard

Do not claim that a Mechanical result is solved/evaluated just because a result object exists in the tree.

A result is accepted only when Mechanical shows:

- colored contour on the model
- visible result legend
- non-empty Minimum and Maximum values
- evaluated result status after the latest mesh/load/setup change

If the model is gray and the Details panel has blank or red Minimum/Maximum fields, report that the result object exists but is not evaluated.

## Useful Check

For a quick filesystem sanity check, run:

```powershell
python .\ansys-mechanical-mvp\scripts\check_mechanical_delivery.py <path-to-project.wbpj> --exports <optional-export-dir>
```

This script does not replace Mechanical GUI validation.

For the newer platform CLI, run:

```powershell
$env:PYTHONPATH = ".\src"
python -m ansys_skill_platform.cli validate <path-to-project.wbpj> --exports <optional-export-dir>
```
