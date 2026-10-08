"""Validate releases, immutable source, ordering, hashes and static SQL policy."""
import argparse
import json
from pathlib import Path
import re

from .common import (APPLICATION, ENVIRONMENTS, FILE_PATTERN, OBJECT_PATTERN, ROOT,
                     DemoError, app_root, environments, file_hash, git, load_yaml,
                     release_path, summary, table_cell, write_json)
from .validate_sql import analyze


def validate_release(release_id, root=ROOT):
    path = release_path(release_id, root)
    manifest = load_yaml(path / "manifest.yaml")
    required = {"schema_version", "release_id", "application", "description", "migrations", "targets",
                "rollout", "approval", "verification"}
    if not required <= set(manifest) or set(manifest) - required - {"corrects", "depends_on"}:
        raise DemoError("Manifest has missing or unsupported keys; secrets/connection inputs are not allowed")
    if manifest["schema_version"] != 1 or manifest["release_id"] != release_id or manifest["application"] != APPLICATION:
        raise DemoError("Manifest release/application/schema version does not match its directory")
    if not isinstance(manifest["description"], str) or not 1 <= len(manifest["description"]) <= 500:
        raise DemoError("Release description must contain 1–500 characters")
    files = manifest["migrations"]
    if not isinstance(files, list) or not files or any(not isinstance(f, str) or not FILE_PATTERN.fullmatch(f) for f in files):
        raise DemoError("Migration names must be numbered SQL filenames without paths")
    if len(set(files)) != len(files):
        raise DemoError("Duplicate migration filenames")
    if files != sorted(files) or [int(f[:3]) for f in files] != list(range(1, len(files) + 1)):
        raise DemoError("Migrations must be ordered with consecutive unique prefixes starting at 001")
    if set(files) != {p.name for p in path.glob("*.sql")}:
        raise DemoError("Listed SQL files must exist and all release SQL must be declared")
    for filename in files + ["manifest.yaml"]:
        file = path / filename
        if file.is_symlink() or file.resolve().parent != path.resolve() or not file.is_file():
            raise DemoError("Release files cannot be symlinks or escape their release directory")
    if manifest["targets"] != list(ENVIRONMENTS) or manifest["rollout"] != {"mode": "manual", "order": list(ENVIRONMENTS)}:
        raise DemoError("Rollout must use the approved four environments in manual order")
    if manifest["approval"] != {"reviewers": ["OWNER", "DBA"], "execution": "authorized_manual_operator"}:
        raise DemoError("Independent OWNER/DBA review and manual execution are required")
    for key in ("depends_on", "corrects"):
        if key in manifest:
            if manifest[key] == release_id:
                raise DemoError("Release cannot depend on or correct itself")
            release_path(manifest[key], root)
    if release_id.endswith("-FIX") and "corrects" not in manifest:
        raise DemoError("Correction releases must identify the unchanged failed release")
    verification = manifest["verification"]
    if not isinstance(verification, dict) or set(verification) != {"object_status", "compile_errors", "expected_data", "objects", "data", "function"}:
        raise DemoError("Verification contract is incomplete")
    if any(verification.get(k) is not True for k in ("object_status", "compile_errors", "expected_data")):
        raise DemoError("Object, compilation and data checks cannot be disabled")
    objects = verification["objects"]
    if not isinstance(objects, list) or not objects:
        raise DemoError("Expected Oracle objects are required")
    for obj in objects:
        if not isinstance(obj, dict) or set(obj) != {"name", "type"} or not isinstance(obj["name"], str) or not OBJECT_PATTERN.fullmatch(obj["name"]) or obj["type"] not in {"TABLE", "SEQUENCE", "INDEX", "VIEW", "FUNCTION", "PROCEDURE", "PACKAGE", "PACKAGE BODY", "TRIGGER"}:
            raise DemoError("Oracle object contract must use synthetic DM_CP_ identifiers and known types")
    if len({(o["name"], o["type"]) for o in objects}) != len(objects):
        raise DemoError("Duplicate expected Oracle objects")
    if verification["data"] != {"table": "DM_CP_CUSTOMER", "row_count": 3, "active_count": 2} or verification["function"] != {"name": "DM_CP_LABEL", "input": "C0001", "expected": "C0001:Demo Customer One"}:
        raise DemoError("Unexpected demo data/function verification contract")
    environments(root)
    policy = load_yaml(app_root(root) / "policies" / "sql-policy.yaml")
    migrations = []
    errors = []
    for filename in files:
        result = analyze((path / filename).read_text(encoding="utf-8"), policy)
        migrations.append({"file": filename, "sha256": file_hash(path / filename), **result})
        errors.extend(f"{filename}: {e}" for e in result["errors"])
    return {"release_id": release_id, "manifest_sha256": file_hash(path / "manifest.yaml"),
            "status": "INVALID" if errors else "VALIDATED", "errors": errors,
            "migrations": migrations}, manifest


