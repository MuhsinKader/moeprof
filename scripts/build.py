#!/usr/bin/env python3
"""Generate MoeProf adapters and compatibility packaging from canonical sources.

Human-maintained canonical inputs:
- plugin.json
- governor/constitution.md
- exactly four canonical skills under skills/

Generated outputs:
- adapters/codex/AGENTS.md
- adapters/chatgpt/custom-instructions.txt
- adapters/local/instructions.md
- .codex-plugin/plugin.json

Generated files must never be edited by hand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_MANIFEST = ROOT / "plugin.json"
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
GOVERNOR = ROOT / "governor" / "constitution.md"

SKILLS = {
    "moeprof-discovery": ROOT / "skills" / "moeprof-discovery" / "SKILL.md",
    "moeprof-spec": ROOT / "skills" / "moeprof-spec" / "SKILL.md",
    "moeprof-engineering": ROOT / "skills" / "moeprof-engineering" / "SKILL.md",
    "moeprof-verification": ROOT / "skills" / "moeprof-verification" / "SKILL.md",
}

ADAPTER_TARGETS = {
    "codex": ROOT / "adapters" / "codex" / "AGENTS.md",
    "chatgpt": ROOT / "adapters" / "chatgpt" / "custom-instructions.txt",
    "local": ROOT / "adapters" / "local" / "instructions.md",
}

SURFACE_LABELS = {
    "codex": "Codex",
    "chatgpt": "ChatGPT Web",
    "local": "Local OpenAI-powered runtime",
}

EXPECTED_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
EXPECTED_PLUGIN_NAME = "moeprof"
NAME_RE = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)


def read_bytes(path: Path) -> bytes:
    """Read canonical text with platform-independent LF line endings.

    Git may check files out as CRLF on Windows. Normalizing here keeps generated
    source hashes and adapters identical across Windows, macOS, and Linux.
    """
    if not path.is_file():
        raise SystemExit(f"Missing canonical source: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    return text.encode("utf-8")


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def load_portable_manifest() -> dict[str, object]:
    raw = read_bytes(PORTABLE_MANIFEST)
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid plugin.json: {exc}") from exc

    if not isinstance(manifest, dict):
        raise SystemExit("plugin.json must contain a JSON object")

    if manifest.get("$schema") != EXPECTED_SCHEMA:
        raise SystemExit(
            f"plugin.json must use schema {EXPECTED_SCHEMA!r}"
        )

    if manifest.get("name") != EXPECTED_PLUGIN_NAME:
        raise SystemExit(
            f"plugin.json name must be {EXPECTED_PLUGIN_NAME!r}"
        )

    version = manifest.get("version")
    description = manifest.get("description")
    if not isinstance(version, str) or not version.strip():
        raise SystemExit("plugin.json requires a non-empty string version")
    if not isinstance(description, str) or not description.strip():
        raise SystemExit("plugin.json requires a non-empty string description")

    return manifest


def canonical_sources() -> list[tuple[Path, bytes]]:
    sources: list[tuple[Path, bytes]] = [(GOVERNOR, read_bytes(GOVERNOR))]

    discovered = {
        p.parent.name
        for p in (ROOT / "skills").glob("*/SKILL.md")
        if p.is_file()
    }
    expected = set(SKILLS)
    if discovered != expected:
        missing = sorted(expected - discovered)
        extra = sorted(discovered - expected)
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        raise SystemExit(
            "Canonical Skill set drifted; MoeProf v0.1 requires exactly four Skills"
            + (f" ({', '.join(details)})" if details else "")
        )

    for expected_name, path in SKILLS.items():
        data = read_bytes(path)
        text = data.decode("utf-8")
        match = NAME_RE.search(text)
        actual_name = match.group(1) if match else None
        if actual_name != expected_name:
            raise SystemExit(
                f"Skill name mismatch in {path.relative_to(ROOT)}: "
                f"expected {expected_name!r}, found {actual_name!r}"
            )
        sources.append((path, data))

    return sources


def source_state(sources: list[tuple[Path, bytes]]) -> str:
    return "\n".join(
        f"{path.relative_to(ROOT).as_posix()}@{git_blob_sha(data)}"
        for path, data in sources
    )


def render_adapter(surface: str, governor_text: str, state: str) -> str:
    label = SURFACE_LABELS[surface]
    return (
        "<!-- GENERATED FILE — DO NOT EDIT BY HAND\n"
        "Canonical sources:\n"
        + "\n".join(f"- {line}" for line in state.splitlines())
        + "\nRegenerate: python scripts/build.py\n"
        "-->\n\n"
        f"# MoeProf 2.0 — {label} Adapter\n\n"
        "This adapter carries the canonical MoeProf Governor onto this surface. "
        "The four canonical workflow Skills remain under `skills/` and are loaded "
        "progressively when their triggers apply. Surface limitations must not weaken "
        "MoeProf on more capable runtimes.\n\n"
        + governor_text.rstrip()
        + "\n"
    )


def render_codex_manifest(manifest: dict[str, object]) -> str:
    compatibility = {
        "name": manifest["name"],
        "version": manifest["version"],
        "description": manifest["description"],
        "skills": "./skills/",
    }
    return json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n"


def expected_outputs() -> dict[Path, str]:
    manifest = load_portable_manifest()
    sources = canonical_sources()
    governor_text = sources[0][1].decode("utf-8")
    state = source_state(sources)

    outputs = {
        ADAPTER_TARGETS[surface]: render_adapter(surface, governor_text, state)
        for surface in ADAPTER_TARGETS
    }
    outputs[CODEX_MANIFEST] = render_codex_manifest(manifest)
    return outputs


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"WROTE {path.relative_to(ROOT)}")


def check_outputs(outputs: dict[Path, str]) -> int:
    drifted: list[str] = []
    for path, expected in outputs.items():
        if not path.is_file():
            drifted.append(f"MISSING {path.relative_to(ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            drifted.append(f"DRIFT {path.relative_to(ROOT)}")

    if drifted:
        for item in drifted:
            print(item)
        print("Run: python scripts/build.py")
        return 1

    print("OK: generated MoeProf artifacts match canonical sources")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify MoeProf adapters and compatibility packaging."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated artifacts are missing or stale.",
    )
    args = parser.parse_args()

    outputs = expected_outputs()
    if args.check:
        return check_outputs(outputs)

    write_outputs(outputs)
    return check_outputs(outputs)


if __name__ == "__main__":
    sys.exit(main())
