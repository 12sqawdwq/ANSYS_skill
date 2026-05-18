# Platform Refactor Playbook

Use this reference to convert a CAE tutorial, checklist, or skill repository into a validation platform.

## Review Passes

Run the refactor through at least four passes:

1. Engineering pass: list required FEM/CFD credibility gates and identify what the current repository cannot prove.
2. Data pass: define benchmark schemas, result schemas, finding severities, and report output formats.
3. Architecture pass: isolate solver-specific behavior behind adapters and keep validators deterministic.
4. Delivery pass: add CLI, tests, examples, and CI-ready commands.

## Minimum Platform Architecture

Recommended structure:

```text
src/
  cae_platform/
    cli.py
    validators/
    benchmarks/
    postprocess/
    report/
    plugins/
benchmarks/
  <case-name>/
    benchmark.json
tests/
```

The names can differ, but these responsibilities should remain separate.

## Engineering Requirement Matrix

Use these requirements when refactoring a repository. A platform can start small, but it should make each missing requirement visible instead of pretending it is complete.

| ID | Requirement | Acceptance Evidence |
| --- | --- | --- |
| REQ-PHYS-001 | Define physics, assumptions, units, and coordinate systems. | Project metadata or report section states them explicitly. |
| REQ-MAT-001 | Record material or fluid property provenance. | Values, units, source, and model assumptions are visible. |
| REQ-BC-001 | Audit loads and boundary conditions. | Validator or report lists supports, loads, directions, coordinate systems, and total magnitudes. |
| REQ-MESH-001 | Report mesh or cell statistics. | Element/cell count and quality metrics are captured. |
| REQ-MESH-002 | Require mesh convergence for stress, pressure drop, heat flux, or other mesh-sensitive claims. | At least two or three refinements with trend or documented limitation. |
| REQ-SOLVER-001 | Prove solver input was generated. | Input deck, `ds.dat`, case file, or equivalent evidence exists. |
| REQ-SOLVER-002 | Prove solver completed. | Completion marker, exit status, residual history, or solver API state exists. |
| REQ-RESULT-001 | Prove result objects are evaluated. | Numeric result values are extracted or GUI/API status confirms evaluation. |
| REQ-VV-001 | Compare against a benchmark, conservation law, or independent sanity calculation. | Relative error, imbalance, reaction balance, or pass/fail tolerance is reported. |
| REQ-REPORT-001 | Generate a structured engineering report. | JSON plus Markdown/HTML/PDF report is created from the same findings. |
| REQ-SW-001 | Expose validation through a CLI. | Example command runs in tests or documentation. |
| REQ-SW-002 | Represent findings with stable severity and codes. | Findings include OK/WARN/FAIL, code, message, and evidence source. |
| REQ-PLUGIN-001 | Isolate solver-specific logic behind adapters. | Mechanical/MAPDL/Fluent/etc. parsing does not leak into core validator contracts. |

## Validator Contract

A validator should produce findings, not prose-only conclusions.

Each finding should include:

- severity: OK, INFO, WARN, FAIL
- code: stable machine-readable identifier
- message: engineer-readable description
- evidence path or source
- optional numeric value and tolerance

Avoid validators that silently pass. Missing evidence should be WARN or FAIL.

## Benchmark Contract

Each benchmark should define:

- physics type
- geometry parameters
- material or fluid properties
- load and boundary conditions
- mesh/time-step targets
- analytical or trusted reference
- tolerance and acceptance rules
- known limitations

For example, a cantilever benchmark should define Euler-Bernoulli displacement, dimensions, material, load direction, element-size target, and acceptable relative error.

## Report Contract

An engineering report should contain:

- project identity and solver version
- model assumptions
- mesh/cell statistics
- boundary condition summary
- solver status
- result summary with units
- benchmark or sanity comparison
- pass/warn/fail table
- limitations and manual gates

Prefer JSON as an intermediate representation so Markdown, HTML, and PDF reports can be generated from the same data.

## Plugin Boundary

Keep solver-specific code behind adapters:

- Mechanical adapter: `.wbpj`, `.mechdb`, `ds.dat`, DPF, Mechanical scripting
- MAPDL adapter: `.db`, `.rst`, PyMAPDL, APDL input/output
- Fluent adapter: case/data files, residuals, monitors, mass imbalance
- Abaqus/CalculiX adapter: input deck, odb/frd/dat parsing

Core validators should operate on normalized evidence models when possible.

## Refactor Priorities

Do this first:

1. Package structure and CLI
2. Deterministic validator findings
3. Benchmark schema
4. Unit tests
5. JSON report output

Then add:

6. Markdown/HTML/PDF reports
7. DPF or solver API result extraction
8. mesh convergence workflows
9. plugin adapters
10. LLM-assisted engineering review

## Anti-Patterns

Avoid:

- claiming solved results from screenshots alone
- claiming GUI object existence as solver completion
- mixing benchmark formulas directly into CLI code without tests
- hiding solver-specific assumptions in generic validators
- accepting stress peaks without singularity and mesh-convergence discussion
- treating report generation as a substitute for verification
