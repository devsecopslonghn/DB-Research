"""Verify fixed Oracle assertions through ODC SELECT-only sessions, or labeled fixtures."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from .build_release import verify_bundle
from .common import DemoError, ENVIRONMENTS, fail_cli, sanitize, write_json
from .odc_client import ODCClient


def assess(expected, actual, native_status):
    problems = []
    if native_status != "EXECUTION_SUCCEEDED":
        problems.append("ODC target has not completed successfully")
    if actual.get("query_status") != "SUCCESS":
        problems.append("Oracle verification queries did not all succeed")
    objects = actual.get("objects", [])
    for obj in expected["objects"]:
        matches = [o for o in objects if o.get("name") == obj["name"] and o.get("type") == obj["type"]]
        if len(matches) != 1 or matches[0].get("status") != "VALID":
            problems.append(f"{obj['name']} ({obj['type']}) is missing, duplicated or not VALID")
    if "errors" not in actual or not isinstance(actual["errors"], list):
        problems.append("USER_ERRORS evidence is missing")
    elif any(str(error.get("attribute", "ERROR")).upper() == "ERROR" for error in actual["errors"]):
        problems.append("USER_ERRORS contains compilation errors")
    if actual.get("data") != {"row_count": expected["data"]["row_count"], "active_count": expected["data"]["active_count"]}:
        problems.append("Reference-data counts differ from the contract")
    if actual.get("function", {}).get("result") != expected["function"]["expected"]:
        problems.append("Deterministic function result differs from the contract")
    return {"verification": "INVALID" if problems else "VERIFIED", "problems": problems}


def queries(envelope):
    expected = envelope["verification"]
    names = ",".join("'" + obj["name"] + "'" for obj in expected["objects"])
    return {
        "identity": "SELECT SYS_CONTEXT('USERENV','CURRENT_SCHEMA') AS SCHEMA_OWNER FROM DUAL",
        "objects": f"SELECT OBJECT_NAME, OBJECT_TYPE, STATUS FROM USER_OBJECTS WHERE OBJECT_NAME IN ({names}) ORDER BY OBJECT_NAME, OBJECT_TYPE",
        "errors": f"SELECT NAME, TYPE, LINE, POSITION, ATTRIBUTE, TEXT FROM USER_ERRORS WHERE NAME IN ({names}) ORDER BY NAME, SEQUENCE",
        "data": "SELECT COUNT(*) AS ROW_COUNT, SUM(CASE WHEN STATUS_CODE='ACTIVE' THEN 1 ELSE 0 END) AS ACTIVE_COUNT FROM DM_CP_CUSTOMER",
        "function": "SELECT DM_CP_LABEL('C0001') AS FUNCTION_RESULT FROM DUAL",
    }


def query_rows(results):
    rows = []
    for result in results:
        columns = result.get("columnLabels") or []
        for row in result.get("rows") or []:
            if len(columns) != len(row):
                raise DemoError("Oracle response column/row shape is incomplete")
            rows.append(dict(zip(columns, row)))
    return rows


def verify_live(client, envelope, receipt):
    if receipt.get("evidence_source") != "LIVE" or receipt.get("git_commit") != envelope["git_commit"] or receipt.get("sql_sha256") != envelope["sql_sha256"]:
        raise DemoError("Live verification receipt does not match immutable provenance")
    client.inventory(envelope["targets"])
    values = {}
    statements = queries(envelope)
    for target in envelope["targets"]:
        name = target["environment"]
        native_status = receipt.get("environments", {}).get(name, {}).get("native_status")
        if native_status != "EXECUTION_SUCCEEDED":
            values[name] = {"verification": "NOT_AVAILABLE", "reason": "ODC target is not EXECUTION_SUCCEEDED"}
            continue
        actual = {"environment": name, "database_id": target["odc_target_id"], "schema": target["schema"],
                  "observed_at": datetime.now(timezone.utc).isoformat(), "query_status": "FAILED"}
        try:
            identity = query_rows(client.read_only_sql(target["odc_target_id"], statements["identity"]))
            if identity != [{"SCHEMA_OWNER": target["schema"]}]:
                raise DemoError("Oracle session owner differs from approved target")
            objects = query_rows(client.read_only_sql(target["odc_target_id"], statements["objects"]))
            errors = query_rows(client.read_only_sql(target["odc_target_id"], statements["errors"]))
            data = query_rows(client.read_only_sql(target["odc_target_id"], statements["data"]))
            function = query_rows(client.read_only_sql(target["odc_target_id"], statements["function"]))
            if len(data) != 1 or len(function) != 1:
                raise DemoError("Oracle data/function query has an unexpected result count")
            actual.update({"query_status": "SUCCESS",
                           "objects": [{"name": o["OBJECT_NAME"], "type": o["OBJECT_TYPE"], "status": o["STATUS"]} for o in objects],
                           "errors": [{"name": e["NAME"], "type": e["TYPE"], "line": e["LINE"], "position": e["POSITION"],
                                       "attribute": e["ATTRIBUTE"], "text": e["TEXT"]} for e in errors],
                           "data": {"row_count": data[0]["ROW_COUNT"], "active_count": data[0]["ACTIVE_COUNT"]},
                           "function": {"result": function[0]["FUNCTION_RESULT"]}})
        except (DemoError, KeyError) as exc:
            actual["reason"] = str(exc)
        actual.update(assess(envelope["verification"], actual, native_status))
        values[name] = sanitize(actual, [client.password])
    return {"evidence_source": "LIVE", "release_id": envelope["release_id"], "git_commit": envelope["git_commit"],
            "sql_sha256": envelope["sql_sha256"], "environments": values}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--source", choices=("FIXTURE", "LIVE"), required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    client = None
    try:
        envelope = verify_bundle(args.bundle)
        if args.source == "FIXTURE":
            if not args.input:
                raise DemoError("Fixture verification requires a labeled input")
            fixture = json.loads(args.input.read_text())
            if fixture.get("evidence_source") != "FIXTURE" or fixture.get("release_id") != envelope["release_id"]:
                raise DemoError("Fixture source/release does not match")
            values = {}
            for name in ENVIRONMENTS:
                environment = fixture["environments"][name]
                actual = dict(environment.get("oracle", {}))
                actual.update(assess(envelope["verification"], actual, environment.get("native_status")))
                values[name] = actual
            result = {"evidence_source": "FIXTURE", "release_id": envelope["release_id"],
                      "git_commit": envelope["git_commit"], "sql_sha256": envelope["sql_sha256"], "environments": values}
        else:
            if not args.receipt:
                raise DemoError("Live verification requires a collected ODC receipt")
            client = ODCClient.from_env()
            client.login()
            result = verify_live(client, envelope, json.loads(args.receipt.read_text()))
        write_json(args.output, sanitize(result))
        print(f"Oracle verification contract rendered; evidence source={args.source}")
    except (DemoError, OSError, ValueError, KeyError) as exc:
        fail_cli(exc)
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
