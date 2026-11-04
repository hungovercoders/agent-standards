#!/usr/bin/env python3
"""Apply the GitHub configuration in github/ to an org or a repo, via `gh api`.

The skills assume GitHub is set up a certain way: a `ci-enabled` custom
property, a baseline ruleset on every repo, and a CI-required ruleset on
opted-in repos. Keeping that configuration as files and applying it with one
command means it is reviewed in a PR, repeatable, and never drifts from
what the docs describe.

Dry run by default: prints every call it would make. Pass --apply to make
them. Re-running is safe: the property is upserted and rulesets are matched
by name and updated in place rather than duplicated.

    org  hungovercoders          property definition + both org rulesets (org owner)
    repo <owner/name>   github/repo-settings.json + ci-enabled=true once `ci`
                        has passed on a merged pull request (repo admin)

Run via `task setup:github:org ORG=hungovercoders` / `task setup:github:repo REPO=...`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITHUB_DIR = REPO_ROOT / "github"


def gh(method: str, path: str, body: dict | None, apply: bool, soft: bool = False) -> object:
    """Call `gh api`; in dry-run mode, print the call and return None.
    GETs always run; with soft=True a failed GET returns None instead of exiting."""
    if not apply and method != "GET":
        print(f"  would {method} {path}")
        if body is not None:
            print("    " + json.dumps(body)[:160] + ("..." if len(json.dumps(body)) > 160 else ""))
        return None
    cmd = ["gh", "api", "--method", method, path]
    if body is not None:
        cmd += ["--input", "-"]
    try:
        result = subprocess.run(
            cmd, input=json.dumps(body) if body is not None else None,
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        if soft:
            print("  gh (the GitHub CLI) not found: can't list existing rulesets")
            return None
        sys.exit("gh (the GitHub CLI) is not installed - see https://cli.github.com")
    if result.returncode != 0:
        if soft:
            print(f"  could not {method} {path}: {result.stderr.strip()[:120]}")
            return None
        sys.exit(f"gh api {method} {path} failed:\n{result.stderr.strip()}")
    print(f"  {method} {path}: ok")
    out = result.stdout.strip()
    if not out:
        return None
    return json.loads(out)


def load(rel: str) -> dict:
    return json.loads((GITHUB_DIR / rel).read_text(encoding="utf-8"))


def setup_org(org: str, apply: bool) -> None:
    print(f"Org {org}: custom properties")
    for prop in sorted((GITHUB_DIR / "properties").glob("*.json")):
        gh("PUT", f"orgs/{org}/properties/schema/{prop.stem}", load(f"properties/{prop.name}"), apply)

    print(f"Org {org}: rulesets")
    existing = gh("GET", f"orgs/{org}/rulesets?per_page=100", None, True, soft=not apply) or []
    by_name = {r["name"]: r["id"] for r in existing if isinstance(r, dict)}
    if not existing and not apply:
        print("  (an existing ruleset with the same name is updated instead of created)")
    for path in sorted((GITHUB_DIR / "rulesets").glob("*.json")):
        ruleset = load(f"rulesets/{path.name}")
        if ruleset["name"] in by_name:
            gh("PUT", f"orgs/{org}/rulesets/{by_name[ruleset['name']]}", ruleset, apply)
        else:
            gh("POST", f"orgs/{org}/rulesets", ruleset, apply)


def ci_passed(repo: str, apply: bool) -> bool | None:
    """Whether a check named `ci` succeeded on the head of a pull request
    merged into the default branch. A success on the default branch alone
    would also accept a push-only workflow, and a PR into another branch
    could run a workflow that never fires on the branch the ruleset
    protects; either leaves every PR waiting forever once the check is
    required. None when it can't be told (dry run without access)."""
    info = gh("GET", f"repos/{repo}", None, True, soft=not apply)
    if not isinstance(info, dict):
        return None
    branch = info.get("default_branch", "main")
    prs = gh(
        "GET",
        f"repos/{repo}/pulls?state=closed&base={branch}&sort=updated&direction=desc&per_page=20",
        None, True, soft=not apply,
    )
    if not isinstance(prs, list):
        return None
    for pr in prs:
        if not (isinstance(pr, dict) and pr.get("merged_at")):
            continue
        sha = pr.get("head", {}).get("sha")
        runs = gh("GET", f"repos/{repo}/commits/{sha}/check-runs?check_name=ci", None, True, soft=not apply)
        if isinstance(runs, dict) and any(
            r.get("conclusion") == "success" for r in runs.get("check_runs", [])
        ):
            return True
    return False


def setup_repo(repo: str, apply: bool) -> None:
    print(f"Repo {repo}: settings")
    gh("PATCH", f"repos/{repo}", load("repo-settings.json"), apply)
    print(f"Repo {repo}: opt into the CI-required ruleset")
    # Opting in before `ci` reports blocks every PR in the repo: the required
    # check would wait forever. Same rule the repo-ci-setup skill follows.
    passed = ci_passed(repo, apply)
    if passed is False:
        sys.exit(
            f"  no PR merged into {repo}'s default branch has a successful `ci` check: "
            "not setting ci-enabled. Merge a PR on which the `ci` job ran, then re-run."
        )
    if passed is None:
        print("  (couldn't confirm `ci` has passed; the real run checks before setting it)")
    gh(
        "PATCH", f"repos/{repo}/properties/values",
        {"properties": [{"property_name": "ci-enabled", "value": "true"}]}, apply,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="target", required=True)
    org = sub.add_parser("org")
    org.add_argument("org")
    repo = sub.add_parser("repo")
    repo.add_argument("repo", help="owner/name")
    for p in (org, repo):
        p.add_argument("--apply", action="store_true", help="make the calls (default: dry run)")
    args = parser.parse_args()

    if not args.apply:
        print("Dry run: nothing will change. Re-run with APPLY=1 to apply.\n")
    if args.target == "org":
        setup_org(args.org, args.apply)
    else:
        setup_repo(args.repo, args.apply)
    if not args.apply:
        print("\nDry run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
