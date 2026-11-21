#!/usr/bin/env python3
"""Conservative portable-skill structure checks, not a behavioral evaluator."""
import argparse
import json
import re
import yaml
from pathlib import Path


def check(root):
    root = Path(root).resolve()
    errors, warnings = [], []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["Missing SKILL.md"], []
    if any(p.is_symlink() for p in root.rglob("*")):
        errors.append("Symlinks are not portable package resources")
    text = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
    if not match:
        return ["Missing YAML frontmatter delimiters"], warnings
    header, body = match.groups()
    try:
        fields = yaml.safe_load(header)
    except yaml.YAMLError:
        return ["Invalid YAML frontmatter"], warnings
    if not isinstance(fields, dict):
        return ["Frontmatter must be an object"], warnings
    if not isinstance(fields.get("name"), str) or not isinstance(fields.get("description"), str):
        return ["Name and description must be strings"], warnings
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields.get("name", "")):
        errors.append("Invalid or missing name")
    if len(fields.get("name", "")) > 64:
        errors.append("Name exceeds 64 characters")
    if not fields.get("description") or fields.get("description") in ("|", ">"):
        errors.append("Use a non-empty single-line description for this checker")
    if not body.strip():
        errors.append("Empty instructions")
    if len(body.splitlines()) > 500:
        warnings.append("Long entry: consider conditional references")
    if re.search(r"\b(?:TODO|FIXME|replace-with-task-name)\b", text):
        errors.append("Unresolved placeholder")
    refs = re.findall(r"`((?:references|scripts|assets)/[^`\s]+)`", body)
    refs += re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", body)
    for ref in refs:
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
            continue
        ref = ref.split("#", 1)[0]
        if any(char in ref for char in "*<>"):
            warnings.append("Manual reference check required: " + ref)
            continue
        target = (root / ref).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append("Missing or escaping resource: " + ref)
    if re.search(r"(?:/workspace/|/mnt/data/|/root/)", body):
        errors.append("Author-specific absolute path in entry")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    errors, warnings = check(args.directory)
    print(json.dumps({"status": "failed" if errors else "structurally_checked",
                      "errors": errors, "warnings": warnings,
                      "behavior_validation": "not_performed"}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
