# Revised research review

**The existing platform shortlist contains OceanBase ODC and AccessFlow.**
ODC has Platform Fit HIGH and Migration Engine Fit LOW.
AccessFlow has Platform Fit MEDIUM and Migration Engine Fit LOW.
No complete replacement for all requested release and recovery capabilities was verified.
No application tests or Oracle tests ran.

Review date: 2026-10-03.

| Acceptance item | Review evidence | Result |
|---|---|---|
| Apply the new primary product constraint | Existing platforms precede SQL governance systems, engines, and proposed compositions | VERIFIED |
| Study Bytebase's operating model first | Public API/workflow documentation, resource definitions, actual frontend routes and project navigation | VERIFIED by source and official documentation |
| Classify every reviewed candidate | Category A/B/C register includes original candidates, new platforms, sampled forks, and commercial references | VERIFIED |
| Compare serious candidate product models | Ten separate tables contain all 18 requested capabilities | VERIFIED |
| Use independent fit scores | Two shortlist rows have separate Platform Fit and Migration Engine Fit scores | VERIFIED. No combined score |
| Retain strong platforms despite missing target state | ODC remains HIGH/LOW. AccessFlow remains MEDIUM/LOW | VERIFIED |
| Inspect actual shortlisted frontends | Backend-pinned ODC client, AccessFlow routes, navigation, and page components | VERIFIED by source review |
| Check all requested page types | Ten page checks per shortlisted platform | VERIFIED. Missing or partial pages remain explicit |
| Provide official visual evidence | Official project/batch screenshots and AccessFlow repository screenshots, with source URLs and local hashes | VERIFIED. Eleven image assets recorded, including two diagrams |
| Execute requested discovery searches | Twelve phrases, six topic requests, README text searches, Chinese/Gitee terms | VERIFIED for the documented search. Two topic requests returned HTTP 429 |
| Investigate recent and historical Bytebase forks | Seven repositories, local ancestry checks, historical API comparisons, and license files | VERIFIED for the sample. Exact fork creation commits remain UNKNOWN |
| Distinguish inherited history from independent development | Recent fork-only commit counts and historical divergence limits | VERIFIED. No unrestricted independent Oracle product established |
| Inspect new license and edition boundaries | ODC backend/client Apache-2.0. SQLE/DMS MPL-2.0. Community project/global inventory/version guards. Oracle plugin and NineData source gaps | VERIFIED for inspected files |
| Preserve original execution evidence | Twenty original Git HEADs and 103 source references | VERIFIED. Source hashes and line ranges match |
| Preserve supplemental source evidence | Eighteen Git snapshots in the supplemental register, including reused original snapshots. One selected-file Dokeeper snapshot | VERIFIED. Eighty source hashes and line ranges match |
| Preserve source working trees | Git status checks against original and supplemental manifests | VERIFIED. All registered source working trees are clean |
| Keep document links and tables valid | Relative destination checks and table column checks | VERIFIED |
| Preserve execution uncertainty | Twelve platform cases plus 33 original Oracle/governance cases | VERIFIED. All 45 original criteria remain. See the subsequent API/UI result report. |
| Integrate ODC deployment observations | ODC-EVALUATION.md and sanitized odc-runtime-20261003.json | VERIFIED by resource, file, and authenticated GET inspection. No Oracle SQL executed |
| Separate platform and target databases | Diagram and resource mapping distinguish OceanBase CE MetaDB from external Oracle targets | VERIFIED against deployment manifests |
| Correct ODC Git and CI claims | Repository registration controller and datasource/flow controllers | VERIFIED by source. Git and CI remain PARTIAL. Write operations remain NOT RUN |
| Explain inherited project permissions | Permission helper, service, API, and permission type enum | VERIFIED by source. Oracle cross-schema enforcement remains NOT RUN |
| Add ODC to desired-feature tables | Five feature groups now preserve twenty candidates and add ODC | VERIFIED. Twenty-one candidates |
| Preserve document generation | Six affected generators reproduce their current outputs | VERIFIED. Eleven outputs compared without application execution |
| Review independent ODC source findings | Antigravity, pinned claude-opus-5-5-medium, read-only source review | VERIFIED. Exit code 0, JSON SUCCESS, empty stderr |
| Keep composition secondary | Report selection, shortlist, and evaluation order use existing products first | VERIFIED |
| Review prose and claim scope | Sentence length, specific source limits, freshness, direct implementation versus roadmap | VERIFIED for reviewed prose |
| Review independent research execution | Pinned Gemini retry after exhausted Claude quota | VERIFIED. Exit code 0, JSON SUCCESS, empty stderr |
| Preserve unrelated files | Before-revision file hashes and source working-tree checks | VERIFIED. Changes concern research deliverables and document tools |

The [machine check record](evidence/product-model/document-checks.json) records the final document verification.
The [report diff](evidence/product-model/REPORT.diff) records the main change from the earlier report.
The archived baseline is [retained as text](evidence/product-model/REPORT-before-product-model.txt).
These document checks do not execute candidate applications, database statements, or application tests.
The [ODC review record](evidence/product-model/odc-integration-review.json) records this integration separately from the earlier fork research.
The [ODC report diff](evidence/product-model/REPORT-odc-integration.diff) uses the [pre-integration report](evidence/product-model/REPORT-before-odc-integration.txt).

## Remaining uncertainty

ODC's inspected public main source dates from June 2025. Its pinned frontend dates from May 2025.
Active 2026 public main maintenance was not established.
Its batch workflow is real. Immutable versioned releases, enforced environment prerequisites, and target applied detection remain incomplete or unverified.
Its embedded OceanBase Cloud Platform mode excludes Oracle in the frontend. Evaluate standalone ODC Web.

AccessFlow's schema promotion is real. Its project and estate model remains partial.
Its schema gate limits required DML and common PL/SQL forms.
Its central checksum does not establish Oracle target history or uncertain-result recovery.

Oracle script handling, compilation status, concurrent execution, retries, process crashes, and restore behavior remain runtime verification work.
ODC 4.4.1 is deployed. Readiness, 5/10 GiB volumes, selected authenticated GET routes, and Oracle plugin/driver packaging were inspected.
No Oracle target was connected. No performance measurement or production recovery experiment ran.
Other candidates retain their original source-only verification scope.
No proposed composition was implemented.

The fork sample is not exhaustive.
Exact creation commits and meaningful development in divergent historical forks remain unestablished.
The Gitee mirror was inaccessible. API and topic request limits restricted discovery.
The Dokeeper full clone exceeded available disk space. Selected commit-pinned raw files were retained instead.
NineData documentation does not establish an OSS implementation license.
The public SQLE Oracle plugin has unresolved complete license coverage.

## Deliverables

- [Revised report](REPORT.md)
- [ODC deployment, Bytebase mapping, Oracle onboarding, permissions, API, and license details](ODC-EVALUATION.md)
- [Product categories and capability comparisons](PRODUCT-MODEL.md)
- [Frontend and screenshot evidence](UI-EVIDENCE.md)
- [Historical and fork research](FORK-SEARCH.md)
- [Supplemental source evidence](PRODUCT-EVIDENCE.md)
- [Product-model search record](evidence/product-model/SEARCH.md)
- [License audit](LICENSE-AUDIT.md)
- [Maturity record](MATURITY.md)
- [Original desired-feature comparison](FEATURE-MATRIX.md)
- [Oracle coverage](ORACLE-COMPATIBILITY.md)
- [Platform and Oracle verification plan](poc/ORACLE-POC.md)

The original evidence and additional-candidate documents remain available.
The revised primary findings control platform selection.
