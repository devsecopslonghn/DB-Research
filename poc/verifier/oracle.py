import os

from poc.common import Rejected


def connect(target, role):
    try:
        import oracledb
    except ImportError:
        raise Rejected("approved python-oracledb dependency is unavailable") from None
    secret = os.environ.get(target[role + "_secret_env"])
    if not secret:
        raise Rejected("approved separate Oracle secret was not injected")
    try:
        params = oracledb.ConnectParams(host=target["host"], port=target["port"],
                                        service_name=target["service_name"], protocol="tcps",
                                        ssl_server_dn_match=True, tcp_connect_timeout=10, retry_count=0)
        conn = oracledb.connect(user=target[role + "_user"], password=secret, params=params)
        conn.call_timeout = 15000
        return conn
    except Exception:
        raise Rejected("Oracle connection failed; inspect privately through approved access") from None


def identity(conn, target, role):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT SYS_CONTEXT('USERENV','DB_NAME'),
            SYS_CONTEXT('USERENV','DB_UNIQUE_NAME'), SYS_CONTEXT('USERENV','CON_NAME'),
            SYS_CONTEXT('USERENV','SERVICE_NAME'), USER, SYS_CONTEXT('USERENV','CURRENT_SCHEMA') FROM DUAL""")
        db_name, unique, con_name, service, user, schema = cursor.fetchone()
    observed = {"database_identity": {"db_name": db_name, "db_unique_name": unique, "con_name": con_name},
                "service_name": service, "user": user, "current_schema": schema, "oracle_version": conn.version}
    if (observed["database_identity"] != target["database_identity"] or service != target["service_name"]
            or conn.version != target["oracle_version"] or user != target[role + "_user"]
            or schema != target[role + "_user"]):
        raise Rejected("live Oracle identity/version/schema differs from approved target")
    return observed


def verify(conn, target, expected):
    details = {"objects": [], "effects": [], "invocations": []}
    missing, invalid, effect_failure = False, False, False
    with conn.cursor() as cursor:
        for obj in expected["objects"]:
            binds = {"owner": target["schema"], "name": obj["name"], "kind": obj["type"]}
            cursor.execute("SELECT OWNER,OBJECT_NAME,OBJECT_TYPE,STATUS FROM ALL_OBJECTS "
                           "WHERE OWNER=:owner AND OBJECT_NAME=:name AND OBJECT_TYPE=:kind", binds)
            rows = cursor.fetchall()
            cursor.execute("SELECT LINE,POSITION,ATTRIBUTE,MESSAGE_NUMBER FROM ALL_ERRORS "
                           "WHERE OWNER=:owner AND NAME=:name AND TYPE=:kind ORDER BY SEQUENCE", binds)
            errors = cursor.fetchall()
            # Message text can include SQL/literals; retain positions/codes, not raw text.
            details["objects"].append({"expected": obj, "rows": [list(r) for r in rows],
                                       "diagnostics": [list(r) for r in errors]})
            missing |= len(rows) != 1
            invalid |= any(r[3] != "VALID" for r in rows) or any(e[2] == "ERROR" for e in errors)
        for effect in expected["effects"]:
            cursor.execute('SELECT COUNT(*) FROM "' + target["schema"] + '"."' + effect["table"]
                           + '" WHERE "' + effect["key_column"] + '"=:key', {"key": effect["key"]})
            count = int(cursor.fetchone()[0])
            details["effects"].append({"expected": effect, "observed_count": count})
            effect_failure |= count != effect["expected_count"]
        # Only explicitly approved deterministic POC calls; never invoke invalid/missing objects.
        if not missing and not invalid:
            for call in expected["invocations"]:
                import oracledb
                argument = cursor.var(oracledb.DB_TYPE_CLOB)
                argument.setvalue(0, call["clob_input"])
                result = cursor.callfunc('"' + target["schema"] + '"."' + call["function"] + '"',
                                         oracledb.DB_TYPE_NUMBER, [argument])
                details["invocations"].append({"function": call["function"], "observed_number": str(result),
                                               "expected_number": call["expected_number"]})
                effect_failure |= result != call["expected_number"]
    verdict = "INVALID" if invalid else "FAILED" if missing or effect_failure else "VERIFIED"
    return {"verification_status": verdict, **details}


class Observer:
    def preflight(self, target):
        if not target["enabled"]:
            raise Rejected("lab target is disabled pending DBA confirmation")
        if any(v == "UNCONFIRMED" for v in target["database_identity"].values()):
            raise Rejected("lab identity is not confirmed")
        observations = {}
        for role in ("observer", "writer"):
            with connect(target, role) as conn:
                observations[role] = identity(conn, target, role)
        return observations

    def check(self, target, expected):
        with connect(target, "observer") as conn:
            observed = identity(conn, target, "observer")
            return {"identity": observed, **verify(conn, target, expected)}

    def probe(self, target):
        # Read-only discovery before enabling/reviewing inventory. No credentials returned.
        observations = {}
        for role in ("observer", "writer"):
            with connect(target, role) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT SYS_CONTEXT('USERENV','DB_NAME'), SYS_CONTEXT('USERENV','DB_UNIQUE_NAME'), "
                                   "SYS_CONTEXT('USERENV','CON_NAME'), SYS_CONTEXT('USERENV','SERVICE_NAME'), USER FROM DUAL")
                    row = cursor.fetchone()
                observations[role] = dict(zip(("db_name", "db_unique_name", "con_name", "service_name", "user"), row))
                observations[role]["oracle_version"] = conn.version
        return observations
