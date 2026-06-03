#!/usr/bin/env python3
"""Validate the delego plugin: the marketplace/plugin/MCP manifests parse with
the required fields, and every SKILL.md and agent has well-formed frontmatter.

Run from the repo root:  python scripts/validate.py
Requires: pyyaml.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("validate.py needs pyyaml:  pip install pyyaml")

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
fails = 0


def fail(msg: str) -> None:
    global fails
    fails += 1
    print(f"FAIL {msg}")


def ok(msg: str) -> None:
    print(f"ok   {msg}")


# --- manifests --------------------------------------------------------------- #
try:
    mp = json.load(open(".claude-plugin/marketplace.json", encoding="utf-8"))
    if not mp.get("name") or not isinstance(mp.get("plugins"), list) or not mp["plugins"]:
        raise ValueError("needs a name and a non-empty plugins[]")
    ok(f"marketplace.json: '{mp['name']}' with {len(mp['plugins'])} plugin(s)")
except Exception as e:  # noqa: BLE001
    fail(f"marketplace.json: {e}")

try:
    pj = json.load(open("delego/.claude-plugin/plugin.json", encoding="utf-8"))
    if not KEBAB.fullmatch(pj.get("name", "")):
        raise ValueError("name must be kebab-case")
    ok(f"plugin.json: '{pj['name']}' v{pj.get('version', '(git sha)')}")
except Exception as e:  # noqa: BLE001
    fail(f"plugin.json: {e}")

try:
    mcp = json.load(open("delego/.mcp.json", encoding="utf-8"))
    if not mcp.get("mcpServers"):
        raise ValueError("no mcpServers")
    ok(f".mcp.json: servers {list(mcp['mcpServers'])}")
except Exception as e:  # noqa: BLE001
    fail(f".mcp.json: {e}")


# --- skills (name must equal directory) -------------------------------------- #
def frontmatter(path: str) -> dict | None:
    m = FRONTMATTER.match(open(path, encoding="utf-8").read())
    return (yaml.safe_load(m.group(1)) or {}) if m else None


for path in sorted(glob.glob("delego/skills/*/SKILL.md")):
    directory = os.path.basename(os.path.dirname(path))
    fm = frontmatter(path)
    if fm is None:
        fail(f"{path}: missing frontmatter")
        continue
    name, desc = str(fm.get("name", "")), fm.get("description", "")
    problems = []
    if name != directory:
        problems.append(f"name {name!r} != dir {directory!r}")
    if not KEBAB.fullmatch(name):
        problems.append("name not kebab-case")
    if not isinstance(desc, str) or len(desc) < 40:
        problems.append("description too short")
    (fail if problems else ok)(f"{path}: " + ("; ".join(problems) or name))

# --- agents (kebab name, unique across the tree) ----------------------------- #
seen: dict[str, str] = {}
for path in sorted(glob.glob("delego/agents/*/*.md")):
    fm = frontmatter(path)
    if fm is None:
        fail(f"{path}: missing frontmatter")
        continue
    name, desc = str(fm.get("name", "")), fm.get("description", "")
    problems = []
    if not KEBAB.fullmatch(name):
        problems.append("name not kebab-case")
    if not isinstance(desc, str) or len(desc) < 40:
        problems.append("description too short")
    if name in seen:
        problems.append(f"duplicate name {name!r} (also {seen[name]})")
    else:
        seen[name] = path
    (fail if problems else ok)(f"{path}: " + ("; ".join(problems) or name))

print()
print("plugin valid" if not fails else f"{fails} problem(s)")
sys.exit(1 if fails else 0)
