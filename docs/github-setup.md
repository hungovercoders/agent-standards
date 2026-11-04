# GitHub org setup

Two org rulesets, one custom property and the shared skills make every
repo merge through a passing `ci` check, without blocking repos that have
no CI. Everything GitHub needs is in `github/` and applied by a task, so
the setup is reviewed, repeatable and matches these docs.

## Requirements

- GitHub Team or Enterprise plan: org rulesets are a Team feature
  ([changelog](https://github.blog/changelog/2025-06-16-organization-rulesets-now-available-for-github-team-plans/)).
- An org owner with `gh` authenticated with org admin scope
  (`gh auth refresh -s admin:org`).
- Linear's GitHub integration, with **Link commits to issues with magic
  words** on ([Linear docs](https://linear.app/docs/github)).
- This repo readable by every engineer, with `.github/CODEOWNERS` naming
  the team that owns the standards.

## Org: property and rulesets

An org owner runs, from this repo:

```bash
task setup:github:org ORG=hungovercoders            # dry run: prints every call
task setup:github:org ORG=hungovercoders APPLY=1    # applies github/properties and github/rulesets
```

| What it creates | Effect |
|---|---|
| `ci-enabled` property (true/false, unset by default, repo admins may set it) | None until a repo sets it |
| **Baseline** ruleset, all repos: PR required, no force pushes, no deleting the default branch | Only while its `enforcement` is `active` |
| **CI required** ruleset, repos with `ci-enabled = true`: the `ci` check must pass | Only on repos that have opted in |

The baseline's `enforcement` field in
`github/rulesets/baseline-default-branch.json` is the switch: `disabled`
means announced but not enforced, `active` means enforced. It changes
through a PR, then a re-run of the task. Required approvals are 0 because
review happens on the draft. Both rulesets let org admins bypass, for CI
outages; a bypass is noted on the PR.

The task is safe to re-run: the property is upserted, and rulesets are
matched by name and updated in place.

## Repo: settings and opt-in

A repo admin runs, once the repo's `ci` job has passed on a merged pull
request:

```bash
task setup:github:repo REPO=hungovercoders/<repo> APPLY=1
```

It deletes head branches on merge, lets PR authors update from base, and
sets `ci-enabled`. The task refuses to set the property until a merged PR
shows a passing `ci` check: a pass on the default branch alone could come
from a push-only workflow, and a required check that never reports on PRs
blocks every one of them. The `repo-ci-setup` skill walks an agent through the same steps,
including adding the `ci` job.

Opted-in repos are a query on the property:

```bash
gh api --paginate orgs/hungovercoders/properties/values \
  --jq '.[] | select(any(.properties[]; .property_name == "ci-enabled" and .value == "true")) | .repository_name'
```

## Everyone: the skills

Engineers install the skills by reading [install.md](install.md). For the
whole org at once, an admin deploys
`templates/managed/managed-settings.json` (enables the plugin) and
`templates/managed/CLAUDE.md.tmpl` (says the shared skills take
precedence) with MDM or similar. The managed file is guidance; the
rulesets are the enforcement.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| PR stuck on "Expected - Waiting for status to be reported" | No job named exactly `ci`, a matrix renamed it, a `paths` filter skipped the workflow, or it didn't trigger | Run `repo-ci-setup`; if the repo isn't ready, set `ci-enabled` back to false |
| `ci` doesn't run on drafts | The workflow skips drafts, or its `pull_request` types are incomplete | Use types `opened, synchronize, reopened, ready_for_review` and no draft condition |
| Skill won't mark a draft ready | `ci` failing, running or missing | Fix and push, or wait with `gh pr checks --watch` |
| `setup:github:repo` returns 403 | Not a repo admin | Ask an org owner |
| CI outage blocks every merge | The required check can't report | An org admin bypasses and notes it on the PR |
| Linear issue doesn't link or move | Magic-words toggle off, or no issue ID in the branch | Turn on the toggle; use Linear's copied branch name |
| Agents still format commits differently | A competing personal or repo instruction | Run `instructions-doctor` |
