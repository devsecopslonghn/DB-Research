"""Small shared contracts. No database credentials or migration executor."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import yaml

ROOT = Path(__file__).resolve().parents[2]
APPLICATION = "customer-profile"
ENVIRONMENTS = ("DEV", "SIT", "UAT", "MOCKPROD")
STATES = ("PREPARED", "VALIDATED", "WAITING_APPROVAL", "APPROVED", "EXECUTING",
          "EXECUTION_FAILED", "VERIFYING", "VERIFIED", "INVALID", "PARTIAL",
          "CORRECTION_REQUIRED")
RELEASE_PATTERN = re.compile(r"REL-\d{4}\.\d{2}-DEMO\d{2}(?:-FAIL|-FIX)?\Z")
FILE_PATTERN = re.compile(r"\d{3}_[a-z0-9_]+\.sql\Z")
OBJECT_PATTERN = re.compile(r"DM_CP_[A-Z0-9_]{1,24}\Z")
TARGETS = {
    "DEV": (1000069, 1000001, "ODC_POC_20261004_DEV", 1, "dev"),
    "SIT": (1000122, 1000002, "ODC_POC_20261004_SIT", 2, "sit"),
    "UAT": (1000184, 1000003, "ODC_POC_20261004_UAT", 1000021, "POCUAT"),
    "MOCKPROD": (1000218, 1000004, "ODC_POC_20261004_MOCKPROD", 1000022, "POCPROD"),
}


class DemoError(ValueError):
    """A bounded validation or integration error safe to explain."""


class UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise DemoError("YAML keys must be unique strings")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def load_yaml(path):
    try:
        value = yaml.load(Path(path).read_text(encoding="utf-8"), Loader=UniqueLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise DemoError(f"Cannot read valid YAML: {Path(path).name}") from exc
    if not isinstance(value, dict):
        raise DemoError("YAML document must be a mapping")
    return value


def app_root(root=ROOT):
    return Path(root) / "demo" / APPLICATION


def release_path(release_id, root=ROOT):
    if not isinstance(release_id, str) or not RELEASE_PATTERN.fullmatch(release_id):
        raise DemoError("Release ID is outside the demo allowlist format")
    base = app_root(root) / "migrations"
    path = base / release_id
    if path.is_symlink() or not path.is_dir() or path.resolve().parent != base.resolve():
        raise DemoError(f"Release directory is missing or unsafe: {release_id}")
    return path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    return sha256(Path(path).read_bytes())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def summary(text):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as stream:
            stream.write(text + "\n")


def git(root, *args):
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as exc:
        raise DemoError("Git source/provenance lookup failed") from exc


def environments(root=ROOT):
    configs = {}
    for name in ENVIRONMENTS:
        path = app_root(root) / "environments" / f"{name.lower()}.yaml"
        if path.is_symlink():
            raise DemoError("Environment configuration cannot be a symlink")
        value = load_yaml(path)
        expected = {"environment": name, "odc_target_id": TARGETS[name][0],
                    "odc_datasource_id": TARGETS[name][1], "schema": TARGETS[name][2],
                    "project_id": 1, "odc_environment_id": TARGETS[name][3], "odc_environment_name": TARGETS[name][4]}
        if value != expected:
            raise DemoError(f"{name}: configuration differs from approved isolated POC mapping")
        configs[name] = value
    return configs


def sanitize(value, secrets=()):
    """Drop sensitive fields and redact strings; use explicit response projections too."""
    secret_values = [str(s) for s in secrets if s]
    secret_values += [v for k, v in os.environ.items()
                      if re.search(r"(?:PASSWORD|TOKEN|COOKIE|CLIENT_SECRET)$", k) and v]
    sensitive = re.compile(r"password|passwd|secret|cookie|authorization|(?:access|refresh|csrf)?token|privatekey|kubeconfig", re.I)

    def clean(item):
        if isinstance(item, dict):
            return {str(k): clean(v) for k, v in item.items()
                    if not sensitive.search(re.sub(r"[^a-z]", "", str(k).lower()))}
        if isinstance(item, list):
            return [clean(v) for v in item]
        if isinstance(item, str):
            for secret in sorted(secret_values, key=len, reverse=True):
                item = item.replace(secret, "[REDACTED]")
            item = re.sub(r"(?i)(Bearer\s+)[\w.-]+", r"\1[REDACTED]", item)
            item = re.sub(r"\beyJ[\w-]+\.eyJ[\w-]+\.[\w-]+", "[REDACTED]", item)
            item = re.sub(r"(https?://)[^/@\s]+:[^/@\s]+@", r"\1[REDACTED]@", item)
            item = re.sub(r"(?i)((?:password|token|cookie|authorization)\s*[=:]\s*)[^\s,;]+",
                          r"\1[REDACTED]", item)
        return item
    return clean(value)


def table_cell(value):
    return str(value if value is not None else "NOT_AVAILABLE").replace("|", "\\|").replace("\n", " ")


def fail_cli(exc):
    print(f"BLOCKED: {sanitize(str(exc))}")
    raise SystemExit(1)
