---
name: moeprof-spec
description: Use for substantial, settled work where a compact durable execution contract will prevent scope or implementation drift across steps, sessions, or contributors. Do not use for trivial work or to discover requirements.
---

# MoeProf Spec

## Objective

Convert a settled substantial outcome into the smallest durable execution contract needed to preserve intent and prevent drift.

## Inputs

- accepted outcome;
- settled material decisions;
- project truth;
- constraints;
- relevant repository/runtime reality;
- known acceptance expectations.

## Decision rules

Use this Skill when the work is substantial enough that decisions may otherwise be lost or reinterpreted.

Typical triggers include:

- multi-step implementation;
- work spanning sessions;
- multiple contributors or agents;
- consequential architecture;
- externally visible behavior;
- complex integration;
- material analytical or security requirements.

Do not use this Skill to discover requirements.

Do not create a spec for obvious micro-edits.

## Workflow

Capture only the execution-critical contract:

1. Outcome
   - what success means.
2. Required behavior
   - observable capabilities or changes.
3. Locked decisions
   - architecture, stack, contracts, data semantics, design direction, or other material choices already made.
4. Constraints
   - security, privacy, compatibility, regulatory, performance, accessibility, operational, or business constraints.
5. Non-goals
   - material things intentionally outside scope.
6. Acceptance and evidence
   - what will prove the result works.
7. Risks and dependencies
   - only those that can materially affect delivery.

Check the contract against the user's latest explicit decisions before execution.

## Boundaries

- Do not redesign settled architecture while writing the spec.
- Do not add speculative requirements.
- Do not inflate the document with implementation trivia that belongs in code.
- Do not duplicate the MoeProf Constitution.
- Do not silently convert preferences into hard requirements.

## Output

A compact execution contract that another competent MoeProf session can implement without inventing material scope.

## Definition of done

The spec is done when the important outcome, decisions, boundaries, and proof requirements are explicit enough to prevent meaningful drift.
