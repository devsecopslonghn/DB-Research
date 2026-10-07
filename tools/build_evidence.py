"""Build source references and a local snapshot manifest."""
import csv
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {}
for parent in (ROOT / "evidence/source", ROOT / "evidence/additional-source"):
    for directory in parent.iterdir():
        if not (directory / ".git").exists():
            continue
        remote = subprocess.check_output(
            ["git", "-C", str(directory), "remote", "get-url", "origin"], text=True
        ).strip().removesuffix(".git")
        repo = remote.removeprefix("https://github.com/")
        sha = subprocess.check_output(
            ["git", "-C", str(directory), "rev-parse", "HEAD"], text=True
        ).strip()
        key = directory.name
        SOURCES[key] = {"repo": repo, "sha": sha, "directory": str(directory.relative_to(ROOT))}

RECORDS = []


def add(key, name, path, start, end, claim):
    source = SOURCES[key]
    file = ROOT / source["directory"] / path
    lines = file.read_text().splitlines()
    end = min(end, len(lines))
    if not (1 <= start <= end <= len(lines)):
        raise ValueError((name, path, start, end, len(lines)))
    RECORDS.append({
        "id": name, "repo": source["repo"], "sha": source["sha"], "file": path,
        "start": start, "end": end, "claim": claim,
        "url": f"https://github.com/{source['repo']}/blob/{source['sha']}/{path}#L{start}-L{end}",
        "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
    })


def match(key, name, path, needle, claim, context=8):
    lines = (ROOT / SOURCES[key]["directory"] / path).read_text().splitlines()
    line = next(i + 1 for i, text in enumerate(lines) if needle in text)
    add(key, name, path, max(1, line - 2), min(len(lines), line + context), claim)


af = "backend/src/main/java/com/bablsoft/accessflow/"
fw = "flyway-core/src/main/java/org/flywaydb/core/internal/"
fo = "flyway-database/flyway-database-oracle/src/main/java/org/flywaydb/database/oracle/"
lb = "liquibase-standard/src/main/java/liquibase/"
licenses = {
    "bablsoft__accessflow": ("AF-L", "LICENSE.md"),
    "bytebase__bytebase": ("BB-L", "LICENSE"),
    "minuth__open-migration": ("OM-L", "LICENSE"),
    "apegeek__schema-pilot": ("SP-L", "LICENSE.en"),
    "binout__flyway-ui": ("UI-L", "LICENSE"),
    "playframework__flyway-play": ("PLAY-L", "LICENSE.txt"),
    "liquibase__liquibase": ("LB5-L", "LICENSE"),
    "liquibase__liquibase__v4.33.0": ("LB4-L", "LICENSE.txt"),
    "flyway__flyway": ("FW-L", "LICENSE.txt"),
    "sqitchers__sqitch": ("SQ-L", "License.md"),
    "ariga__atlas": ("AT-L", "LICENSE"),
    "cookieY__Yearning": ("YE-L", "LICENSE"),
    "hhyo__Archery": ("AR-L", "LICENSE"),
    "Tareya__devops-archery": ("FORK-L", "LICENSE"),
    "dbdeploy": ("DEP-L", "LICENSE.md"),
    "dbmaintain": ("MAINT-L", "LICENSE.txt"),
    "dbpm": ("PM-L", "LICENSE"),
    "dbward": ("WARD-L", "LICENSE-APACHE"),
    "cloudbeaver": ("CB-L", "LICENSE"),
}
for key, (name, path) in licenses.items():
    source_dir = ROOT / SOURCES[key]["directory"]
    if not (source_dir / path).exists():
        candidates = [p for p in source_dir.iterdir() if p.is_file() and p.name.lower().startswith(('license', 'licence'))]
        path = candidates[0].name
    length = len((source_dir / path).read_text().splitlines())
    add(key, name, path, 1, min(length, 45), "License text. Read the complete file for its conditions.")

