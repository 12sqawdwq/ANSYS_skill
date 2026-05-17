---
name: ansys-mechanical-mvp
description: Create, review, or debug a minimum viable Ansys simulation delivery path that uses Discovery or SpaceClaim for geometry and Workbench Mechanical for the real structural solver workflow. Use when users ask for .scdocx/.dsco/.wbpj deliverables, Mechanical result contours, mesh/load setup, PyMAPDL-to-Mechanical validation, or when deciding whether visible Ansys result objects are truly solved/evaluated.
---

# Ansys Mechanical MVP

## Core Principle

Treat Discovery / SpaceClaim as the geometry authoring layer and Workbench Mechanical as the real FEA layer.

Do not treat `.dsco`, screenshots, HTML, AVZ exports, or colorized geometry as solved Mechanical results unless Mechanical itself shows evaluated result objects with non-empty numeric ranges and contours.

## Minimum Viable Path

Use this sequence for a small static structural benchmark or design handoff:

1. Create or edit geometry in Discovery / SpaceClaim.
2. Save neutral Ansys geometry such as `.scdocx`.
3. Create a Workbench `Static Structural` system and attach the geometry.
4. Open the `Model` cell in Mechanical.
5. In Mechanical, set material, mesh controls, boundary conditions, and loads.
6. Generate Mesh in Mechanical.
7. Solve in Mechanical.
8. Evaluate all result objects.
9. Save the `.wbpj` and its `_files` directory together.
10. Validate by reopening the `.wbpj` and checking that contours and numeric min/max values are visible.

## Acceptance Criteria

A Mechanical delivery is acceptable only when all of these are true:

- The project opens from `.wbpj` without missing-file warnings.
- The associated `_files` directory is present beside the `.wbpj`.
- Mechanical Outline contains the expected `Analysis Settings`, supports, loads, mesh, and `Solution`.
- Result objects have evaluated status, not just lightning/update-required icons.
- Selected result objects show a color contour, legend, and non-empty Minimum/Maximum values.
- For benchmark work, a numerical reference exists, such as Euler-Bernoulli beam displacement or a PyMAPDL result.

If a result item appears in the tree but the viewport is gray and Min/Max values are blank or red, report that the result is not actually evaluated.

## Mechanical Review Checklist

Use this review stance when the user asks whether the result is ready:

- Inspect the Mechanical tree status icons.
- Check `Details` for selected result objects.
- Verify `Minimum` and `Maximum` are populated.
- Verify a contour legend is visible in the graphics window.
- Confirm Mesh was generated, not only defined.
- Confirm `Solution` has been solved/evaluated after the latest setup change.
- If automation generated `ds.dat`, inspect it for material, constraints, loads, element counts, and solve commands.

For more details, read `references/mechanical-mvp.md`.

## Automation Guidance

Use automation to create projects and insert setup objects, but be conservative about claiming solved Mechanical results from batch runs.

Workbench journals can create a project and send Python to the Mechanical `Model` container. However, a batch export can still produce a view file that is not a trustworthy solved contour. Always validate in Mechanical GUI or by checking solver result files and evaluated result object state.

Use `scripts/check_mechanical_delivery.py` for a quick filesystem-level sanity check. It does not prove engineering correctness; it only flags missing deliverables and common false-positive result artifacts.

## Reporting Standard

When reporting status to users, separate these states clearly:

- Geometry ready: Discovery / SpaceClaim file exists.
- Project ready: `.wbpj` and `_files` exist.
- Setup ready: Mechanical tree contains material, mesh, supports, loads, and result objects.
- Solver input generated: `ds.dat` or solver files exist.
- Solved and viewable: Mechanical result objects show contours and non-empty numeric ranges.

Do not collapse these into one "done" status.
