"""Locate the existing release/commit handoff; no deployment sequencing or SQL execution."""
import argparse
import json
import os
import re
import urllib.error
import urllib.request

from .common import DemoError, ROOT, fail_cli, git, release_path


def find_handoff_run(release_id, commit):
    release_path(release_id)
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if repository != "devsecopslonghn/DB-Research" or not token or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise DemoError("GitHub handoff lookup requires the approved repository, token and exact source commit")
    name = f"odc-handoff-{release_id}-{commit}"
    for page in range(1, 21):
        request = urllib.request.Request(f"https://api.github.com/repos/{repository}/actions/artifacts?per_page=100&page={page}",
                                         headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
                                                  "X-GitHub-Api-Version": "2022-11-28"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
        except (urllib.error.URLError, ValueError):
            raise DemoError("GitHub handoff artifact lookup failed") from None
        artifacts = data.get("artifacts", [])
        for artifact in artifacts:
            run = artifact.get("workflow_run") or {}
            if artifact.get("name") == name and not artifact.get("expired") and run.get("head_sha") == commit:
                return {"name": name, "run_id": run["id"]}
        if len(artifacts) < 100:
            break
    raise DemoError("No retained ODC handoff exists for this release/commit; do not create or guess a replacement ticket")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-id", required=True)
    args = parser.parse_args()
    try:
        value = find_handoff_run(args.release_id, git(ROOT, "rev-parse", "HEAD").decode().strip())
        output = os.environ.get("GITHUB_OUTPUT")
        if output:
            with open(output, "a") as stream:
                stream.write(f"name={value['name']}\nrun_id={value['run_id']}\n")
        print(json.dumps(value))
    except DemoError as exc:
        fail_cli(exc)


if __name__ == "__main__":
    main()