def changed_releases(root, base, head):
    for ref in (base, head):
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            raise DemoError("Diff references must be exact Git SHAs")
    names = git(root, "diff", "--name-only", "--no-renames", base, head, "--", "demo/", "scripts/db_demo/", ".github/workflows/").decode().splitlines()
    prefix = f"demo/{APPLICATION}/migrations/"
    releases = sorted({name[len(prefix):].split("/")[0] for name in names if name.startswith(prefix)})
    # Script/policy/environment changes affect all releases.
    if not releases or any(not name.startswith(prefix) for name in names):
        releases = sorted(p.name for p in (app_root(root) / "migrations").iterdir() if p.is_dir())
    changed = git(root, "diff", "--name-only", "--no-renames", base, head, "--", prefix).decode().splitlines()
    immutable_errors = []
    for name in changed:
        try:
            git(root, "cat-file", "-e", f"{base}:{name}")
        except DemoError:
            continue
        immutable_errors.append(f"Existing release file changed/deleted: {name}; create a new reviewed release")
    return releases, immutable_errors


def render(report):
    lines = ["# Database release validation", "", f"Result: **{report['status']}**", "",
             "Static checks are lexical checks, not Oracle execution or a full SQL parser.", "",
             "| Release | File | SHA-256 | SQL types | Policy findings |", "| --- | --- | --- | --- | --- |"]
    for release in report["releases"]:
        for migration in release.get("migrations", []):
            findings = "; ".join(f"{f['level']}:{f['rule']}@{f['line']}" for f in migration["findings"]) or "INFO: no listed dangerous pattern"
            lines.append("| " + " | ".join(table_cell(v) for v in [release["release_id"], migration["file"], migration["sha256"], ", ".join(migration["sql_types"]), findings]) + " |")
    if report["errors"]:
        lines += ["", "Errors:", ""] + [f"- {table_cell(e)}" for e in report["errors"]]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-id")
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {"status": "VALIDATED", "releases": [], "errors": []}
    try:
        if bool(args.base) != bool(args.head):
            raise DemoError("Both base and head are required for change detection")
        if args.base:
            releases, report["errors"] = changed_releases(ROOT, args.base, args.head)
        else:
            releases = [args.release_id] if args.release_id else sorted(p.name for p in (app_root() / "migrations").iterdir() if p.is_dir())
        if not releases:
            raise DemoError("No demo releases found")
        report["changed_releases"] = releases
        for release_id in releases:
            try:
                result, _ = validate_release(release_id)
                report["releases"].append(result)
                report["errors"].extend(result["errors"])
            except (DemoError, OSError, UnicodeError) as exc:
                report["errors"].append(f"{release_id}: {exc}")
    except (DemoError, OSError) as exc:
        report["errors"].append(str(exc))
    if report["errors"]:
        report["status"] = "INVALID"
    write_json(args.output / "validation-report.json", report)
    text = render(report)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "validation-report.md").write_text(text, encoding="utf-8")
    summary(text)
    print(f"Validation: {report['status']}; releases={len(report['releases'])}; errors={len(report['errors'])}")
    raise SystemExit(bool(report["errors"]))


if __name__ == "__main__":
    main()
