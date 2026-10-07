import os
import re
import subprocess
from pathlib import Path

from poc.common import Rejected, digest


def jdbc_url(target):
    # No caller-supplied JDBC URL; hostname verification stays enabled.
    return ("jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST=" + target["host"] + ")"
            "(PORT=" + str(target["port"]) + "))(CONNECT_DATA=(SERVICE_NAME=" + target["service_name"] + "))"
            "(SECURITY=(SSL_SERVER_DN_MATCH=YES)))")


class Engine:
    def __init__(self, jar, approved_hash, version, driver, driver_policy):
        self.jar = Path(jar).resolve()
        if not self.jar.is_file() or digest(self.jar.read_bytes()) != approved_hash:
            raise Rejected("engine artifact checksum is not approved")
        if driver_policy.get("approved") is not True:
            raise Rejected("Oracle FUTC driver exception is not approved for the OSS-only branch")
        self.driver = Path(driver).resolve()
        if not self.driver.is_file() or digest(self.driver.read_bytes()) != driver_policy["sha256"]:
            raise Rejected("Oracle driver checksum is not approved")
        self.command = ["java", "-cp", str(self.jar) + os.pathsep + str(self.driver), "org.example.poc.Engine"]
        result = subprocess.run(self.command + ["--version"],
                                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin")},
                                capture_output=True, timeout=30, check=False)
        if result.returncode or b"OSS_POC_VERSION=" + version.encode() not in result.stdout.splitlines():
            raise Rejected("engine version is not approved")

    def run(self, target, migrations, timeout=300):
        secret = os.environ.get(target["writer_secret_env"])
        if not secret:
            raise Rejected("approved writer secret was not injected")
        # Remove inherited Flyway/Java options and unrelated credentials/configuration.
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8",
               "POC_JDBC_URL": jdbc_url(target), "POC_DB_USER": target["writer_user"],
               "POC_DB_PASSWORD": secret, "POC_SCHEMA": target["schema"],
               "POC_HISTORY_TABLE": target["history_table"], "POC_MIGRATIONS": str(migrations),
               "POC_EXPECT_DB_NAME": target["database_identity"]["db_name"],
               "POC_EXPECT_DB_UNIQUE_NAME": target["database_identity"]["db_unique_name"],
               "POC_EXPECT_CON_NAME": target["database_identity"]["con_name"],
               "POC_EXPECT_SERVICE": target["service_name"], "POC_EXPECT_ORACLE_VERSION": target["oracle_version"]}
        try:
            result = subprocess.run(self.command, env=env, cwd=str(migrations),
                                    capture_output=True, timeout=timeout, check=False)
        except (subprocess.TimeoutExpired, OSError):
            return {"outcome": "UNKNOWN_OUTCOME", "reason": "engine interrupted or timed out"}
        # Raw library stdout/stderr is deliberately discarded: it can contain secrets/SQL.
        marker = re.findall(rb"(?m)^OSS_POC_RESULT=(SUCCESS:[0-9]+|SQL_FAILURE|UNKNOWN_OUTCOME)\r?$", result.stdout)
        if result.returncode == 0 and marker == [b"SUCCESS:1"]:
            return {"outcome": "SUCCESS", "exit_code": 0, "migrations_executed": 1}
        if result.returncode == 42 and marker == [b"SQL_FAILURE"]:
            return {"outcome": "PARTIAL", "exit_code": 42, "reason": "DDL may already have committed"}
        return {"outcome": "UNKNOWN_OUTCOME", "exit_code": result.returncode,
                "reason": "no unambiguous single-migration completion"}
