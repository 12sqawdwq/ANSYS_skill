# Strict FEM/CFD Review

Use this reference when reviewing a CAE automation repository from the perspective of a demanding simulation engineer.

## Severity

- Blocker: the result cannot be trusted or the platform claim is false.
- Major: the workflow may run, but key verification evidence is missing.
- Minor: clarity, reporting, or maintainability issue.

## Universal Simulation Gates

Block acceptance unless the workflow can answer:

- What physics are solved?
- What assumptions simplify the physics?
- What unit system is used everywhere?
- What coordinate system defines loads, constraints, and reported results?
- What are the expected order-of-magnitude results?
- What numerical method and solver are used?
- What evidence proves the solver completed?
- What evidence proves the result object was evaluated?
- What benchmark, sanity check, conservation check, or independent calculation bounds the result?

## FEM Review Requirements

For structural, thermal, modal, or multiphysics FEM work, require:

- geometry scale and units audit
- material property provenance, including linear/nonlinear assumptions
- element type and formulation rationale
- mesh size, aspect ratio, Jacobian, skewness, and convergence logic
- boundary condition audit for overconstraint and rigid body modes
- load direction, distribution, and coordinate system audit
- reaction force or moment balance when applicable
- contact, joint, remote point, and constraint-equation review when present
- stress singularity handling near point loads, sharp corners, contacts, and fixed edges
- result location clarity: nodal, elemental, integration point, averaged, unaveraged
- deformation scale and contour legend validation
- benchmark comparison for canonical cases

FEM blocker examples:

- result object exists but no contour or numeric min/max exists
- nodal force intended as total force but applied as force per node
- stress maximum reported at a singular constraint without interpretation
- no mesh convergence for stress-driven conclusions
- no reaction balance for a static structural load case

## CFD Review Requirements

For CFD, thermal-fluid, or flow solver work, require:

- fluid property provenance and temperature/compressibility assumptions
- domain and boundary condition rationale
- inlet/outlet mass, pressure, and turbulence specification audit
- Reynolds, Mach, Prandtl, or relevant dimensionless number estimate
- mesh quality: skewness, orthogonality, aspect ratio, boundary-layer resolution
- wall treatment and y+ target for turbulent flow
- solver model rationale: laminar, RANS, LES, multiphase, compressible, etc.
- residual history plus engineering monitors, not residuals alone
- mass, momentum, and energy imbalance checks
- time-step or Courant number check for transient runs
- grid independence study for reportable conclusions
- postprocessing plane/probe definitions and coordinate systems

CFD blocker examples:

- residuals converge but mass imbalance is unacceptable
- wall shear or heat transfer is reported without y+ or near-wall model check
- pressure drop is reported without inlet/outlet reference definitions
- transient result is reported without timestep independence or monitor periodicity

## Result Credibility Gate

Do not accept a result because software generated an object, file, or screenshot.

Accept a result only when there is evidence for:

- solver completion
- evaluated results
- visible or extracted numeric values
- physically reasonable magnitude
- mesh/time-step adequacy for the conclusion
- independent reference, conservation check, or benchmark comparison

Use "visual evidence" only as one part of acceptance. Engineering acceptance needs numeric evidence.
