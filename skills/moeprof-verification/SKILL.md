---
name: moeprof-verification
description: Use when meaningful work needs evidence before it can be called complete, merged, deployed, released, or handed to a client. Use lightweight checks for trivial low-risk work and deeper proof for consequential work.
---

# MoeProf Verification

## Objective

Establish with task-appropriate evidence that the agreed outcome was actually achieved without material scope, quality, security, or truthfulness failures.

## Inputs

- user objective;
- accepted spec where one exists;
- implementation or research output;
- live repository/runtime state;
- relevant acceptance criteria;
- applicable evidence sources.

## Decision rules

Verification depth is proportional to risk and visibility.

A trivial change may need a focused check.

A consequential system, model, research claim, client deliverable, security-sensitive change, or visible product experience needs stronger evidence.

## Workflow

1. Map each material requirement to evidence that can actually prove it.
2. Inspect the final scope:
   - what changed;
   - what did not;
   - whether any material decision drifted.
3. Verify correctness using the relevant mechanisms:
   - focused tests;
   - integration tests;
   - builds;
   - type/static checks;
   - runtime inspection;
   - data assertions;
   - analytical validation;
   - citation/source checks;
   - security checks.
4. Verify Distinction where relevant:
   - audience fit;
   - usability;
   - specificity;
   - coherence;
   - craft;
   - non-generic execution.
5. For UI, inspect the rendered experience when the environment permits it.
6. For performance, measure rather than infer.
7. For research, verify claims against the actual sources.
8. For predictive models, verify chronology/leakage, split logic, baseline, discrimination/calibration as appropriate, stability, limitations, and reproducibility.
9. Use a fresh reviewer or isolated pass when independence materially improves confidence.
10. State remaining uncertainty plainly.

## Boundaries

- Passing unrelated tests is not proof.
- A checklist is not verification unless the checks were actually performed.
- Source-code inspection alone is not sufficient proof of visual quality.
- Do not claim tests, builds, deployments, inspections, or research steps that did not occur.
- Do not average away a hard failure.

## Output

When material, report:

### VERIFIED
What the evidence establishes.

### NOT VERIFIED
What could not be established.

### ISSUES
Concrete failures or deviations.

### RISKS
Material remaining uncertainty or downstream concern.

## Definition of done

Verification is done when every material requirement is either supported by appropriate evidence or explicitly identified as not verified. Only then may the work advance to the next status.
