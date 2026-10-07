import re
import subprocess
from pathlib import Path

from poc.common import Rejected, digest, expectations, identifier, require_actor


def git_artifact(repo, commit, relative_path, suffix=".sql"):
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise Rejected("exact Git commit required")
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts or path.suffix != suffix:
        raise Rejected("invalid Git artifact path")
    try:
        frozen = subprocess.run(["git", "-C", str(repo), "show", commit + ":" + path.as_posix()],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    except subprocess.CalledProcessError:
        raise Rejected("SQL is unavailable at the exact Git commit") from None
    if frozen != (Path(repo) / path).read_bytes():
        raise Rejected("working SQL differs from the exact Git commit")
    return frozen


def envelope(release_id, commit, version, target_id, target, requester, sql, expected, policy, loss_after_success=False):
    require_actor(policy, "requesters", requester)
    identifier(release_id)
    identifier(target_id)
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise Rejected("exact Git commit required")
    if not re.fullmatch(r"[1-9][0-9]{0,17}", version):
        raise Rejected("numeric migration version required")
    if loss_after_success and policy.get("allow_failure_instrumentation") is not True:
        raise Rejected("failure instrumentation is not authorized")
    if not sql or len(sql) > 1024 * 1024:
        raise Rejected("SQL size outside bounded POC limit")
    try:
        text = sql.decode("utf-8")
    except UnicodeDecodeError:
        raise Rejected("SQL must be UTF-8") from None
    if "\x00" in text or text.startswith("\ufeff"):
        raise Rejected("NUL and BOM are unsupported")
    # Conservative admission gate, not an Oracle parser; literals may cause false rejection.
    if re.search(r"(?im)^\s*(?:@|@@|PROMPT\b|SET\b|DEFINE\b|UNDEFINE\b|SPOOL\b|WHENEVER\b|CONNECT\b|HOST\b|START\b|EXIT\b)", text) or re.search(r"&[A-Za-z_]|\$\{", text):
        raise Rejected("native client directives/substitutions require corpus decision")
    return {
        "release_id": release_id, "git_commit": commit, "migration_version": version,
        "artifact_sha256": digest(sql), "target_id": target_id, "target": target,
        "database_identity": target["database_identity"], "service_or_pdb": target["service_or_pdb"],
        "schema": target["schema"], "requested_by": requester,
        "engine": policy["engine"], "engine_version": policy["engine_version"],
        "engine_sha256": policy["engine_sha256"], "expected": expectations(expected),
        "oracle_driver": policy["oracle_driver"],
        "execution_options": {"placeholder_replacement": False, "create_schemas": False,
                              "baseline": False, "clean": False, "automatic_retry": False,
                              "loss_after_engine_success": loss_after_success},
    }
