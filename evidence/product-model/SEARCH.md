# Product-model search record

The search used Bytebase's documented resource model before screening alternatives.
Research date: 2026-10-03.
Search results supplied leads. Repository source and official documentation supplied technical conclusions.
Commercial comparison lists and engine lists did not establish platform equivalence.

## Requested search phrases

All twelve phrases received browser search requests:

1. `Bytebase alternative open source`
2. `Bytebase open source alternative`
3. `Bytebase alternative self hosted`
4. `database DevOps platform open source`
5. `database change management platform open source`
6. `database release management web UI open source`
7. `database deployment control plane open source`
8. `database lifecycle management open source`
9. `database CI/CD platform open source`
10. `database migration management server open source`
11. `schema change management platform open source`
12. `database governance platform open source`

Additional indexed GitHub README searches used `alternative to Bytebase`, `similar to Bytebase`, and `Bytebase alternative`.
They also used `database DevOps`, `database change management`, and `database release management`.
The search identified Dokeeper through its copied Bytebase comparison text.
It identified NineData Community documentation through a database change-management search.
Neither lead established a new unrestricted OSS platform.

## Topic searches

All six requested GitHub topic URLs received browser requests:

| Topic | Access result during the final request batch |
|---|---|
| [database-devops](https://github.com/topics/database-devops) | HTTP 429. Separate indexed searches supplied leads. |
| [database-governance](https://github.com/topics/database-governance) | HTTP 429. Separate indexed searches supplied leads. |
| [database-migration](https://github.com/topics/database-migration) | Accessible. Mostly engines, libraries, and database copy tools. |
| [schema-migration](https://github.com/topics/schema-migration) | Accessible. Mostly migration engines and frameworks. |
| [database-ci-cd](https://github.com/topics/database-ci-cd) | Accessible. No new qualifying Oracle platform established. |
| [database-change-management](https://github.com/topics/database-change-management) | Accessible. No new qualifying Oracle platform established. |

Topics and search indexes are incomplete discovery tools.
The review does not claim exhaustive repository coverage.

## Primary leads and disposition

| Lead | Primary source | Disposition |
|---|---|---|
| OceanBase ODC | [Backend repository](https://github.com/oceanbase/odc), [frontend repository](https://github.com/oceanbase/odc-client), [documentation repository](https://github.com/oceanbase/odc-doc) | Category A shortlist. Oracle source and batch deployment model inspected. |
| AccessFlow | [Repository](https://github.com/bablsoft/accessflow) | Category A shortlist with partial project/estate model. |
| SQLE / DMS | [SQLE](https://github.com/actiontech/sqle), [DMS](https://github.com/actiontech/dms), [Oracle plugin](https://github.com/actiontech/sqle-oracle-plugin) | Category B Community workflow. SQL version/batch release endpoints are Enterprise. |
| Archery / Yearning | [Archery](https://github.com/hhyo/Archery), [Yearning](https://github.com/cookieY/Yearning) | Category B. Oracle available in Archery. Release promotion not established. |
| Dokeeper | [Repository](https://github.com/mydakit/dokeeper) | Historical Bytebase derivative. Restricted enterprise source remains. |
| NineData Community | [Public repository](https://github.com/ninedata-cloud/ninedata-community) | Documentation and images alone do not establish OSS implementation rights. |
| WQMYH database-govern | [Repository](https://github.com/WQMYH/database-govern) | Renamed Bytebase fork with no fork-only default-branch commits in API comparison. |
| Early Bytebase forks | [hongweiyi](https://github.com/hongweiyi/bytebase), [nanzm](https://github.com/nanzm/bytebase) | Historical license and Oracle driver checks. No new qualifying product verified. |
| dbcm | [Repository](https://github.com/theophilusx/dbcm) | Category C terminal/PostgreSQL tool. Archived. No central Oracle platform. |
| iDB / Fleetdock discovery results | [iDB](https://www.idb.net/), [Fleetdock](https://fleetdock.dev/) | Server/database operations leads. Required Oracle release model not established. No shortlist entry. |

The final two leads received discovery screening only.
Their features and licenses did not receive a complete source audit.
Chinese searches included `Bytebase 开源 替代 数据库 变更 平台` and Gitee-oriented Apache/MIT fork terms.
The inaccessible Gitee mirror and API rate limits remain explicit in [the fork record](../../FORK-SEARCH.md).

## Freshness

AccessFlow's recorded source and release activity extend to October 2026.
SQLE and DMS snapshots contain August and September 2026 commits.
ODC's public backend main snapshot is dated June 2025. Its pinned frontend is dated May 2025.
A roadmap entry is not evidence that an implementation exists.
Published release text and source commits do not prove image contents or runtime readiness.
