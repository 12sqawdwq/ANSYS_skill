---
name: cae-validation-platform
description: Refactor CAE, FEM, CFD, Ansys, MAPDL, Fluent, Abaqus, CalculiX, or PyAnsys workflow repositories from tutorial/checklist artifacts into verification-driven simulation validation platforms. Use when reviewing simulation automation projects, defining engineering acceptance criteria, designing validator architectures, benchmark databases, reports, plugin systems, or LLM-assisted CAE QA agents.
---

# CAE Validation Platform

## Purpose

Use this skill to turn a CAE workflow repository into a software system for simulation verification, validation, and delivery QA.

The target is not "the solver ran." The target is a reproducible platform that can explain whether a simulation result is credible enough to review, compare, report, or reject.

## Review Before Refactor

Run several review passes before editing architecture:

1. Physics pass: identify the governing physics, assumptions, units, material/fluid properties, loads, boundary conditions, and expected response scale.
2. Numerical pass: review element/cell type, mesh quality, mesh convergence expectations, timestep or load-step strategy, solver settings, and known singularities.
3. Solver-state pass: separate setup existence, solver input generation, solver completion, result evaluation, and final engineering acceptance.
4. Postprocessing pass: verify result location, averaging, coordinate systems, conservation checks, reaction balance, residuals, and benchmark comparison.
5. Software pass: turn manual checks into typed validators, CLI commands, benchmark data, reports, tests, and plugin boundaries.

If a repository cannot distinguish these states, treat it as a knowledge repository, not a validation platform.

## Refactor Pattern

Convert narrative workflow knowledge into these modules:

- `validators/`: deterministic checks with explicit pass/warn/fail findings.
- `benchmarks/`: analytical or trusted numerical references with tolerance rules.
- `postprocess/`: result extraction through solver APIs such as DPF, MAPDL, Fluent, or neutral files.
- `report/`: Markdown, HTML, PDF, or JSON engineering reports.
- `plugins/`: solver-specific adapters for Mechanical, MAPDL, Fluent, Abaqus, CalculiX, etc.
- `cli.py`: user-facing commands such as `validate`, `benchmark`, `report`, and `compare`.
- `tests/`: unit tests for formulas, parsers, validators, and failure modes.

Keep manual gates explicit. Do not claim automation has solved a gate that still requires Mechanical, CFD-Post, Fluent, or another solver UI/API to confirm.

## Strict Engineering Gates

Reject or downgrade claims when any of these are missing:

- clear units and coordinate systems
- load and boundary condition audit
- material or fluid property provenance
- mesh/cell quality and mesh independence logic
- solver completion evidence
- result-evaluation evidence
- conservation or reaction balance checks
- benchmark or sanity comparison
- reportable pass/warn/fail conclusion

For detailed FEM/CFD checks, read `references/strict-fem-cfd-review.md`.

For platform refactoring requirements, read `references/platform-refactor-playbook.md`.

## Reporting Language

Use precise states:

- Geometry ready
- Setup ready
- Mesh generated
- Solver input generated
- Solver completed
- Results evaluated
- Engineering accepted

Never collapse these into a single "done" status.
