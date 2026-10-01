# MoeProf Codex Bootstrap

## Purpose

Install MoeProf into Codex as user-level infrastructure without placing MoeProf or Prof artifacts inside ordinary project repositories.

## Installation boundary

Allowed locations:

- ~/.moeprof/ for the local MoeProf checkout.
- ~/.codex/ for Codex global instructions, configuration, plugin state, and cache.
- ~/.agents/ for personal marketplace metadata used by supported OpenAI clients.

Do not place MoeProf or Prof configuration, identity, Skills, hooks, or setup files inside ordinary project directories.

Project-level AGENTS.md files may exist only for project-owned truth. They must not carry or duplicate the global MoeProf Constitution.

## Codex components

- Global Governor: adapters/codex/AGENTS.md, installed as the user-level Codex AGENTS.md.
- Four canonical Skills: delivered through the MoeProf plugin.
- OpenAI Developer Docs MCP: configured at user level, outside the portable plugin.
- Native Codex capabilities: preserved wherever legitimately available.

## Required setup

1. Keep the local MoeProf checkout under ~/.moeprof rather than inside a project directory.
2. Run scripts/build.py --check from that checkout before installation.
3. Install the generated Codex AGENTS.md as the user-level Codex AGENTS.md.
4. Add the official OpenAI Developer Docs MCP using the user-level Codex configuration.
5. Add the MuhsinKader/moeprof marketplace source at user level.
6. Restart Codex or the ChatGPT desktop app.
7. Install or enable the moeprof plugin from the MoeProf marketplace.
8. Start a fresh Codex session and run the integration smoke tests.

## Smoke tests

Before calling Codex integrated, verify:

- the global Governor is active;
- all four MoeProf Skills are discoverable;
- OpenAI Developer Docs MCP is available;
- legitimate native Codex capabilities remain available;
- no MoeProf or Prof artifact was written into an ordinary project directory;
- trivial work does not trigger unnecessary Discovery or Spec ceremony;
- Codex does not claim tests, builds, inspection, or deployment that did not occur.

Until these checks actually pass, the Codex surface is IMPLEMENTED but not INTEGRATED.

## Explicit non-goals

This bootstrap does not create project-level MoeProf configuration, add a custom Research Authority MCP, add a generic memory MCP, grant production credentials, or claim integration before runtime verification.
