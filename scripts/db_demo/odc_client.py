"""Supported ODC API handoff. Deliberately provides no approve/execute operation."""
import argparse
import base64
import http.cookiejar
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

from .build_release import verify_bundle
from .common import DemoError, ENVIRONMENTS, fail_cli, sanitize, summary, write_json


class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        before, after = urllib.parse.urlsplit(req.full_url), urllib.parse.urlsplit(newurl)
        if (before.scheme, before.netloc) != (after.scheme, after.netloc):
            raise DemoError("ODC cross-origin redirect refused")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class ODCClient:
    def __init__(self, base_url, username, password, timeout=20):
        parts = urllib.parse.urlsplit(base_url)
        if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment:
            raise DemoError("ODC_BASE_URL must be a credential-free HTTP(S) service URL")
        if parts.scheme == "http":
            try:
                private = ipaddress.ip_address(parts.hostname).is_private
            except ValueError:
                private = parts.hostname == "localhost" or parts.hostname.endswith((".local", ".svc.cluster.local"))
            if not private:
                raise DemoError("Public plaintext ODC authentication is refused")
        if not username or not password:
            raise DemoError("ODC_USERNAME and ODC_PASSWORD are required")
        self.base = base_url.rstrip("/")
        self.username, self.password, self.timeout = username, password, timeout
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(SameOriginRedirect(), urllib.request.HTTPCookieProcessor(self.cookies))

    @classmethod
    def from_env(cls):
        missing = [key for key in ("ODC_BASE_URL", "ODC_USERNAME", "ODC_PASSWORD") if not os.environ.get(key)]
        if missing:
            raise DemoError("Missing runtime configuration: " + ", ".join(missing))
        return cls(*(os.environ[key] for key in ("ODC_BASE_URL", "ODC_USERNAME", "ODC_PASSWORD")))

    def request(self, method, path, payload=None, form=None):
        if not path.startswith("/api/v2/") or ".." in path:
            raise DemoError("ODC request is outside supported API namespace")
        join = "&" if "?" in path else "?"
        url = self.base + path + join + "currentOrganizationId=1"
        headers = {"Accept": "application/json"}
        xsrf = next((c.value for c in self.cookies if c.name == "XSRF-TOKEN"), None)
        if xsrf:
            headers["X-XSRF-TOKEN"] = urllib.parse.unquote(xsrf)
        data = None
        if form is not None:
            data = urllib.parse.urlencode(form).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif payload is not None:
            data = json.dumps(payload).encode()
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(8 * 1024 * 1024 + 1)
                if len(raw) > 8 * 1024 * 1024:
                    raise DemoError("ODC response exceeds bounded collection limit")
                value = json.loads(raw)
        except urllib.error.HTTPError as exc:
            raise DemoError(f"ODC endpoint returned HTTP {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise DemoError("ODC endpoint unavailable or response is not JSON") from None
        if not isinstance(value, dict) or value.get("successful") is not True:
            raise DemoError("ODC API rejected the request")
        return value.get("data", value)

    def login(self):
        data = self.request("GET", "/api/v2/encryption/publicKey")
        public_key = data.get("publicKey") if isinstance(data, dict) else data
        if not isinstance(public_key, str):
            raise DemoError("ODC encryption public key is unavailable")
        if not public_key.startswith("-----BEGIN"):
            public_key = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----\n"
        # Only public key material is written; the password stays on subprocess stdin.
        with tempfile.TemporaryDirectory(prefix="odc-public-key-") as temp:
            path = Path(temp) / "public.pem"
            path.write_text(public_key)
            try:
                result = subprocess.run(["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", str(path),
                                         "-pkeyopt", "rsa_padding_mode:pkcs1"], input=self.password.encode(),
                                        capture_output=True, check=True, timeout=10)
            except (OSError, subprocess.SubprocessError):
                raise DemoError("Supported ODC RSA login requires working openssl") from None
        encrypted = base64.b64encode(result.stdout).decode()
        self.request("POST", "/api/v2/iam/login", form={"username": self.username, "password": encrypted})
        if not list(self.cookies):
            raise DemoError("ODC login did not establish a session")

    def close(self):
        try:
            self.request("POST", "/api/v2/iam/logout")
        except DemoError:
            pass
        self.cookies.clear()

    def inventory(self, targets):
        verified = []
        for target in targets:
            database = self.request("GET", f"/api/v2/database/databases/{target['odc_target_id']}")
            source = database.get("dataSource") or {}
            project = database.get("project") or {}
            environment = database.get("environment") or {}
            if (database.get("id") != target["odc_target_id"] or database.get("name") != target["schema"] or
                    source.get("id") != target["odc_datasource_id"] or project.get("id") != target["project_id"] or
                    environment.get("id") != target["odc_environment_id"] or environment.get("name") != target["odc_environment_name"]):
                raise DemoError("Live ODC database/datasource/schema/project does not match the allowlist")
            verified.append({"environment": target["environment"], "database_id": database["id"],
                             "schema": database["name"], "datasource_id": source["id"], "project_id": project["id"],
                             "odc_environment_id": environment["id"], "odc_environment_name": environment["name"]})
        return verified

    def create_change(self, envelope, sql):
        from .common import sha256
        if sha256(sql.encode("utf-8")) != envelope["sql_sha256"]:
            raise DemoError("SQL bytes differ from the immutable envelope; no ticket was created")
        self.inventory(envelope["targets"])
        if envelope.get("evidence_source") == "FIXTURE":
            raise DemoError("Fixture artifacts cannot create live changes")
        description = (f"app={envelope['application']};release={envelope['release_id']};"
                       f"git={envelope['git_commit']};github_run={envelope['github_run_id']};"
                       f"sql_sha256={envelope['sql_sha256']}")
        request = {"databaseId": envelope["targets"][0]["odc_target_id"], "taskType": "MULTIPLE_ASYNC",
                   "executionStrategy": "MANUAL", "description": description,
                   "parameters": {"sqlContent": sql, "timeoutMillis": 120000, "errorStrategy": "ABORT",
                                  "generateRollbackPlan": False, "queryLimit": 100, "delimiter": ";",
                                  "retryTimes": 0, "markAsFailedWhenAnyErrorsHappened": True, "projectId": 1,
                                  "orderedDatabaseIds": [[t["odc_target_id"]] for t in envelope["targets"]],
                                  "manualTimeoutMillis": 86400000, "autoErrorStrategy": "ABORT"}}
        data = self.request("POST", "/api/v2/flow/flowInstances/", payload=request)
        contents = data.get("contents", []) if isinstance(data, dict) else []
        if len(contents) != 1 or type(contents[0].get("id")) is not int:
            # Never retry this POST blindly: an ambiguous create may already have succeeded.
            raise DemoError("ODC create outcome is ambiguous; inspect ODC before creating another ticket")
        return contents[0]["id"]

    def ticket(self, ticket_id):
        if type(ticket_id) is not int or ticket_id <= 0:
            raise DemoError("ODC ticket ID must be a positive integer")
        return self.request("GET", f"/api/v2/flow/flowInstances/{ticket_id}")

    def collect(self, ticket_id, envelope):
        detail = self.ticket(ticket_id)
        parameters = detail.get("parameters") or {}
        if detail.get("type") != "MULTIPLE_ASYNC" or parameters.get("orderedDatabaseIds") != [[t["odc_target_id"]] for t in envelope["targets"]] or parameters.get("sqlContent") is None:
            raise DemoError("Ticket does not match the release's native batch targets")
        from .common import sha256
        if sha256(parameters["sqlContent"].encode()) != envelope["sql_sha256"]:
            raise DemoError("ODC ticket SQL differs from the immutable release artifact")
        markers = {f"app={envelope['application']}", f"release={envelope['release_id']}", f"git={envelope['git_commit']}",
                   f"github_run={envelope['github_run_id']}", f"sql_sha256={envelope['sql_sha256']}"}
        if not markers <= set(detail.get("description", "").split(";")):
                raise DemoError("ODC ticket provenance does not match the release")
        approvals = []
        for node in detail.get("nodeList") or []:
            if node.get("nodeType") == "APPROVAL_TASK":
                operator = node.get("operator") or {}
                roles = operator.get("roleNames") or []
                if not roles:
                    candidate = next((c for c in node.get("candidates") or [] if c.get("id") == operator.get("id")), {})
                    roles = candidate.get("roleNames") or []
                approvals.append({"node_id": node.get("id"), "native_status": node.get("status"),
                                  "actor_id": operator.get("id"), "actor": operator.get("accountName") or operator.get("name"),
                                  "actor_roles": roles, "role_evidence": "native_operator_or_matching_project_candidate",
                                  "timestamp": node.get("completeTime"), "comment": node.get("comment")})
        statuses = {name: {"native_status": "NOT_AVAILABLE", "ticket_id": ticket_id} for name in ENVIRONMENTS}
        errors = []
        try:
            result = self.request("GET", f"/api/v2/flow/flowInstances/{ticket_id}/tasks/result")
            contents = result.get("contents", []) if isinstance(result, dict) else []
            records = [r for c in contents for r in c.get("databaseChangingRecordList", [])]
            for record in records:
                database = record.get("database") or {}
                for target in envelope["targets"]:
                    if database.get("id") == target["odc_target_id"]:
                        flow = record.get("flowInstanceDetailResp") or {}
                        statuses[target["environment"]] = {"native_status": record.get("status", "NOT_AVAILABLE"),
                                                          "ticket_id": ticket_id, "start": flow.get("executionTime"),
                                                          "end": flow.get("completeTime"),
                                                          "flow_created_at": flow.get("createTime")}
        except DemoError as exc:
            errors.append({"endpoint": "tasks/result", "status": "NOT_AVAILABLE", "reason": str(exc)})
        audit_events = []
        audit_collection = "NOT_AVAILABLE"
        try:
            start = detail.get("createTime")
            query = "/api/v2/audit/events?type=MULTIPLE_ASYNC&page=1&size=100"
            if type(start) is int:
                query += "&startTime=" + str(start - 60000)
            audits = self.request("GET", query)
            for event in audits.get("contents", []) if isinstance(audits, dict) else []:
                if str(event.get("taskId")) == str(ticket_id):
                    audit_events.append({k: event.get(k) for k in ("id", "action", "taskId", "username", "startTime", "endTime", "result")})
            audit_collection = "LIVE_PERSONAL_AUDIT_ONLY; only explicit taskId matches retained; create events may have no taskId"
        except DemoError as exc:
            errors.append({"endpoint": "audit/events", "status": "NOT_AVAILABLE", "reason": str(exc)})
        receipt = {"evidence_source": "LIVE", "release_id": envelope["release_id"], "git_commit": envelope["git_commit"],
                   "sql_sha256": envelope["sql_sha256"], "odc_batch_id": ticket_id, "native_status": detail.get("status"),
                   "approvals": approvals, "environments": statuses, "collection_errors": errors,
                   "requester_id": (detail.get("creator") or {}).get("id"),
                   "audit_references": [self.base + f"/api/v2/flow/flowInstances/{ticket_id}", self.base + f"/api/v2/flow/flowInstances/{ticket_id}/tasks/result",
                                        self.base + f"/api/v2/flow/flowInstances/{ticket_id}/tasks/asyncExecuteResult", self.base + "/api/v2/audit/events"],
                   "audit_collection": audit_collection, "audit_events": audit_events,
                   "execution_actor": "NOT_AVAILABLE: read Execute audit; task-node operator may be requester"}
        return sanitize(receipt, [self.password] + [c.value for c in self.cookies])

    def read_only_sql(self, database_id, sql):
        if database_id not in {1000069, 1000122, 1000184, 1000218} or not sql.lstrip().upper().startswith("SELECT ") or ";" in sql:
            raise DemoError("Verification accepts only built-in SELECT statements on approved targets")
        session = self.request("POST", f"/api/v2/datasource/databases/{database_id}/sessions")
        session_id = str(session.get("sessionId", ""))
        if not session_id:
            raise DemoError("ODC verification session is unavailable")
        if not session_id.startswith("sid:"):
            session_id = "sid:" + session_id
        try:
            initial = self.request("POST", f"/api/v2/datasource/sessions/{session_id}/sqls/streamExecute",
                                   payload={"sql": sql, "split": False, "queryLimit": 100, "addROWID": False,
                                            "showTableColumnInfo": False, "autoCommit": True, "continueExecutionOnError": False})
            request_id = initial.get("requestId")
            if request_id is None:
                raise DemoError("ODC query did not return a request ID")
            results = []
            for _ in range(60):
                data = self.request("GET", f"/api/v2/datasource/sessions/{session_id}/sqls/getMoreResults?requestId={urllib.parse.quote(str(request_id))}")
                results.extend(data.get("results") or [])
                if data.get("finished"):
                    if not results or any(r.get("status") != "SUCCESS" for r in results):
                        raise DemoError("ODC Oracle verification query failed")
                    return results
                time.sleep(0.5)
            raise DemoError("ODC verification query timed out; result is unknown")
        finally:
            try:
                self.request("DELETE", "/api/v2/datasource/sessions", payload={"sessionIds": [session_id]})
            except DemoError:
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation", choices=("create_odc_change", "collect_status"), required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ticket-id", type=int)
    args = parser.parse_args()
    client = None
    try:
        envelope = verify_bundle(args.bundle)
        client = ODCClient.from_env()
        client.login()
        if args.operation == "create_odc_change":
            if args.ticket_id:
                raise DemoError("Create does not accept an existing ticket ID")
            if (args.output / "odc-created.json").exists():
                raise DemoError("A create receipt already exists; collect that ticket instead of replaying create")
            ticket_id = client.create_change(envelope, (args.bundle / "release-bundle" / "migration.sql").read_bytes().decode("utf-8"))
            # Persist identity immediately, before result collection can fail.
            write_json(args.output / "odc-created.json", {"release_id": envelope["release_id"], "odc_batch_id": ticket_id,
                                                        "git_commit": envelope["git_commit"], "evidence_source": "LIVE"})
        else:
            if not args.ticket_id:
                raise DemoError("Collect requires the existing receipt's ticket ID")
            ticket_id = args.ticket_id
        receipt = client.collect(ticket_id, envelope)
        write_json(args.output / "odc-receipt.json", receipt)
        summary(f"## ODC handoff\n\nRelease: `{envelope['release_id']}`  \nCommit: `{envelope['git_commit']}`  \nODC ticket/batch: `{ticket_id}`  \nTargets: DEV → SIT → UAT → MOCKPROD  \nNative state: **{receipt['native_status']}**. Human review/approval and execution remain in ODC.\n")
        print(f"ODC batch {ticket_id}: {receipt['native_status']}")
    except (DemoError, OSError) as exc:
        fail_cli(exc)
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
