# Bytebase forks and historical search

**No independent, unrestricted Oracle platform was verified in the inspected fork sample.**
This result applies to seven sampled repositories. It does not describe every Bytebase fork.
Historical Apache source does not establish Oracle support or rights to included enterprise code.

Research date: 2026-10-03.

## Method

The review inspected recent forks, two early forks, a renamed fork, and the Dokeeper derivative lead.
It compared recent fork history locally against the recorded upstream branch.
It obtained API comparisons for historical and renamed forks.
It inspected each available root license and enterprise license.
The exact commit used when each fork was created remains UNKNOWN.
A common ancestor or current inherited commit is not necessarily that creation commit.

| Fork | Inspected HEAD | License | Verified upstream relationship | Independent development finding |
|---|---|---|---|---|
| `whatif-dev/db-tools-bytebase` | `80341df8627cefc5e6d1adae1eb50bf1e52d20e6` | MIT subset, enterprise and enablement restrictions | HEAD is a common ancestor of recorded upstream. 0 fork-only commits, 27 upstream-only commits. | Sampled default branch retains upstream history. |
| `camillanapoles/bytebase-Database-governance` | `924bf38b2db906f459cdbd5300c8f02728c3f202` | MIT subset, enterprise and enablement restrictions | HEAD is a common ancestor. 0 fork-only commits, 90 upstream-only commits. | Sampled default branch retains upstream history. |
| `FarendraAugust/fariskha-sqlite` | `2a8302b7af1adb15f705014d508650a49812de20` | MIT subset, enterprise and enablement restrictions | HEAD is a common ancestor. 0 fork-only commits, 16 upstream-only commits. | Repository name does not establish independent SQLite development. |
| `WQMYH/database-govern` | `a85f6cb4195299995e8554303550d672d5093e1d` | MIT subset, enterprise and enablement restrictions | API comparison finds 0 fork-only commits and 414 upstream-only commits. Merge base equals HEAD. | Renamed repository. No independent default-branch commits in this comparison. |
| `hongweiyi/bytebase` | `be87525c1228fe00cdcc3585859664bdd3167aca` | Apache-2.0 at sampled snapshot | API comparison finds 0 fork-only commits. Merge base equals HEAD. | Early 2021 snapshot. No implemented Oracle driver established. |
| `nanzm/bytebase` | `378a868ab1e8c8e2ad011f4b968e34decceb2436` | Apache-2.0 subset, proprietary enterprise directories | API reports divergence. Common ancestor: `6ee73cdc57bdcc6750013e14dc7fea428583d93a`. | March 2022 default-branch snapshot. Historical divergence alone does not establish an independent product. Oracle driver absent from inspected driver inventory. |
| `mydakit/dokeeper` | `40b22b38adb0ee506dba3f2d0dcc2cf2d6a71493` | MIT subset, proprietary enterprise directories | API reports divergence. Same historical common ancestor: `6ee73cdc57bdcc6750013e14dc7fea428583d93a`. | Copied Bytebase workflow and Oracle source paths exist. Meaningful independent feature development and unrestricted edition were not verified. |

The recent local comparisons used upstream commit `80524fc54601bcc5545575e02f83b23ee6bb0a70`.
Historical API comparisons record their full upstream response in the evidence directory.
Commit counts from divergent histories do not prove that every different commit is a new fork feature.
The Dokeeper HEAD message references Bytebase issue `#15813` and describes schema drift display.
Its README still describes Bytebase and links to Bytebase documentation.
These facts establish inherited identity. They do not establish complete equivalence or a new free product.

All sampled forks use Category A because their platform structure derives from Bytebase.
None enters the free Oracle shortlist solely through a repository rename or an Apache/MIT badge.
The current Bytebase root license also excludes feature, permission, role, and plan enablement code from its MIT grant.
The license text does not clearly assign a separate grant to that line.
The review therefore treats that code's unrestricted reuse rights as unestablished.
It proposes no license enforcement removal.

License references: [P-FORK-* and P-DOKEEPER-DOC](PRODUCT-EVIDENCE.md#source-references).
Machine records: [supplemental source manifest](evidence/product-model/source-manifest.json),
[oldest fork metadata](evidence/product-model/oldest-forks.json),
[Dokeeper repository metadata](evidence/product-model/dokeeper-repository.json),
and API comparison JSON files in `evidence/product-model/`.
The Dokeeper full clone failed because available disk space was insufficient.
Selected raw files and the commit-pinned source tree were retained instead.
No application tests ran.

## Chinese and Gitee ecosystem

The review searched Bytebase with Chinese database-change and SQL-audit terms.
It examined Archery, Yearning, SQLE/DMS, ODC, and NineData as distinct products.
ODC provides the strongest newly identified project estate and batch deployment model.
SQLE/DMS Community rejects project changes, global inventory, and version releases through explicit backend edition guards.
NineData's public Community repository contains deployment documentation, not inspectable platform code or an OSS license.

The Gitee Bytebase mirror page was inaccessible through the browser tool.
A mirror name does not establish an independent derivative or its license.
No independent Gitee derivative with verified Oracle release workflow was established.
This is an access limitation. It is not a finding that Gitee has no such project.

## Independent research execution

Antigravity performed a bounded recent-fork search from this research directory.
The initial pinned Claude run failed because Claude quota was exhausted.
The retry used pinned `gemini-3.1-pro-high`.
The retry returned exit code 0, JSON status `SUCCESS`, and empty stderr.
Codex repeated the local ancestry checks and added historical, renamed, and Dokeeper checks.
The Antigravity draft is retained as an intermediate record. This reviewed document controls the findings.

Records: [research task](evidence/product-model/fork-task.txt),
[draft](evidence/product-model/fork-search-draft.md),
[successful execution JSON](evidence/product-model/agy-fork-gemini.json),
and [quota response](evidence/product-model/agy-usage.json).
