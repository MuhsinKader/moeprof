#!/usr/bin/env python3
"""Deny-only Codex hook for a small set of high-confidence never-events.

This is a safety backstop, not a general command classifier and not a replacement
for Codex permissions, sandboxing, credentials, environment separation, or human
approval. Ambiguous commands are left to the normal Codex permission model.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Rule:
    name: str
    reason: str
    patterns: tuple[re.Pattern[str], ...]


RULES: tuple[Rule, ...] = (
    Rule(
        name="catastrophic-root-deletion",
        reason="Blocked catastrophic filesystem deletion.",
        patterns=(
            re.compile(r"(?i)(?:^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f[^\n]*\s+/(?:\s|$|\*)"),
            re.compile(r"(?i)remove-item\b[^\n]*(?:-recurse\b[^\n]*-force|-force\b[^\n]*-recurse)[^\n]*(?:[A-Z]:\\|/)(?:\*|\s|$)"),
        ),
    ),
    Rule(
        name="whole-database-destruction",
        reason="Blocked destructive whole-database operation.",
        patterns=(
            re.compile(r"(?is)\bdrop\s+database\s+(?!if\s+exists\s+test\b)"),
            re.compile(r"(?is)\bdrop\s+schema\s+[^;\n]+\bcascade\b"),
        ),
    ),
    Rule(
        name="infrastructure-destruction",
        reason="Blocked explicit infrastructure destruction.",
        patterns=(
            re.compile(r"(?i)\bterraform\s+destroy\b"),
            re.compile(r"(?i)\bpulumi\s+destroy\b"),
        ),
    ),
    Rule(
        name="protected-branch-force-push",
        reason="Blocked force-push to a protected primary branch.",
        patterns=(
            re.compile(r"(?i)\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f)\b[^\n]*(?:\bmain\b|\bmaster\b)"),
            re.compile(r"(?i)\bgit\s+push\b[^\n]*(?:\bmain\b|\bmaster\b)[^\n]*(?:--force(?:-with-lease)?|-f)\b"),
        ),
    ),
    Rule(
        name="credential-store-read",
        reason="Blocked direct read of a known credential store.",
        patterns=(
            re.compile(r"(?i)\b(?:cat|type|more|less|get-content)\b[^\n]*(?:\.ssh[/\\]id_(?:rsa|dsa|ecdsa|ed25519)|\.aws[/\\]credentials|\.git-credentials|\.pypirc|application_default_credentials\.json)"),
        ),
    ),
)


def command_from(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return ""
    command = tool_input.get("command")
    return command if isinstance(command, str) else ""


def match_rule(command: str) -> Rule | None:
    for rule in RULES:
        if any(pattern.search(command) for pattern in rule.patterns):
            return rule
    return None


def denial(event_name: str, reason: str) -> dict[str, Any]:
    if event_name == "PermissionRequest":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "decision": {
                    "behavior": "deny",
                    "message": reason,
                },
            }
        }

    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0

    if not isinstance(payload, dict):
        return 0

    command = command_from(payload)
    if not command:
        return 0

    rule = match_rule(command)
    if rule is None:
        return 0

    event_name = payload.get("hook_event_name")
    if event_name not in {"PreToolUse", "PermissionRequest"}:
        event_name = "PreToolUse"

    print(json.dumps(denial(event_name, rule.reason)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
