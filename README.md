# ANSYS_skill

This repository contains a Codex skill for building and reviewing a minimum viable Ansys simulation delivery path:

```text
Discovery / SpaceClaim geometry -> Workbench project -> Mechanical mesh/load/solve/evaluate/save
```

The skill is designed around a practical lesson from the cantilever benchmark workflow: a Mechanical tree can contain result objects without actually showing evaluated result contours. The final acceptance criterion is not "the object exists"; it is "Mechanical shows contour, legend, and non-empty Min/Max values."

## Skill

```text
ansys-mechanical-mvp/
```

Use this skill when working on:

- Discovery or SpaceClaim geometry handoff
- Workbench `.wbpj` project delivery
- Mechanical `Static Structural` setup
- mesh/load/result-object review
- PyMAPDL benchmark comparison
- deciding whether Mechanical results are truly solved and evaluated

## Why This Skill Exists

During the cantilever beam benchmark, the workflow reached several intermediate states that looked close to done but were not actually final deliverables:

- `.dsco` visual geometry existed, but it was not a real Mechanical solver result.
- `.avz` exports existed, but small exported view files were not enough to prove solved contours.
- Mechanical result objects existed in the tree, but they still needed `Solve` and `Evaluate All Results`.
- A gray body with empty red Min/Max fields was not an evaluated stress or deformation result.

This skill keeps those states separate and gives Codex a repeatable review checklist.

## Visual Review Examples

### Not Yet Accepted: Result Object Exists But Is Not Evaluated

The first screenshot shows a Mechanical model where result objects are present in the tree, but the selected result has no real contour and the result values are still blank/red. This is a setup-ready state, not a solved/evaluated delivery.

![Mechanical result object exists but is not evaluated](assets/images/not-evaluated-result.png)

Checklist signals:

- result object is selected
- geometry is still gray
- no stress/deformation contour legend is visible
- Minimum/Maximum fields are empty or red
- result item still needs solve/evaluate

### Accepted Target: Evaluated Mechanical Contour

The second screenshot shows the desired target state: Mechanical displays a colored contour with legend, min/max markers, and populated numerical values.

![Evaluated Mechanical equivalent stress contour](assets/images/evaluated-contour-result.png)

Checklist signals:

- body shows colored contour
- legend is visible
- Min/Max markers are displayed
- Details panel contains numerical Minimum/Maximum values
- result object has been evaluated after the latest mesh/load change

## Minimum Viable Path

The recommended workflow is deliberately narrow:

1. Build or edit geometry in Discovery / SpaceClaim.
2. Save the geometry as `.scdocx`.
3. Create a Workbench `Static Structural` system.
4. Attach the geometry to the Workbench system.
5. Open the `Model` cell in Mechanical.
6. Define material in Mechanical.
7. Generate mesh in Mechanical.
8. Apply supports and loads in Mechanical.
9. Add result objects in Mechanical.
10. Solve in Mechanical.
11. Evaluate all results in Mechanical.
12. Save the `.wbpj` with its matching `_files` directory.

## Final Acceptance Criteria

A Workbench Mechanical deliverable is accepted only when all of the following are true:

- `.wbpj` opens without missing-file warnings.
- Matching `_files` directory exists beside the `.wbpj`.
- Mechanical Outline contains expected mesh, material, support, load, and result objects.
- Mesh has been generated.
- Solution has been solved after the latest setup change.
- Result objects have been evaluated.
- Selected result shows a colored contour.
- The graphics window shows a legend.
- Details panel shows non-empty Minimum and Maximum values.
- Benchmark cases have a numerical reference, such as Euler-Bernoulli displacement or PyMAPDL output.

## Repository Layout

```text
ansys-mechanical-mvp/
  SKILL.md
  agents/
    openai.yaml
  references/
    mechanical-mvp.md
  scripts/
    check_mechanical_delivery.py
assets/
  images/
    not-evaluated-result.png
    evaluated-contour-result.png
```

## Quick Filesystem Check

The bundled script can catch missing project pieces and suspicious exports:

```powershell
python .\ansys-mechanical-mvp\scripts\check_mechanical_delivery.py `
  "D:\ansys_runs\benchmark\cantilever_workbench.wbpj" `
  --exports "D:\ansys_runs\benchmark\mechanical_exports"
```

This script does not prove engineering correctness. It only checks files. Final validation still happens in Mechanical by visually confirming contours, legend, and numeric result ranges.

## Important Distinction

Use precise status language:

- `Geometry ready`: Discovery / SpaceClaim geometry exists.
- `Project ready`: `.wbpj` and `_files` exist.
- `Setup ready`: Mechanical tree contains material, mesh, supports, loads, and result objects.
- `Solver input generated`: files such as `ds.dat` exist.
- `Solved/evaluated`: Mechanical shows contour, legend, and non-empty Min/Max values.

Do not collapse these states into a single "done" status.

## Installation

To use this skill locally with Codex, copy or clone `ansys-mechanical-mvp` into your Codex skills directory:

```powershell
Copy-Item -Recurse .\ansys-mechanical-mvp "$env:USERPROFILE\.codex\skills\ansys-mechanical-mvp"
```

Then ask Codex to use the `ansys-mechanical-mvp` skill when building or reviewing Ansys Discovery / Workbench Mechanical deliverables.
