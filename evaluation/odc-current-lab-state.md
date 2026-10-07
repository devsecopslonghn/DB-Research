# ODC lab recovery — 7 October 2026

## Current state

**Snapshot timestamps:** 09:16:51–09:22:19 UTC, 7 October 2026; follow-up GETs completed immediately after the final capture timestamp. **Application/MetaDB healthy; historical POC metadata reusable; execution evidence incomplete; live Oracle reachability and SQL effects UNKNOWN.** Selected responses are retained in [sanitized current-lab evidence](odc-current-lab-evidence-20261007.json). Reusable means suitable for inspection and a separately authorized focused experiment, not accepted for production or automatic replay.

Inspection used Kubernetes GET/list/log reads, static file metadata/hash reads, `observer --version`, and authenticated ODC metadata/evidence GETs. An existing local credential for `odc_poc_approver` opened and closed application login sessions. No Kubernetes Secret values were read: only names were listed. No Oracle or MetaDB SQL, datasource connection test, database session, ticket submission/approval/execution, restart, resource update or secret modification occurred. Missing results were inspected through retrieval endpoints; old tests were not rerun.

### Cluster, route and workloads

| Item | Current observation |
| --- | --- |
| Context / cluster | `k8s-admin-public` / `k8s-public`; API `https://api.k8s.drgdevlab.com:6443`; current-context namespace is `argocd`, inspection explicitly used `oceanbase-odc` |
| Namespace | `oceanbase-odc`, Active |
| Endpoint | [ODC datasource UI](https://oceanbase.apps.drgdevlab.com/#/datasource); root HTTPS returned 200 |
| Route / ingress | Kubernetes Ingress `oceanbase-odc`, nginx; host `oceanbase.apps.drgdevlab.com`, `/` Prefix → `odc:8989`; load-balancer IP `103.162.31.149`; TLS host configured. This cluster exposes no OpenShift route API |
| Services | `odc`, ClusterIP `10.103.239.130`, port 8989; `oceanbase-metadb`, ClusterIP `10.107.205.195`, port 2881; `oceanbase-metadb-headless`, headless, port 2881. Both workload endpoints were present |
| ODC deployment | `odc`, desired/ready/available 1/1/1; UID `1e25ed2c-5ab1-4b4b-8edc-f4da5f5ea352` |
| MetaDB StatefulSet | `oceanbase-metadb`, desired/ready/available 1/1/1; UID `a437c09f-980b-425c-a78d-566952add6ca` |
| ODC pod | `odc-5b74c68b74-bzcp7`, Running/Ready, restarts **0**; created `2026-10-07T06:21:48Z`; UID `445e59c5-345f-4625-90a6-107c47562678` |
| MetaDB pod | `oceanbase-metadb-0`, Running/Ready, restarts **0**; created `2026-10-07T06:20:30Z`; UID `c4c97f43-3230-42ca-8814-e2077db930cd` |
| ODC application | `/api/v2/info` reports **4.4.1-20260116**; frontend meta reports `4.4.1-1768284552000`; build timestamp `1768548454.241` |
| ODC image | `oceanbase/odc:4.4.1_bp1@sha256:ee8ee48edea2907b1b2c11eac54c8603e554bdcc570eb11b0b1f9cef2ead040d`; running imageID has the same digest |
| MetaDB image | `oceanbase/oceanbase-ce:4.3.5-lts@sha256:31086a6900c21c479c2bcd942b6a28c53b17a51f4e9b9eb8eafcc596adfcd2e3`; running imageID has the same digest |
| MetaDB binary | `observer --version`: **OceanBase_CE 4.3.5.6**, revision `106000012026040916-560923b02bdb9ed88dbd7940ac97a2e183c09b29`. Initial command lacked the library path and exited 127; adding `LD_LIBRARY_PATH=/root/ob/observer/lib` allowed a version-only read. No server start or SQL |
| Resources | ODC requests 1 CPU/3 GiB, limits 2 CPU/4 GiB; MetaDB requests 2 CPU/8 GiB, limits 4 CPU/10 GiB |

Zero restart counts describe **these replacement pods**, not an uninterrupted lab lifetime. Their creation times establish replacement before this inspection; its cause was not investigated. Historical restarts are retained separately. Ready state and API availability do not prove Oracle execution correctness.

### Persistence, configuration and logs

| Item | Current observation |
| --- | --- |
| ODC PVC | `odc-data`, Bound, 5 GiB, `longhorn-workers`; UID `4f42837c-cece-4c5d-9603-0a42c34acad3`; mounted `/opt/odc/data` |
| MetaDB PVC | `data-oceanbase-metadb-10gi`, Bound, 10 GiB, `longhorn-workers`; UID `669aee81-1d78-486b-b78e-2d221638ccad`, retained unchanged from historical evidence |
| MetaDB mounts | Same data PVC supplies `/root/ob` and `/root/.obd/cluster`; diagnostic log mount is `emptyDir`, 2 GiB |
| ODC log mount | `/opt/odc/log` uses `emptyDir`; it is separate from the data PVC. Current data/log usage approximately 684 KiB/1.1 MiB; these sizes do not prove retention |
| Oracle connection plugin | Mounted `connect-plugin-oracle-4.4.1-20260116.jar`; current SHA-256 `873d828075d83e65967d8cede82b282f23e4e313c10861d4b7a16ed12ab21f33`. Historical runtime used a TCPS extension; there is no retained built-jar checksum comparison here, so byte identity of that extension is UNKNOWN |
| ConfigMaps | `kube-root-ca.crt`; `odc-oracle-tcps-src-272mgcf824` (mounted); `odc-oracle-tcps-src-f4t446b6g7` (not referenced by the current pod). Extension maps contain `OracleTcpsConnectionExtension.java` and `build-plugin.sh`; key sizes/hashes are retained, not raw contents |
| Secret names only | `odc-bootstrap`, `odc-oracle-poc` |
| Pod log sample | Read-only bounded tails: MetaDB 51 lines, 3 WARN/0 ERROR; ODC 7 lines, 0 WARN/0 ERROR. Raw logs were not retained. A short clean sample is not proof of incident-free operation |
| Application expiry | `/api/v2/info` reports `fileExpireHours=336` (14 days). The sampled 4 October tickets are younger; ordinary configured age expiry does not explain their unavailability by itself |

### Project, actors, inventory and workflows

`GET /api/v2/collaboration/projects/1` preserves `odc-oracle-poc`, project ID **1**, unique identifier `ODC_09376b66-7ad2-494f-a243-576c42647dff`. Project basic listing also preserves `odc-poc-bootstrap`, ID **2**; this account cannot read its detailed membership (403).

| Actor | ID | Current project role |
| --- | --- | --- |
| POC requester | 10000 | DEVELOPER |
| POC approver | 10001 | OWNER; authenticated inspection account |
| POC executor | 10002 | DBA |
| POC observer | 10003 | PARTICIPANT |
| admin | 1 | OWNER |

The historical outsider ID 10004 is not a project member. Its current organization-account state is UNKNOWN. Organization users/roles and datasource administration listings return empty results for the connected project account; individual datasource administration endpoints return 403. These are visibility limits, not evidence that users, global roles or datasources were deleted. Project database registry responses expose the five historical POC connections without accessing passwords or opening Oracle sessions.

All five exact historical database IDs still resolve to their original owner/schema and datasource IDs:

| Environment | Schema | Database ID | Datasource ID |
| --- | --- | --- | --- |
| dev | `ODC_POC_20261004_DEV` | 1000069 | 1000001 |
| sit | `ODC_POC_20261004_SIT` | 1000122 | 1000002 |
| POCUAT | `ODC_POC_20261004_UAT` | 1000184 | 1000003 |
| POCPROD | `ODC_POC_20261004_MOCKPROD` | 1000218 | 1000004 |
| dev / observer | `ODC_POC_20261004_OBSERVER` | 1000345 | 1000005 |

They retain host `adb.ap-mumbai-1.oraclecloud.com`, port **1521**, service `gaf051b0a6547f3_labdb_tp.adb.oraclecloud.com`. Registry `existed=true` and connection `enabled=true` are metadata; transient source status `TESTING` is not a new successful connection test. Schema existence, object validity, current Oracle version, grants and target effects were not queried. The historical target was Oracle **26ai EE 23.26.4.1.0**; that remains historical only. The separate bootstrap `oracle-cloud` datasource ID 1 was not administratively readable in this session.

Environment listing preserves default/dev/sit/prod plus POCUAT **1000021** and POCPROD **1000022**. Four built-in approval flows remain: Auto Approval **1**, Project Owner **2**, Project DBA **3**, Project Owner → Project DBA **4**. Current high-risk level **4** points to flow **4**; ticket 1000023 retains its completed OWNER then DBA nodes. This proves the historical approval record survives; it does not prove independent execution authorization or verified promotion.

### Tickets, attachments and audit

Project ticket listing returns **26 records, IDs 1000003–1000028**: 21 `EXECUTION_SUCCEEDED`, 5 `EXECUTION_FAILED`. These are product statuses, not acceptance results. Fourteen selected historical ticket details were read; nine with corresponding published artifact hashes still match. The capture's `sqlSha256`/`sqlBytes` are calculated locally from returned `sqlContent`, not native ODC checksum fields or enforcement. No SQL was executed or resubmitted.

| Record | Current readback |
| --- | --- |
| Valid PL/SQL tickets 1000006–1000010 | Metadata and final success status preserved; current Oracle effects UNKNOWN |
| INVALID procedure ticket 1000011 | Still `EXECUTION_SUCCEEDED`; approved SQL hash matches the historical artifact. Historical Oracle INVALID/PLS-00201 failure is unchanged; no new object query |
| Abort/partial ticket 1000012 | Still `EXECUTION_FAILED`; SQL hash matches historical artifact |
| Changed-content ticket 1000015 | Still `EXECUTION_FAILED`; creation/content persisted, not new checksum rejection evidence |
| UI ticket 1000017 | Still `EXECUTION_SUCCEEDED` |
| Approval ticket 1000023 | Requester 10000, approvals by 10001 then 10002, ASYNC operator 10000 retained; same SQL SHA-256 as published manual-approval evidence. Operator metadata alone is not an authenticated Execute-caller audit |
| Replay/duplicate tickets 1000024/26/27 | Failed replay ticket and two successful duplicate ticket records preserved; no new target marker counts |
| API approval ticket 1000028 | Still `EXECUTION_SUCCEEDED` |
| Logs, sample 1000011/12/23/28 | All GET log endpoints return HTTP 200 but contain **“read log failed”**; do not treat HTTP 200 as successful evidence retrieval |
| Results and attachments, same sample | All result GETs and attachment download GETs return **500**; downloads are not ZIPs. Count: 4 missing log readbacks, 4 unavailable result readbacks, 4 unavailable attachments |
| Audit | `GET /api/v2/audit/events?fuzzyUsername=POC` returns **403** for this account. Historical evidence retained 97 POC audit records; current count, search/export and post-replacement retention are UNKNOWN |

The data PVCs and historical ticket records survived pod replacement. Full log/result/attachment retention demonstrably does not work for the sampled old records. The exact cause of missing attachments is UNKNOWN; the ephemeral log mount and source's executor-host forwarding explain plausible failure surfaces, not a proved single root cause. No storage repair or recovery acceptance was attempted.

### Correlation and reuse boundary

Use [the responsibility comparison](odc-vs-ci-reference.md#3-historicalcurrent-correlation) for the historical/current matrix. The lab is **YES, conditionally reusable for inspection**: same pinned base images, same PVC UIDs, stable POC registry IDs, projects, roles and ticket content. **Oracle runtime reuse needs separate confirmation** of credentials/grants/route/current effects and a retention remedy. No 19c/21c, crash, restore, serialization or unknown-outcome acceptance is inferred.

This file records current state only. [Original ODC results](../ODC-ORACLE-POC-RESULTS.md), [historical API evidence](../evidence/oracle-poc-api.json), [manual approval evidence](../evidence/oracle-poc-manual-approval.json), and [historical PVC verification](../evidence/odc-oracle-portal-verification-20261004.json) remain unchanged.
