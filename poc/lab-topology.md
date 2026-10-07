# Existing lab and orchestration topology

Recorded 7 October 2026 from narrow read-only cluster metadata and retained repository evidence. No cluster configuration, workload, credential or Oracle object was changed.

| Component | Established evidence | Remaining confirmation |
| --- | --- | --- |
| Jenkins | Current context `k8s-admin-public`; namespace `jenkins`, StatefulSet/pod `jenkins` / `jenkins-0`; one ready replica; image `docker.io/jenkins/jenkins:2.568.3-jdk21`; ingress `jenkins.apps.drgdevlab.com` | Authenticated account access, approved job definition, actor IDs, restricted agent, owner and backup policy |
| Jenkins capability | Installed plugin file names include workflow-aggregator, pipeline-input-step, pipeline-utility-steps, credentials-binding, git, matrix-auth and kubernetes | Exact plugin versions/health, effective RBAC and input behavior were not tested |
| Existing Jenkins storage | PVC `jenkins-home-longhorn-target-5gi` is Bound | This does not establish a restricted agent's durable local SQLite volume or retained artifact policy |
| Existing Bytebase | Namespace `bytebase`, pod `bytebase-0`, image `bytebase/bytebase:3.22.1` at digest `sha256:d7aa62532fe5c789a46c51a1d53dadaaac316c7054d1e15733be4095f5f04139` | No connection/credential APIs or stored secrets accessed |
| Oracle route, historical nonsecret record | Host `adb.ap-mumbai-1.oraclecloud.com`, port 1521, service `gaf051b0a6547f3_labdb_tp.adb.oraclecloud.com`; TCPS with hostname verification; historical lab used TLS without wallet | Current service/PDB/DB identity, routing, TLS/mTLS policy and direct connection still require separate references |
| Oracle version, historical runtime | Oracle 26ai Enterprise Edition 23.26.4.1.0 on 4 October | Exact current version/RU is UNCONFIRMED; estate 19c/21c is not verified |
| POC target | One database/PDB + allowlisted service + one owner schema | `OSS_POC_WRITER` and `OSS_POC_OBSERVER` are proposed fixture names, not confirmed/provisioned accounts |
| Credentials | No Oracle/POC credential environment names injected into this session | Approved separate writer/observer references, restricted grants and rotation owner required |
| Source repository | `DB-Research` is a filesystem research workspace without `.git` | Approved Git source/commit needed for a genuine immutable release |

Nonsecret connection facts come from [ODC-CONNECTION-POC.md](../ODC-CONNECTION-POC.md) and [Bytebase runtime results](../BYTEBASE-ORACLE-POC-RESULTS.md), not extracted connection secrets. The user's reported active Bytebase connection establishes historical connectivity through that application's path; it cannot establish the POC principals, grants, current DB identity or runner TLS access. Bytebase secrets and `bytebase.cred` were not read or reused.

The disabled [allowlist example](inventory/targets.example.json) records only the historical route and unconfirmed identity placeholders. DBA confirmation requires a read-only `probe` with the approved separate credentials, comparison with existing lab records, and review of DB_NAME, DB_UNIQUE_NAME, CON_NAME, SERVICE_NAME and exact driver-reported version. Execution checks both writer and observer identities against the frozen allowlist. Use distinct observer grants exposing expected objects/diagnostics and approved deterministic calls; invisibility is a failed check, never proof of absence/validity.

The POC adds no Oracle system or environment schemas. No DEV/SIT/UAT/MOCKPROD promotion was configured. Existing historical schemas/results are not new POC targets by default.

## Runtime-prerequisite follow-up, 7 October 2026

[New discovery and preparation evidence](reports/runtime-prerequisites-20261007T095109Z/README.md) resolves local observer-package availability and confirms the existing engine pin, but does not establish an approved Oracle target or restricted runtime agent. Actual current Jenkins configuration uses `hudson.security.FullControlOnceLoggedInAuthorizationStrategy`, with controller executors 0 and private user realm. The two configured SSH agents are shared `NORMAL` nodes without `oracle-oss-poc`; no Kubernetes agent templates or reference-job markers were found. Named actors, source-author protection, persistent restricted state, credential binding and an approved Git source remain necessary. No controller/agent/security settings were changed.
