"""Bounded lexical SQL checks; deliberately not an Oracle parser or safety proof."""
import argparse
import json
from pathlib import Path
import re

from .common import ROOT, DemoError, app_root, fail_cli, load_yaml

PATTERNS = {
    "ALTER_SYSTEM": r"\bALTER\s+SYSTEM\b",
    "CREATE_USER": r"\bCREATE\s+USER\b",
    "DROP_USER": r"\bDROP\s+USER\b",
    "GRANT_DBA": r"\bGRANT\s+DBA\b",
    "ALTER_USER": r"\bALTER\s+USER\b",
    "GRANT_ANY_PRIVILEGE": r"\bGRANT\b[^;\n]*\bANY\b",
    "DYNAMIC_SQL": r"\bEXECUTE\s+IMMEDIATE\b|\bDBMS_SQL\s*\.",
    "DROP_TABLE": r"\bDROP\s+TABLE\b",
    "TRUNCATE_TABLE": r"\bTRUNCATE\s+TABLE\b",
    "COMMIT": r"\bCOMMIT\b",
    "ROLLBACK": r"\bROLLBACK\b",
    "WHENEVER": r"(?m)^\s*WHENEVER\b",
    "SPOOL": r"(?m)^\s*SPOOL\b",
    "AT_SCRIPT": r"(?m)^\s*@@?\S",
    "SUBSTITUTION": r"&&?[A-Za-z0-9_]",
}
LEVELS = {"INFO", "WARNING", "REQUIRES_DBA_REVIEW", "BLOCKED"}


def lexical_views(sql):
    """Mask comments/strings while preserving line positions, including Oracle q literals."""
    code = list(sql)
    uncommented = list(sql)
    token = re.compile(r"--[^\n]*|/\*[\s\S]*?\*/|q'(?P<open>[\[\{\(<])|q'(?P<other>[^\s])|'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"", re.I)
    offset = 0
    while True:
        match = token.search(sql, offset)
        if not match:
            break
        end = match.end()
        if match.group("open") or match.group("other"):
            delimiter = match.group("open") or match.group("other")
            closing = {"[": "]", "{": "}", "(": ")", "<": ">"}.get(delimiter, delimiter)
            location = sql.find(closing + "'", end)
            end = len(sql) if location < 0 else location + 2
        is_comment = sql[match.start():].startswith(("--", "/*"))
        for i in range(match.start(), end):
            if sql[i] != "\n":
                code[i] = " "
                if is_comment:
                    uncommented[i] = " "
        offset = end
    return "".join(code), "".join(uncommented)


def analyze(sql, policy=None):
    if policy is None:
        policy = load_yaml(app_root(ROOT) / "policies" / "sql-policy.yaml")
    if set(policy) != {"version", "rules", "limitations"} or policy["version"] != 1:
        raise DemoError("Invalid SQL policy schema")
    rules = policy["rules"]
    if not isinstance(rules, dict) or set(rules) != set(PATTERNS) or any(v not in LEVELS for v in rules.values()):
        raise DemoError("Policy must classify every known SQL pattern")
    for key in ("ALTER_SYSTEM", "CREATE_USER", "DROP_USER", "GRANT_DBA", "ALTER_USER", "GRANT_ANY_PRIVILEGE"):
        if rules[key] != "BLOCKED":
            raise DemoError("Administrative SQL policy cannot be weakened")
    if rules["DYNAMIC_SQL"] not in ("REQUIRES_DBA_REVIEW", "BLOCKED"):
        raise DemoError("Dynamic SQL requires explicit DBA review")
    code, uncommented = lexical_views(sql)
    findings = []
    for name, pattern in PATTERNS.items():
        view = uncommented if name == "SUBSTITUTION" else code
        for match in re.finditer(pattern, view, re.I):
            findings.append({"rule": name, "level": rules[name],
                             "line": sql[:match.start()].count("\n") + 1})
    types = []
    for match in re.finditer(r"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+|NONEDITIONABLE\s+)?(TABLE|SEQUENCE|INDEX|VIEW|FUNCTION|PROCEDURE|PACKAGE|TRIGGER)\b|\b(INSERT|UPDATE|DELETE|MERGE)\b", code, re.I):
        name = (match.group(1) or match.group(2)).upper()
        if name not in types:
            types.append(name)
    plsql = bool(re.search(r"\b(FUNCTION|PROCEDURE|PACKAGE|TRIGGER|DECLARE|BEGIN)\b", code, re.I))
    if plsql and not types:
        types.append("PLSQL_BLOCK")
    errors = []
    if not code.strip():
        errors.append("SQL file is empty or comments only")
    if plsql and not re.search(r"(?m)^\s*/\s*$", code):
        errors.append("Oracle PL/SQL requires a standalone slash delimiter")
    if any(f["level"] == "BLOCKED" for f in findings):
        errors.append("SQL contains a BLOCKED policy pattern")
    return {"sql_types": types, "plsql": plsql, "findings": findings, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sql_file", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(args.sql_file.read_text(encoding="utf-8"))
        print(json.dumps(result, indent=2))
        if result["errors"]:
            raise SystemExit(1)
    except (DemoError, OSError) as exc:
        fail_cli(exc)


if __name__ == "__main__":
    main()
