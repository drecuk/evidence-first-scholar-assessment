#!/usr/bin/env python3
"""Validate the repository marketplace, plugin package, and optional release archive."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath


SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")


def add(checks: list[dict[str, str]], status: str, name: str, detail: str) -> None:
    checks.append({"status": status, "check": name, "detail": detail})


def load_json(path: Path, checks: list[dict[str, str]]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(checks, "FAIL", f"parse {path.name}", str(exc))
        return {}
    if not isinstance(data, dict):
        add(checks, "FAIL", f"parse {path.name}", "top level must be an object")
        return {}
    add(checks, "PASS", f"parse {path.name}", str(path))
    return data


def validate_skill(skill_dir: Path, checks: list[dict[str, str]]) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        add(checks, "FAIL", "skill entrypoint", f"missing {skill_file}")
        return
    text = skill_file.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        add(checks, "FAIL", "skill frontmatter", "missing opening YAML frontmatter")
        return
    name_match = re.search(r"^name:\s*(.+)$", frontmatter.group(1), re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+)$", frontmatter.group(1), re.MULTILINE)
    if not name_match or name_match.group(1).strip() != skill_dir.name:
        add(checks, "FAIL", "skill name", "frontmatter name must match directory")
    else:
        add(checks, "PASS", "skill name", skill_dir.name)
    if not description_match or not description_match.group(1).strip():
        add(checks, "FAIL", "skill description", "missing nonblank description")
    else:
        add(checks, "PASS", "skill description", "present")
    if len(skill_file.read_bytes()) > 1024 * 1024:
        add(checks, "FAIL", "skill size", "SKILL.md exceeds 1 MiB")
    else:
        add(checks, "PASS", "skill size", f"{skill_file.stat().st_size} bytes")
    for marker in ("TODO", "<placeholder>", "REPLACE_ME"):
        if marker in text:
            add(checks, "FAIL", "skill placeholders", f"found {marker}")


def validate_archive(archive: Path, expected_root: str, checks: list[dict[str, str]]) -> None:
    if not archive.is_file():
        add(checks, "FAIL", "archive exists", str(archive))
        return
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        unsafe = []
        prohibited = []
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                unsafe.append(name)
            if any(part in {".git", "node_modules", "__MACOSX", "__pycache__"} for part in path.parts):
                prohibited.append(name)
            if path.name in {".DS_Store", ".app.json", ".env"}:
                prohibited.append(name)
        if unsafe:
            add(checks, "FAIL", "archive path safety", ", ".join(unsafe))
        else:
            add(checks, "PASS", "archive path safety", f"{len(names)} entries")
        if prohibited:
            add(checks, "FAIL", "archive hygiene", ", ".join(prohibited))
        else:
            add(checks, "PASS", "archive hygiene", "no prohibited files")
        manifest = f"{expected_root}/plugin.json"
        if manifest not in names:
            add(checks, "FAIL", "archive root", f"missing {manifest}")
        else:
            add(checks, "PASS", "archive root", manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    checks: list[dict[str, str]] = []
    marketplace_path = root / ".agents/plugins/marketplace.json"
    marketplace = load_json(marketplace_path, checks) if marketplace_path.is_file() else {}
    if not marketplace:
        add(checks, "FAIL", "marketplace", f"missing or invalid {marketplace_path}")
        plugin_dir = root / "plugins/evidence-first-scholar-assessment"
    else:
        entries = marketplace.get("plugins", [])
        if len(entries) != 1:
            add(checks, "FAIL", "marketplace entries", f"expected 1, found {len(entries)}")
            plugin_dir = root / "plugins/evidence-first-scholar-assessment"
        else:
            source = entries[0].get("source", {})
            path_text = source.get("path", "") if isinstance(source, dict) else ""
            if not path_text.startswith("./"):
                add(checks, "FAIL", "marketplace path", "source.path must start with ./")
            plugin_dir = root / path_text.removeprefix("./")
            if plugin_dir.is_dir():
                add(checks, "PASS", "marketplace path", str(plugin_dir))
            else:
                add(checks, "FAIL", "marketplace path", f"missing {plugin_dir}")

    manifest_path = plugin_dir / "plugin.json"
    manifest = load_json(manifest_path, checks) if manifest_path.is_file() else {}
    if not manifest:
        add(checks, "FAIL", "portable manifest", f"missing or invalid {manifest_path}")
    else:
        if manifest.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            add(checks, "PASS", "plugin schema", manifest["$schema"])
        else:
            add(checks, "FAIL", "plugin schema", str(manifest.get("$schema")))
        name = manifest.get("name", "")
        if NAME.fullmatch(name) and "--" not in name and ".." not in name and len(name) <= 64:
            add(checks, "PASS", "plugin name", name)
        else:
            add(checks, "FAIL", "plugin name", repr(name))
        version = manifest.get("version", "")
        if SEMVER.fullmatch(version):
            add(checks, "PASS", "plugin version", version)
        else:
            add(checks, "FAIL", "plugin version", repr(version))
        interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
        for key, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)):
            value = interface.get(key, "")
            if isinstance(value, str) and value.strip() and len(value) <= limit:
                add(checks, "PASS", f"interface {key}", f"{len(value)}/{limit} characters")
            else:
                add(checks, "FAIL", f"interface {key}", f"invalid or over {limit} characters")
        prompts = interface.get("defaultPrompt", [])
        if isinstance(prompts, str):
            prompts = [prompts]
        if isinstance(prompts, list) and 1 <= len(prompts) <= 3 and all(isinstance(p, str) and 0 < len(p) <= 128 and "\n" not in p for p in prompts):
            add(checks, "PASS", "default prompts", f"{len(prompts)} prompts")
        else:
            add(checks, "FAIL", "default prompts", "must be 1-3 nonblank single-line prompts <=128 characters")
        for key in ("logo", "composerIcon"):
            value = interface.get(key, "")
            target = plugin_dir / value.removeprefix("./") if isinstance(value, str) else Path()
            if isinstance(value, str) and value.startswith("./") and target.is_file():
                add(checks, "PASS", key, f"{value} ({target.stat().st_size} bytes)")
            else:
                add(checks, "FAIL", key, f"missing referenced asset {value!r}")
        if any(key in manifest for key in ("skills", "mcpServers", "interface")):
            add(checks, "FAIL", "portable top-level fields", "portable manifest contains compatibility-only component fields")
        else:
            add(checks, "PASS", "portable top-level fields", "no compatibility-only component fields")

    skills_root = plugin_dir / "skills"
    skill_dirs = [path for path in skills_root.iterdir() if path.is_dir()] if skills_root.is_dir() else []
    if not skill_dirs:
        add(checks, "FAIL", "skills", "no skill directories")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, checks)

    prohibited_source = []
    for path in plugin_dir.rglob("*") if plugin_dir.is_dir() else []:
        if path.name in {".DS_Store", ".app.json", ".env"} or path.is_symlink():
            prohibited_source.append(str(path.relative_to(plugin_dir)))
    if prohibited_source:
        add(checks, "FAIL", "source hygiene", ", ".join(prohibited_source))
    else:
        add(checks, "PASS", "source hygiene", "no prohibited files or symlinks")

    if args.archive:
        validate_archive(args.archive.resolve(), plugin_dir.name, checks)

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {"status": status, "repo_root": str(root), "plugin_dir": str(plugin_dir), "checks": checks}
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