add("bytebase__bytebase", "BB-ENT", "LICENSE.enterprise", 1, 26, "Enterprise code requires a valid subscription for production use.")
add("bytebase__bytebase", "BB-PLAN", "backend/enterprise/plan.yaml", 1, 44, "The Free plan permits 10 instances and 20 seats. It lists the free features.")
add("bytebase__bytebase", "BB-GATES", "backend/enterprise/plan.yaml", 135, 163, "Approval, audit logs, enterprise SSO, custom roles, and external secrets require Enterprise.")
add("bytebase__bytebase", "BB-STATE", "backend/runner/taskrun/database_migrate_executor.go", 533, 600, "The runner skips central revisions. It executes SQL before creating the next central revision.")
add("bytebase__bytebase", "BB-ORA", "backend/plugin/db/oracle/oracle.go", 101, 218, "The Go Oracle driver splits SQL. It supports transaction and autocommit execution paths.")
match("bytebase__bytebase", "BB-DRIVER", "backend/plugin/db/oracle/oracle.go", "go-ora", "Oracle execution uses the Go go-ora driver.")
add("bablsoft__accessflow", "AF-PROM", af + "schemachange/internal/DefaultSchemaChangePromotionService.java", 77, 175, "Promotion checks central state and a central checksum. It submits an ordered request group.")
add("bablsoft__accessflow", "AF-GATE", af + "schemachange/internal/SchemaChangeStatementGate.java", 126, 150, "The schema gate refuses transaction markers, multiple statements, and DML.")
add("bablsoft__accessflow", "AF-SCAN", af + "schemachange/internal/SchemaChangeStatementScanner.java", 13, 88, "The scanner treats BEGIN as a transaction marker. Internal semicolons can fail the single-statement gate.")
add("bablsoft__accessflow", "AF-GROUP", af + "requestgroups/internal/GroupExecutionService.java", 152, 218, "The group executes target SQL before saving the member result centrally.")
add("bablsoft__accessflow", "AF-JDBC", af + "proxy/internal/DefaultQueryExecutor.java", 138, 163, "Relational execution uses a JDBC prepared statement.")
match("bablsoft__accessflow", "AF-ORA", af + "core/internal/DefaultJdbcCoordinatesFactory.java", 'case ORACLE -> "jdbc:oracle:thin:', "The built-in Oracle connector uses a Thin JDBC URL and the Oracle JDBC driver.", 85)
match("bablsoft__accessflow", "AF-SSO", "docs/07-security.md", "### SAML", "The security documentation describes SAML and OAuth/OIDC authentication.", 24)
match("bablsoft__accessflow", "AF-VAULT", "docs/07-security.md", "| HashiCorp Vault |", "The product resolves Vault, AWS, and Azure secret references.", 12)
match("bablsoft__accessflow", "AF-DR", "docs/09-deployment.md", "## Backup", "The deployment guide covers backup and recovery.", 25)
match("bablsoft__accessflow", "AF-CI", "docs/18-deployment-governance.md", "| GitLab CI |", "The repository provides a GitLab deployment gate template.", 12)
match("bablsoft__accessflow", "AF-DOC", "docs/20-schema-change-governance.md", "schema_change_sets", "The schema workflow stores its sets, statements, and promotions in central PostgreSQL.", 8)
add("bablsoft__accessflow", "AF-IAC", "docs/16-iac.md", 1, 17, "Terraform, OpenTofu, and CI templates manage governance resources through the REST API.")
add("bablsoft__accessflow", "AF-SIEM", "docs/09-deployment.md", 1018, 1036, "External audit sinks include Splunk, syslog, signed HTTPS, and S3 Object Lock.")
add("bablsoft__accessflow", "AF-RECOVERY", "docs/20-schema-change-governance.md", 389, 406, "The documentation identifies lost status projection and partial application without an in-module repair path.")
add("bablsoft__accessflow", "AF-DRIFT", "docs/20-schema-change-governance.md", 478, 498, "Oracle is a catalog-backed drift target. Sampling targets are excluded.")
add("bablsoft__accessflow", "AF-DISASTER", "docs/09-deployment.md", 1673, 1695, "Disaster recovery includes central database backup and preservation of audit ownership and keys.")
add("bablsoft__accessflow", "AF-AUDIT", "docs/07-security.md", 1825, 1844, "The audit log has a cryptographic chain and separate writer permissions.")
add("bablsoft__accessflow", "AF-REST", "docs/20-schema-change-governance.md", 235, 244, "The schema workflow exposes REST endpoints.")
match("dband-drm__drm-cli", "DRM-L", "package.json", '"license"', "The package declares ISC. The snapshot has no standalone license file.", 1)
add("dband-drm__drm-cli", "DRM-LOCAL", "README.md", 16, 44, "The installation metadata backend is SQLite or JSON.")
add("dband-drm__drm-cli", "DRM-FW", "modules/flyway.py", 233, 279, "The Flyway adapter requests dryRunOutput while generating SQL.")
add("dband-drm__drm-cli", "DRM-EXEC", "modules/oracle.py", 35, 45, "The Oracle URL parser accepts narrow IPv4 and service-name patterns.")
add("dband-drm__drm-cli", "DRM-SQLPLUS", "modules/oracle.py", 91, 132, "The adapter sends generated SQL to SQLPlus. It appends EXIT and checks the process exit code.")
add("dband-drm__drm-cli", "DRM-LB", "modules/liquibase.py", 238, 268, "The Liquibase adapter generates updateSql before native script execution.")
match("dband-drm__drm-cli", "DRM-RETRY", "modules/deploy.py", "queue retry", "The release layer retries a deployment. This does not prove safe statement replay.", 6)
add("minuth__open-migration", "OM-ENG", "server/services/engines/EngineFactory.ts", 1, 24, "The engine factory supports PostgreSQL, SQLite, MySQL, and MariaDB. It has no Oracle engine.")
add("minuth__open-migration", "OM-STATE", "server/services/engines/PostgresEngine.ts", 50, 105, "The target tracking table stores names and dates. PostgreSQL SQL and tracking inserts share a transaction.")
add("minuth__open-migration", "OM-RUN", "server/services/migration.service.ts", 99, 163, "Applied detection uses filenames. A failure does not stop the outer migration loop.")
add("minuth__open-migration", "OM-META", "server/database/schema.ts", 1, 42, "The central server uses SQLite metadata. The schema has no user identity on migration rows.")
match("minuth__open-migration", "OM-AUTH", "server/utils/auth.ts", "admin auth", "The application documents one administrator session.", 18)
match("apegeek__schema-pilot", "SP-EXEC", "server/server.js", "historyErrors: historyErrs", "The executor can report successful SQL with separate history errors.", 33)
add("apegeek__schema-pilot", "SP-DRIVERS", "server/server.js", 1, 12, "The server imports MySQL and PostgreSQL clients.")
add("binout__flyway-ui", "UI-DEPS", "pom.xml", 27, 35, "The project pins Flyway 2.2.1 and Java 6.")
add("binout__flyway-ui", "UI-SERVLET", "src/main/java/com/googlecode/flyway/ui/FlywayServlet.java", 32, 52, "The servlet displays a supplied Flyway instance. It is not a database inventory service.")
match("playframework__flyway-play", "PLAY-DEPS", "build.sbt", "defaultFlywayVersion", "The module pins its default Flyway dependency.", 6)
match("playframework__flyway-play", "PLAY-SCOPE", "README.md", "Flyway module for Play", "Flyway Play embeds migrations in a Play application.", 10)
add("flyway__flyway", "FW-ORA", fo + "OracleDatabase.java", 75, 135, "Oracle history stores version, checksum, actor, time, and success. Oracle DDL transactions are unsupported.")
add("flyway__flyway", "FW-PARSER", fo + "OracleParser.java", 145, 200, "The parser recognizes Oracle PL/SQL and slash delimiters.")
add("flyway__flyway", "FW-EXEC", fw + "command/DbMigrate.java", 437, 492, "The runner executes a migration before adding its successful history row.")
add("flyway__flyway", "FW-FAIL", fw + "command/DbMigrate.java", 340, 362, "For nontransactional failure, the runner records failure and requires recovery.")
match("flyway__flyway", "FW-CHECKSUM", fw + "info/MigrationInfoImpl.java", "CHECKSUM_MISMATCH", "Migration validation compares resolved checksums with applied history.", 18)
match("liquibase__liquibase__v4.33.0", "LB4-ORA", lb + "database/core/OracleDatabase.java", '"oracle.jdbc.OracleDriver"', "Liquibase 4.33 uses the Oracle JDBC driver.", 8)
add("liquibase__liquibase__v4.33.0", "LB4-STATE", lb + "sqlgenerator/core/CreateDatabaseChangeLogTableGenerator.java", 45, 67, "DATABASECHANGELOG stores identity, checksum, execution type, and deployment information.")
add("liquibase__liquibase__v4.33.0", "LB4-EXEC", lb + "changelog/visitor/UpdateVisitor.java", 115, 143, "Changeset execution occurs before the database records its execution status.")
match("liquibase__liquibase__v4.33.0", "LB4-SKIP", lb + "changelog/filter/ShouldRunChangeSetFilter.java", "CHANGESET_ALREADY_RAN_MESSAGE", "The changeset filter has an already-applied decision.", 60)
match("liquibase__liquibase__v4.33.0", "LB4-CHECKSUM", lb + "changelog/visitor/ValidatingVisitor.java", "isCheckSumValid", "Validation checks applied changeset checksums, subject to runOnChange and runAlways settings.", 15)
match("liquibase__liquibase__v4.33.0", "LB4-SEC", "SECURITY.md", "#", "The source includes a vulnerability reporting policy.", 20)
add("sqitchers__sqitch", "SQ-STATE", "lib/App/Sqitch/Engine/oracle.sql", 29, 52, "The Oracle registry stores change IDs, script hashes, and deployment identities.")
add("sqitchers__sqitch", "SQ-EVENTS", "lib/App/Sqitch/Engine/oracle.sql", 106, 141, "The target registry stores deploy, revert, fail, and merge events.")
add("sqitchers__sqitch", "SQ-EXEC", "lib/App/Sqitch/Engine.pm", 1041, 1068, "Sqitch runs a deploy script before verifying and recording the change.")
add("sqitchers__sqitch", "SQ-SQLPLUS", "lib/App/Sqitch/Engine/oracle.pm", 616, 640, "The Oracle engine invokes SQLPlus for scripts.")
add("sqitchers__sqitch", "SQ-INTEGRITY", "lib/App/Sqitch/Engine.pm", 1260, 1319, "The check command compares deployed script hashes with the plan and reports divergence.")
add("ariga__atlas", "AT-DRIVERS", "cmd/atlas/main.go", 12, 34, "The public CLI imports MySQL, PostgreSQL, SQLite, and related drivers. Oracle is absent here.")
add("cookieY__Yearning", "YE-SCOPE", "README.md", 6, 35, "The project documents MySQL auditing, approval, history, and RBAC.")
add("cookieY__Yearning", "YE-IDENTITY", "src/router/router.go", 76, 86, "The router exposes LDAP and OIDC login endpoints.")
add("hhyo__Archery", "AR-ORA", "sql/engines/oracle.py", 19, 50, "Oracle execution uses python-oracledb with SID or service-name connections.")
add("hhyo__Archery", "AR-EXEC", "sql/engines/oracle.py", 1108, 1212, "The workflow executes and commits each statement. It checks PL/SQL object compilation.")
add("hhyo__Archery", "AR-PARSER", "sql/utils/sql_utils.py", 151, 217, "The parser identifies procedures, functions, packages, triggers, and anonymous PL/SQL blocks.")
add("hhyo__Archery", "AR-STATE", "sql/models.py", 325, 411, "Central workflow records contain actor, target, time, SQL, review, and result.")
add("hhyo__Archery", "AR-SQLPLUS", "sql/engines/oracle.py", 786, 805, "The SQL review rejects SET, ROLLBACK, and EXIT commands.")
add("hhyo__Archery", "AR-IDENTITY", "archery/settings.py", 316, 343, "The settings configure an OIDC authentication backend.")
match("hhyo__Archery", "AR-LDAP", "archery/settings.py", "if ENABLE_LDAP:", "The settings configure LDAP authentication.", 25)
add("hhyo__Archery", "AR-API", "sql_api/urls.py", 57, 110, "REST endpoints cover workflow checks, review, execution, content, and logs.")
add("hhyo__Archery", "AR-DOC", "README.md", 24, 48, "The feature table distinguishes Oracle review, execution, backup, and other engine capabilities.")
match("Tareya__devops-archery", "FORK-EXEC", "sql/engines/oracle.py", "def execute_workflow", "The sampled derivative retains direct Oracle workflow execution.", 45)
add("dbmaintain", "MAINT-SCOPE", "README.md", 1, 19, "The maintainer states that DbMaintain is deprecated and no longer maintained.")
match("dbdeploy", "DEP-ORA", "src/Grillisoft.Tools.DatabaseDeploy.Oracle/OracleDatabase.cs", "Oracle.ManagedDataAccess", "The .NET dbdeploy implementation uses Oracle Managed Data Access.", 33)
add("dbdeploy", "DEP-STATE", "src/Grillisoft.Tools.DatabaseDeploy.Oracle/OracleScripts.cs", 35, 50, "Oracle history contains script name, deployment time, user, and hash.")
match("dbward", "WARD-SCOPE", "README.md", "Target Database (PostgreSQL / MySQL)", "The documented execution targets are PostgreSQL and MySQL.", 2)
match("dbward", "WARD-BOUNDARY", "README.md", "Team features", "OIDC and group authentication require commercial code.", 2)
add("dbward", "WARD-PLAN", "README.md", 475, 494, "The documented Free distribution limits database connections and users. Identity and audit export have paid boundaries.")
add("dbward", "WARD-STATE", "crates/dbward-driver/src/postgres.rs", 360, 381, "The target schema_migrations table stores only migration versions.")
add("dbward", "WARD-RUN", "crates/dbward-migrate/src/runner.rs", 18, 77, "The migration runner skips applied versions and reports partial application across multiple migrations.")
add("dbward", "WARD-REST", "README.md", 262, 294, "The server documents REST endpoints, role permissions, and audit verification.")
match("dbpm", "PM-SCOPE", "README.md", "DBPM_SQL_RUNNER", "dbpm requires SQLcl or SQLPlus and an in-database Core substrate.", 3)
match("dbpm", "PM-LIMITS", "README.md", "Non-lockfile installs", "Checksum verification differs between lockfile and non-lockfile installs.", 2)
add("cloudbeaver", "CB-ORA", "server/bundles/io.cloudbeaver.resources.drivers.base/plugin.xml", 1, 57, "The public server bundles an Oracle Thin JDBC driver declaration.")
add("cloudbeaver", "CB-SCOPE", "README.md", 1, 27, "CloudBeaver provides a shared web database editor and deployment instructions.")

