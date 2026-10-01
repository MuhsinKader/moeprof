---
name: moeprof-discovery
description: Use when unresolved ambiguity can materially change a product, architecture, data, security, workflow, research, consulting, or design decision. Do not use for small or already well-scoped work.
---

# MoeProf Discovery

## Objective

Resolve only the ambiguity that can materially change the solution before consequential execution begins.

## Inputs

- user objective;
- current constraints;
- existing project truth;
- repository or system reality where relevant;
- authoritative evidence where relevant.

## Decision rules

Run this Skill when different plausible answers would materially change:

- scope;
- architecture;
- stack;
- data semantics;
- security posture;
- workflow;
- product direction;
- design direction;
- analytical target;
- implementation cost;
- acceptance criteria.

Do not run this Skill merely because questions could be asked.

Do not use it for trivial, reversible, or already-settled work.

## Workflow

1. Restate the intended outcome in one compact form.
2. Separate what is known into:
   - FACT;
   - ASSUMPTION;
   - OPEN QUESTION;
   - DECISION NEEDED.
3. Identify only the uncertainties that can materially change the solution.
4. Resolve them with the cheapest reliable method:
   - inspect the repository or source;
   - inspect data or schema;
   - consult authoritative evidence;
   - run a narrow experiment;
   - ask the user a focused question.
5. Where a material trade-off exists, explain:
   - options;
   - consequences;
   - recommendation;
   - what decision is required.
6. Stop when the work is sufficiently determined to proceed safely.

## Boundaries

- Do not turn discovery into a workshop by default.
- Do not reopen decisions the user has explicitly settled unless new evidence materially invalidates them.
- Do not silently choose a material product, architecture, data, or security direction.
- Do not confuse memory with current project truth.
- Do not perform broad research when a narrow inspection answers the question.

## Output

Produce a compact decision brief containing only what materially affects execution:

- intended outcome;
- confirmed facts;
- remaining assumptions;
- decisions made;
- unresolved blocker, if any;
- recommended next move.

## Definition of done

Discovery is complete when the meaningful ambiguity is resolved enough that execution can proceed without silently inventing consequential requirements.
