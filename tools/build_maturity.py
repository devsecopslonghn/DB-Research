"""Summarize captured repository metadata without filling missing values."""
import datetime
import json
import pathlib
import statistics
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
sources = json.loads((ROOT / "evidence/source-manifest.json").read_text())
out = ["# Maturity assessment", "", "Research date: 2026-10-03.", "",
       "The numbers below come from captured GitHub responses and repository pages.",
       "They describe repository activity. They do not establish production readiness.",
       "Contributor counts include service accounts and anonymous entries returned by GitHub.",
       "A count of at least 100 means that the first page was full and the total was not verified.",
       "Issue counts exclude pull requests when the captured HTML provides a separate count.",
       "Repository creation dates are not first-release dates.", "",
       "## Release and activity register", "",
       "| Repository | Created | First release | Latest stable release | Recent release interval | Latest inspected commit | Stars | Forks | Contributors | Open issues |",
       "|---|---|---|---|---|---|---|---|---|---|"]

for key, source in sorted(sources.items()):
    api = ROOT / "evidence/api" / key
    def read(name, default):
        file = api / (name + ".json")
        return json.loads(file.read_text()) if file.exists() else default
    repository = read("repository", {})
    releases = read("releases", [])
    stable = [r for r in releases if not r["prerelease"] and not r["draft"] and "nightly" not in r["tag_name"].lower()]
    stable.sort(key=lambda r: r["published_at"], reverse=True)
    latest = (f"[{stable[0]['tag_name']}]({stable[0]['html_url']}) {stable[0]['published_at'][:10]}" if stable else "UNKNOWN")
    first = "UNKNOWN"
    if stable and len(releases) < 100:
        first = f"{stable[-1]['tag_name']} {stable[-1]['published_at'][:10]}"
    if key == "liquibase__liquibase__v4.33.0":
        latest = "Pinned v4.33.0. Current upstream releases appear in the main row."
        first = "Same upstream history"
    recent = stable[:8]
    dates = [datetime.datetime.fromisoformat(r["published_at"].replace("Z", "+00:00")) for r in recent]
    intervals = [(a - b).total_seconds() / 86400 for a, b in zip(dates, dates[1:])]
    cadence = f"{statistics.median(intervals):.1f} days, median of {len(intervals)} intervals" if intervals else "UNKNOWN"
    contributors = read("contributors", None)
    contributor_count = "UNKNOWN" if contributors is None else (("at least " if len(contributors) == 100 else "") + str(len(contributors)))
    counts = read("page-counts", {})
    commit_time = subprocess.check_output(["git", "-C", str(ROOT / source["directory"]), "show", "-s", "--format=%cI", "HEAD"], text=True).strip()[:10]
    commit = f"[{commit_time}](https://github.com/{source['repo']}/commit/{source['sha']})"
    evidence_link = f"[metadata](evidence/api/{key}/)" if api.exists() else f"[source]({source['directory']}/)"
    out.append(f"| [{source['repo']}](https://github.com/{source['repo']}) {evidence_link} | {repository.get('created_at', 'UNKNOWN')[:10]} | {first} | {latest} | {cadence} | {commit} | {repository.get('stargazers_count', 'UNKNOWN')} | {repository.get('forks_count', 'UNKNOWN')} | {contributor_count} | {counts.get('open_issues', 'UNKNOWN')} |")

out += ["", "The first-release column uses the earliest stable GitHub release only when the captured page is complete.",
        "It may not include releases published before the project used GitHub releases.",
        "A full page leaves the first release UNKNOWN. API limits prevented further pagination.",
        "Release frequency uses up to eight recent stable releases. It is not a service-level commitment.",
        "Flyway Play and Flyway UI may publish artifacts without creating GitHub releases.",
        "DRM package.json declares 1.2.1, while the recorded GitHub release is Release1.2.0.",
        "Liquibase main README lists an older release than the captured release API.", "",
        "## Deployment, documentation, and security", "",
        "YES means an asset or procedure was found. It does not mean that it was run.",
        "No candidate received an image vulnerability scan or an independent security audit.", "",
        "| Project | Docker image or build | Documentation assessment | Security policy or process | Production-use evidence | Maintenance assessment |",
        "|---|---|---|---|---|---|"]