(ROOT / "evidence/source-manifest.json").write_text(json.dumps(SOURCES, indent=2) + "\n")
(ROOT / "evidence/source-references.json").write_text(json.dumps(RECORDS, indent=2) + "\n")
with (ROOT / "evidence/source-references.csv").open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(RECORDS[0]))
    writer.writeheader()
    writer.writerows(RECORDS)
out = ["# Source evidence", "", "Research date: 2026-10-03.", "",
       "Each link uses the inspected Git commit. The file hash identifies the local source snapshot.", "",
       "## Repository snapshots", "", "| Repository | Commit | Local snapshot |", "|---|---|---|"]
for key, source in sorted(SOURCES.items()):
    out.append(f"| [{source['repo']}](https://github.com/{source['repo']}) | `{source['sha']}` | [{key}]({source['directory']}/) |")
out += ["", "## Source references", "", "| ID | Finding | File and lines |", "|---|---|---|"]
for row in RECORDS:
    out.append(f"| {row['id']} | {row['claim']} | [{row['file']}:{row['start']}–{row['end']}]({row['url']}) |")
out += ["", "## Official documentation", ""]
docs = [
    ("Bytebase plans", "https://www.bytebase.com/pricing/", "Community limits and paid governance features."),
    ("Open Source Definition", "https://opensource.org/definition-annotated", "Commercial-use restrictions conflict with the open-source definition."),
    ("Oracle transaction commits", "https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/committing-transactions.html", "Oracle commits around DDL statements."),
    ("Flyway Oracle", "https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database", "Oracle JDBC support and SQLPlus feature limits."),
    ("Flyway Oracle settings", "https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-oracle-namespace", "SQLPlus support requires the Teams tier."),
    ("Flyway settings", "https://documentation.red-gate.com/fd/flyway-namespace-277578913.html", "dryRunOutput requires the Teams tier."),
    ("Atlas compatibility", "https://atlasgo.io/features", "Oracle support requires Atlas Pro."),
    ("Liquibase 4.33 FAQ", "https://docs.liquibase.com/oss/user-guide-4-33/faq", "The 4.33 open-source license differs from current Community licensing."),
    ("Liquibase license change", "https://www.liquibase.com/blog/liquibase-community-for-the-future-fsl", "FSL terms and the future Apache license."),
    ("Archery Oracle review", "https://archerydms.com/modules/sql_check/", "Oracle PL/SQL support and restricted review rules."),
    ("DbMaintain documentation", "https://dbmaintain.github.io/docs/", "Target state, Oracle PL/SQL, and a native SQLPlus runner."),
    ("Jenkins pipeline input", "https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/", "Pipeline approval input and submitter restrictions."),
    ("Rundeck access control", "https://docs.rundeck.com/docs/learning/howto/acls/", "Job permissions and separation through access control policies."),
    ("Harness self-managed architecture", "https://developer.harness.io/docs/self-managed-enterprise-edition/reference-architecture", "The self-managed enterprise platform requires licensing."),
]
for title, url, claim in docs:
    out.append(f"- [{title}]({url}): {claim}")
out += ["", "## Evidence limits", "",
        "A source review does not prove runtime behavior or production reliability.",
        "Absence claims apply to the inspected execution paths and documented search sample.",
        "The search does not prove that no other project or fork exists.",
        "GitHub metadata changed during collection. Exact values remain in the captured responses.",
        "The report uses the repository release data when a README has an older release statement.",
        "The evidence pack does not assert that any candidate has no security vulnerabilities.", ""]
out += ['## ODC deployment evidence update', '', 'The original twenty snapshots and 103 source references remain unchanged.', 'ODC source findings resolve in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md#source-references).', 'The [ODC evaluation](ODC-EVALUATION.md) adds topology, Oracle onboarding, permission inheritance, APIs, language, and license boundaries.', 'The [sanitized runtime record](evidence/product-model/odc-runtime-20261003.json) records ODC 4.4.1 image, volume, readiness, and authenticated GET observations.', 'Deployment inspection does not verify Oracle execution. All 45 platform and Oracle acceptance cases remain NOT RUN.', '']
(ROOT / "EVIDENCE.md").write_text("\n".join(out))
print(f"Recorded {len(SOURCES)} source snapshots and {len(RECORDS)} source references.")
