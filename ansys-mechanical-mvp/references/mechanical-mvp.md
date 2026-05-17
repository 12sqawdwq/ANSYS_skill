# Mechanical MVP Reference

## Recommended Architecture

Use a narrow delivery split:

- Discovery / SpaceClaim: geometry only.
- Workbench: project container and system linking.
- Mechanical: material, mesh, boundary conditions, loads, solve, postprocessing.
- PyMAPDL: optional benchmark and numerical validation, not the final Workbench GUI deliverable.

## Cantilever Benchmark Defaults

Use these values for a simple verification case:

```text
Length: 1.0 m
Width: 0.05 m
Height: 0.05 m
Young's modulus: 210e9 Pa
Poisson ratio: 0.3
Tip load: -1000 N in global Z
Element size target: 0.02 m
Expected Euler-Bernoulli tip displacement: about 0.00305 m
```

The formula is:

```text
delta = F * L^3 / (3 * E * I)
I = b * h^3 / 12
```

## Result Readiness Checks

In Mechanical, a real viewable solution should show:

- A colored contour on the body.
- A legend for the selected result.
- Populated Minimum and Maximum values.
- Result object status without unresolved lightning/update indicators.
- No red blank result fields in Details.

If the body is gray and the result Details table has empty red Min/Max rows, the object exists but is not evaluated.

## Common False Positives

Avoid these mistakes:

- Treating a `.dsco` visual model as a solver result.
- Treating an `.avz` export as proof of solved results without checking contour values.
- Treating a saved `.wbpj` as solved when it only contains setup objects.
- Treating `ds.dat` solve text as enough if the GUI result objects remain unevaluated.
- Ignoring Mechanical status icons after mesh/load changes.

## Practical Recovery Steps

If result objects exist but no contour appears:

1. In Mechanical, right-click `Mesh` and choose `Generate Mesh`.
2. Right-click `Solution` and choose `Solve`.
3. Right-click `Solution` and choose `Evaluate All Results`.
4. Select each result and check Min/Max plus contour legend.
5. Save the project after the evaluated result is visible.

If automation is still desired, use it only to prepare the tree; keep final solve/evaluate validation in Mechanical unless a robust solver-result API check is implemented.

## Files To Preserve Together

For Workbench delivery, preserve:

```text
project.wbpj
project_files/
```

Do not move one without the other.

## Status Language

Use precise status words:

- "Geometry ready" means a Discovery / SpaceClaim file exists.
- "Setup ready" means Mechanical objects exist.
- "Solver input generated" means solver files such as `ds.dat` exist.
- "Solved/evaluated" means Mechanical shows contour, legend, and numeric ranges.
