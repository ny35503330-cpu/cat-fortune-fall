#!/usr/bin/env python3
"""Audit Claude-style agentic YAML frontmatter for Codex migration.

This script is intentionally dependency-free. It does not modify files.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


INTERESTING_KEYS = {
    "agent",
    "pair",
    "autoInvoke",
    "context",
    "model",
    "effort",
    "tools",
    "allowed-tools",
    "disable-model-invocation",
    "maxTurns",
    "memory",
    "background",
    "isolation",
    "hooks",
    "user-invocable",
    "argument-hint",
}


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    return match.group(1) if match else None


def parse_top_level_keys(frontmatter: str) -> dict[str, str]:
    data: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_value
        if current_key is not None:
            data[current_key] = "\n".join(current_value).strip()
        current_key = None
        current_value = []

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith((" ", "\t", "-")) and ":" in line:
            flush()
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip()]
        elif current_key is not None:
            current_value.append(line)
    flush()
    return data


def classify(path: Path, meta: dict[str, str]) -> list[str]:
    flags: list[str] = []
    if "agent" in meta or "context" in meta:
        flags.append("delegation")
    if "pair" in meta or path.name.startswith("assign-") or "/assign-" in path.as_posix():
        flags.append("generator-evaluator-pair")
    if meta.get("autoInvoke", "").lower() in {"true", "yes", "1"}:
        flags.append("auto-invoke-needs-rewrite")
    if "disable-model-invocation" in meta:
        flags.append("script-or-reference-only")
    if "tools" in meta or "allowed-tools" in meta:
        flags.append("tool-guidance-not-permission")
    if "hooks" in meta:
        flags.append("hooks-need-codex-config")
    if "model" in meta or "effort" in meta:
        flags.append("model-hint")
    return flags or ["simple"]


def audit(root: Path) -> dict:
    source_roots = [root / ".claude" / "skills", root / ".claude" / "agents"]
    rows = []
    key_counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    by_flag: defaultdict[str, list[str]] = defaultdict(list)

    for source_root in source_roots:
        if not source_root.exists():
            continue
        for path in sorted(source_root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            frontmatter = extract_frontmatter(text)
            if frontmatter is None:
                continue
            meta = parse_top_level_keys(frontmatter)
            keys = sorted(meta.keys())
            key_counts.update(keys)
            flags = classify(path, meta)
            flag_counts.update(flags)
            rel = path.relative_to(root).as_posix()
            for flag in flags:
                by_flag[flag].append(rel)
            rows.append(
                {
                    "path": rel,
                    "name": meta.get("name", ""),
                    "description": meta.get("description", ""),
                    "keys": keys,
                    "interesting": sorted(k for k in keys if k in INTERESTING_KEYS),
                    "flags": flags,
                }
            )

    return {
        "root": root.as_posix(),
        "total_files_with_frontmatter": len(rows),
        "key_counts": dict(key_counts.most_common()),
        "flag_counts": dict(flag_counts.most_common()),
        "by_flag": {k: v[:50] for k, v in sorted(by_flag.items())},
        "files": rows,
    }


def print_markdown(report: dict) -> None:
    print("# Agentic YAML Audit")
    print()
    print(f"- root: `{report['root']}`")
    print(f"- files with frontmatter: {report['total_files_with_frontmatter']}")
    print()
    print("## Flag counts")
    print()
    print("| flag | count |")
    print("|---|---:|")
    for flag, count in report["flag_counts"].items():
        print(f"| `{flag}` | {count} |")
    print()
    print("## Key counts")
    print()
    print("| key | count |")
    print("|---|---:|")
    for key, count in report["key_counts"].items():
        print(f"| `{key}` | {count} |")
    print()
    print("## Files needing Codex rewrite attention")
    print()
    print("| path | flags | interesting keys |")
    print("|---|---|---|")
    for row in report["files"]:
        if row["flags"] == ["simple"]:
            continue
        flags = ", ".join(f"`{f}`" for f in row["flags"])
        keys = ", ".join(f"`{k}`" for k in row["interesting"])
        print(f"| `{row['path']}` | {flags} | {keys} |")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    report = audit(Path(args.root).resolve())
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_markdown(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
