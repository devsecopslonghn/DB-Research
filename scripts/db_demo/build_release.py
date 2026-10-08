"""Package exact committed release bytes and provenance without executing SQL."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil

from .common import (ENVIRONMENTS, ROOT, DemoError, app_root, environments,
                     fail_cli, file_hash, git, release_path, sha256, summary, write_json)
from .validate_manifest import validate_release


def source_metadata(root=ROOT):
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    return {"git_repository": os.environ.get("GITHUB_REPOSITORY", "devsecopslonghn/DB-Research"),
            "git_commit": commit,
            "git_branch": os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME") or git(root, "branch", "--show-current").decode().strip(),
            "github_actor": os.environ.get("GITHUB_ACTOR", "LOCAL_OPERATOR"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID", "NOT_AVAILABLE"),
            "created_at": git(root, "show", "-s", "--format=%cI", commit).decode().strip()}


def build_release(release_id, output, root=ROOT, metadata=None, committed=True):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise DemoError("Release output must be new or empty; existing artifacts are immutable")
    if output.resolve().is_relative_to(Path(root).resolve() / "demo" / "customer-profile" / "migrations"):
        raise DemoError("Release artifacts cannot overwrite source releases")
    validation, manifest = validate_release(release_id, root)
    if validation["errors"]:
        raise DemoError("Release did not pass static validation")
    metadata = metadata or source_metadata(root)
    path = release_path(release_id, root)
    sources = [path / "manifest.yaml"] + [path / f for f in manifest["migrations"]]
    sources += [app_root(root) / "environments" / f"{e.lower()}.yaml" for e in ENVIRONMENTS]
    sources += [app_root(root) / "policies" / "sql-policy.yaml"]
    if committed:
        for source in sources:
            if source.read_bytes() != git(root, "show", f"{metadata['git_commit']}:{source.relative_to(root).as_posix()}"):
                raise DemoError("Release/configuration differs from the recorded commit")
    if not committed and metadata.get("evidence_source") != "FIXTURE":
        raise DemoError("Uncommitted sample builds must be explicitly labeled FIXTURE")
    bundle = output / "release-bundle"
    bundle.mkdir(parents=True)
    for source in sources:
        relative = source.relative_to(path) if source.is_relative_to(path) else source.relative_to(app_root(root))
        target = bundle / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    sql = b"\n".join((path / f).read_bytes() for f in manifest["migrations"]) + b"\n"
    (bundle / "migration.sql").write_bytes(sql)
    envelope = {"schema_version": 1, "release_id": release_id, "application": manifest["application"],
                **metadata, "evidence_source": metadata.get("evidence_source", "GIT"),
                "state": "PREPARED", "manifest_sha256": validation["manifest_sha256"],
                "sql_sha256": sha256(sql), "policy_sha256": file_hash(app_root(root) / "policies" / "sql-policy.yaml"),
                "targets": [{**value, "configuration_sha256": file_hash(app_root(root) / "environments" / f"{name.lower()}.yaml")}
                            for name, value in environments(root).items()],
                "rollout": manifest["rollout"], "verification": manifest["verification"],
                "approval": manifest["approval"], "migrations": validation["migrations"],
                "corrects": manifest.get("corrects"), "depends_on": manifest.get("depends_on")}
    write_json(output / "release-envelope.json", envelope)
    write_json(output / "validation-report.json", validation)
    verify_bundle(output, root)
    return envelope


def verify_bundle(directory, root=ROOT):
    directory = Path(directory)
    try:
        envelope = json.loads((directory / "release-envelope.json").read_text())
        release_id = envelope["release_id"]
        if not re.fullmatch(r"[0-9a-f]{40}", envelope.get("git_commit", "")) or envelope.get("git_repository") != "devsecopslonghn/DB-Research" or envelope.get("evidence_source") not in ("GIT", "FIXTURE"):
            raise DemoError("Envelope source repository/commit/evidence label is invalid")
        validation, manifest = validate_release(release_id, root)
        expected_targets = [{**config, "configuration_sha256": file_hash(app_root(root) / "environments" / f"{name.lower()}.yaml")}
                            for name, config in environments(root).items()]
        if envelope["schema_version"] != 1 or envelope["application"] != manifest["application"] or envelope["targets"] != expected_targets:
            raise DemoError("Envelope target/application allowlist mismatch")
        if envelope["manifest_sha256"] != validation["manifest_sha256"] or envelope["migrations"] != validation["migrations"]:
            raise DemoError("Envelope migration/manifest hashes differ from reviewed source")
        for key in ("rollout", "verification", "approval"):
            if envelope[key] != manifest[key]:
                raise DemoError(f"Envelope {key} differs from its manifest")
        if envelope.get("corrects") != manifest.get("corrects") or envelope.get("depends_on") != manifest.get("depends_on"):
            raise DemoError("Envelope correction/dependency differs from manifest")
        bundle = directory / "release-bundle"
        if envelope["manifest_sha256"] != file_hash(bundle / "manifest.yaml"):
            raise DemoError("Bundled manifest hash mismatch")
        expected_files = {"manifest.yaml", "migration.sql", "policies/sql-policy.yaml"}
        for migration in envelope["migrations"]:
            filename = migration["file"]
            expected_files.add(filename)
            if migration["sha256"] != file_hash(bundle / filename):
                raise DemoError("Bundled migration hash mismatch")
        sql = b"\n".join((bundle / m["file"]).read_bytes() for m in envelope["migrations"]) + b"\n"
        if (bundle / "migration.sql").read_bytes() != sql or envelope["sql_sha256"] != sha256(sql):
            raise DemoError("Combined SQL is not the exact ordered migrations")
        policy_hash = file_hash(app_root(root) / "policies" / "sql-policy.yaml")
        if envelope["policy_sha256"] != policy_hash or file_hash(bundle / "policies" / "sql-policy.yaml") != policy_hash:
            raise DemoError("Policy hash mismatch")
        for target in envelope["targets"]:
            name = f"environments/{target['environment'].lower()}.yaml"
            expected_files.add(name)
            if file_hash(bundle / name) != target["configuration_sha256"]:
                raise DemoError("Bundled target configuration hash mismatch")
        actual_files = {p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()}
        if actual_files != expected_files or any(p.is_symlink() for p in bundle.rglob("*")):
            raise DemoError("Release bundle contains unexpected files or symlinks")
        if envelope["evidence_source"] == "GIT":
            original = release_path(release_id, root)
            for name in expected_files - {"migration.sql"}:
                source = original / name if "/" not in name else app_root(root) / name
                if (bundle / name).read_bytes() != git(root, "show", f"{envelope['git_commit']}:{source.relative_to(root).as_posix()}"):
                    raise DemoError("Artifact source bytes are not present in the recorded Git commit")
        return envelope
    except (OSError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, DemoError):
            raise
        raise DemoError("Malformed or missing release artifact") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        envelope = build_release(args.release_id, args.output)
        summary(f"## Release prepared\n\nRelease: `{envelope['release_id']}`  \nCommit: `{envelope['git_commit']}`  \nTargets: DEV → SIT → UAT → MOCKPROD  \nState: **PREPARED**; ODC ticket: NOT_AVAILABLE (no execution).\n")
        print(f"PREPARED: {envelope['release_id']} ({len(envelope['migrations'])} migration files)")
    except (DemoError, OSError) as exc:
        fail_cli(exc)


if __name__ == "__main__":
    main()
