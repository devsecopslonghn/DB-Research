import json
import re
from pathlib import Path

from poc.common import Rejected, identifier, oracle_identifier


def resolve(path, target_id):
    identifier(target_id)
    targets = json.loads(Path(path).read_text())["targets"]
    if len(targets) != 1 or target_id not in targets:
        raise Rejected("target is not in the single-target allowlist")
    target = targets[target_id]
    required = {"enabled", "database_identity", "service_or_pdb", "schema", "host", "port",
                "service_name", "oracle_version", "writer_user", "observer_user", "writer_secret_env",
                "observer_secret_env", "tls", "history_table"}
    if set(target) != required:
        raise Rejected("invalid target inventory fields")
    for field in ("schema", "writer_user", "observer_user", "history_table"):
        oracle_identifier(target[field])
    if target["writer_user"] != target["schema"] or target["observer_user"] == target["writer_user"]:
        raise Rejected("separate owner writer and observer are required")
    for field in ("host", "service_name"):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,252}", target[field]):
            raise Rejected("invalid allowlisted network route")
    for field in ("writer_secret_env", "observer_secret_env"):
        if not re.fullmatch(r"OSS_POC_[A-Z_]+_PASSWORD", target[field]):
            raise Rejected("invalid secret reference")
    if target["writer_secret_env"] == target["observer_secret_env"]:
        raise Rejected("separate credential references are required")
    if type(target["port"]) is not int or not 1 <= target["port"] <= 65535:
        raise Rejected("invalid allowlisted port")
    if type(target["enabled"]) is not bool or target["tls"] is not True:
        raise Rejected("this lab POC requires authenticated TCPS")
    if set(target["database_identity"]) != {"db_name", "db_unique_name", "con_name"}:
        raise Rejected("database/PDB identity is incomplete")
    return target


def lock_key(target):
    # Service aliases do not define a new write scope.
    from poc.common import canonical
    return canonical([target["database_identity"], target["schema"]])
