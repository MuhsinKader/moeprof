---
name: moeprof-engineering
description: Use for substantive implementation. Preserve agreed scope, choose the smallest complete architecture, use the strongest legitimate native capabilities available, and keep feedback loops narrow and evidence-driven.
---

# MoeProf Engineering

## Objective

Implement the agreed outcome with the simplest complete solution that preserves scope, quality, security, maintainability, and the user's intent.

## Inputs

- current user instruction;
- accepted spec where one exists;
- project truth;
- live repository/runtime state;
- relevant authoritative documentation;
- applicable tests and verification expectations.

## Decision rules

Use this Skill for substantive implementation.

Do not use it merely for discussion, brainstorming, or an obvious micro-edit.

If material ambiguity appears during implementation, pause only that decision and invoke the Discovery logic proportionally.

## Workflow

1. Read only the context necessary to perform the task safely.
2. Confirm the live technical reality before changing it.
3. Preserve the agreed stack and architecture unless an explicit material change is approved.
4. Choose the smallest complete implementation.
5. Prefer vertical progress that produces useful, testable behavior.
6. Reuse sound existing patterns before adding new abstractions.
7. Keep changes scoped.
8. Use the strongest legitimate native capabilities available in the current environment:
   - repository inspection;
   - shell;
   - builds;
   - tests;
   - browser/device tools;
   - data tools;
   - MCP;
   - hooks;
   - subagents;
   - worktrees;
   - sandboxing;
   where appropriate and available.
9. Run narrow feedback checks while implementing.
10. Hand the finished change to verification rather than declaring success from implementation alone.

## Engineering principles

- clarity over cleverness;
- cohesion over fragmentation;
- explicit behavior over magic;
- maintainability over theoretical purity;
- current requirements over speculative generality;
- fewer cohesive files where reasonable;
- every abstraction must earn its cost.

## Boundaries

- No silent scope expansion.
- No unrelated refactor hidden inside the task.
- No speculative framework or dependency without a real need.
- No forced TDD.
- No fake test, build, benchmark, or inspection claims.
- No weakening Codex/local capability to match Web limitations.
- No production, destructive, credential-sensitive, or consequential external action without the proper capability boundary and authorization.

## Output

A scoped implementation plus enough factual implementation notes to support verification.

## Definition of done

Engineering is done when the intended change is implemented and ready for independent, task-appropriate verification. It is not complete merely because the files changed.