rows = [
    ("Bytebase", "YES. Official image and deployment docs.", "Extensive. Edition boundaries need care.", "UNKNOWN for a dedicated policy in this snapshot. Vendor security process requires follow-up.", "Official case studies exist. Oracle recovery at the required scale remains UNKNOWN.", "Recent commits and releases. Established project."),
    ("AccessFlow", "YES. Compose images and Helm chart.", "Extensive source design, identity, CI, and recovery docs.", "Security architecture docs. Dedicated vulnerability-reporting policy UNKNOWN.", "Demo deployment documented. Independent large Oracle production use UNKNOWN.", "Recent commits and frequent releases. Small contributor base."),
    ("DRM", "UNKNOWN for a published container. npm and Python installation documented.", "README, wiki, and examples. Actual execution needs source review.", "Dedicated security policy UNKNOWN.", "Vendor deployment claims. Independent evidence UNKNOWN.", "Small project. Package version differs from release tag."),
    ("Open Migration", "YES. Dockerfile and Compose. Registry availability UNKNOWN.", "README and UI examples. Recovery and security operations are limited.", "Dedicated security policy UNKNOWN.", "UNKNOWN.", "Small repository. No recorded release. Last inspected commit is older than current date."),
    ("SchemaPilot", "UNKNOWN for a published image.", "Readme, deployment, and security notes. Limited operational evidence.", "Dedicated reporting process UNKNOWN.", "UNKNOWN.", "Small repository. Last activity in 2025 in captured metadata."),
    ("Flyway UI", "NO documented standalone image in the inspected project.", "Minimal README and embedded example.", "Dedicated policy UNKNOWN. Old dependencies require separate review.", "UNKNOWN.", "Legacy servlet component. No current product evidence."),
    ("Flyway Play", "NO dedicated control-plane image. Application packaging is external.", "Useful module setup and compatibility table.", "Dedicated policy UNKNOWN.", "Module adoption does not prove a central estate service.", "Recent repository work. Old default Flyway dependency remains."),
    ("Flyway", "YES. Official CLI image.", "Extensive official docs. Tier boundaries are explicit.", "Vendor security process UNKNOWN in this review. Do not infer no CVEs.", "Broad engine adoption. Proposed central composition remains unverified.", "Frequent releases and current commits."),
    ("Liquibase main / 4.33", "YES. Official images. License and bundled components depend on version.", "Extensive versioned docs. Current license differs from 4.33.", "YES. SECURITY.md gives a reporting channel. Version support needs separate confirmation.", "Broad engine adoption. No tested Oracle control-plane composition here.", "Current main active. Future maintenance for Apache-only 4.33 is UNKNOWN."),
    ("Sqitch", "YES. Official image project linked from its README.", "Extensive command and engine documentation.", "Dedicated reporting policy UNKNOWN.", "Adoption claims and history. Required enterprise scale UNKNOWN.", "Current commits. Less frequent releases than Flyway."),
    ("Atlas", "YES. Official distribution and Docker documentation.", "Extensive official docs. Oracle Pro boundary is explicit.", "Dedicated reporting process UNKNOWN.", "Vendor adoption claims. No free Oracle product established.", "Current commits and releases."),
    ("Yearning", "YES. Dockerfile and Compose. Current image digest unverified.", "README and product docs, primarily SQL audit use.", "Dedicated reporting process UNKNOWN.", "Deployment examples. Oracle deployment evidence absent from supported scope.", "Inspected HEAD is from March 2025. Latest recorded stable release remains from 2024."),
    ("Archery", "YES. Compose and deployment scripts.", "Detailed Chinese docs and implementation notes.", "Contribution and issue process. Dedicated private disclosure process UNKNOWN.", "Established SQL workflow project. Tested Oracle migration-ledger use UNKNOWN.", "Recent commits. Releases remain active."),
    ("Tareya derivative", "YES. Inherited Docker deployment files.", "Mostly inherited docs.", "Dedicated process UNKNOWN.", "UNKNOWN.", "Independent support and release cadence UNKNOWN."),
    (".NET dbdeploy", "UNKNOWN for a published image.", "README, CLI docs, and dialect implementation.", "Dedicated process UNKNOWN.", "UNKNOWN.", "Inspected current source. Release and support statistics incomplete."),
    ("DbMaintain", "YES. Repository Docker build docs.", "Detailed legacy engine docs.", "Current security maintenance UNKNOWN.", "Historical adoption does not establish current support.", "Maintainer explicitly states deprecated and unmaintained."),
    ("dbpm", "UNKNOWN for a published image. Python CLI deployment.", "Detailed Oracle package, lockfile, and recovery docs.", "YES. SECURITY.md exists. Response effectiveness unverified.", "Author documents live artifact tests. Independent production evidence UNKNOWN.", "Changelog records 1.5.3 on 2026-09-10. Young project."),
    ("dbward", "YES. Quickstart Compose and binary releases documented.", "Useful architecture and license boundary docs.", "Dedicated reporting process UNKNOWN.", "UNKNOWN.", "Young open-core project. Current source inspected."),
    ("CloudBeaver", "YES. Community Docker deployment documented.", "Extensive database and server docs.", "Independent CVE and disclosure review remains UNKNOWN.", "Established web editor. Required release workflow evidence absent.", "Current source inspected. Supplemental release statistics unavailable."),
]
for row in rows:
    out.append("| " + " | ".join(row) + " |")
out += ["", "Evidence locations: [source register](EVIDENCE.md), captured API pages, repository deployment files, and source documentation.",
        "Security-policy file presence is evidence of a reporting route, not proof of a secure product.",
        "A repository without SECURITY.md can still have a vendor reporting route. Such a route remains UNKNOWN here.",
        "Production-use claims are attributed to project owners. This research did not independently verify them.",
        "No result should use GitHub stars as a substitute for Oracle failure and recovery evidence.", ""]
# Preserve the separately maintained product-model source and deployment assessment.
existing = ROOT / "MATURITY.md"
heading = "## Product-model search additions"
if existing.exists() and heading in existing.read_text():
    out += [heading + existing.read_text().split(heading, 1)[1]]
(ROOT / "MATURITY.md").write_text("\n".join(out))
print("Built MATURITY.md from captured metadata.")
