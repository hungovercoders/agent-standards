# Rolling out to a GitHub org

Two org rulesets, one custom property and the shared skills make every repo
merge through a passing `ci` check, without blocking repos that don't have
CI yet. Everything GitHub needs is in `github/` and applied by a task, so
the setup is reviewed, repeatable and matches these docs.

## Prerequisites

- [ ] GitHub Team or Enterprise plan. Org rulesets have been on Team since
      June 2025 ([changelog](https://github.blog/changelog/2025-06-16-organization-rulesets-now-available-for-github-team-plans/)).
- [ ] An org owner with `gh` authenticated with org admin scope
      (`gh auth refresh -s admin:org`).
- [ ] Linear's GitHub integration installed, with **Link commits to issues
      with magic words** turned on ([Linear docs](https://linear.app/docs/github)).
- [ ] This repo pushed to `hungovercoders/agent-standards`, readable by every engineer.
- [ ] `.github/CODEOWNERS` pointing at the team that owns the standards.

## Phase 1: GitHub org setup

An org owner runs, from this repo:

```bash
task setup:github:org ORG=hungovercoders            # dry run: prints every call
task setup:github:org ORG=hungovercoders APPLY=1    # applies github/properties and github/rulesets
```

| What it creates | Effect on day one |
|---|---|
| `ci-enabled` property (true/false, unset by default, repo admins may set it) | None until a repo sets it |
| **Baseline** ruleset, all repos: PR required, no force pushes, no deleting the default branch | None: it ships **disabled** |
| **CI required** ruleset, repos with `ci-enabled = true`: the `ci` check must pass | None: no repo has opted in |

The baseline starts disabled so it can be announced first. To switch it on,
change `"enforcement"` to `"active"` in
`github/rulesets/baseline-default-branch.json` through a PR, then re-run the
task. Required approvals are 0 because review happens on the draft; raise
it later if the team agrees. Both rulesets let org admins bypass, for
CI outages; note any use on the PR.

The task is safe to re-run: the property is upserted, and rulesets are
matched by name and updated in place.

## Phase 2: This repo first

This repo follows its own standard, so it's the first to opt in:

1. Merge a PR here so the `ci` job has run on the default branch.
2. `task setup:github:repo REPO=hungovercoders/agent-standards APPLY=1` deletes head
   branches on merge, lets PR authors update from base, and sets
   `ci-enabled`.

## Phase 3: Publish the skills

Engineers install them by reading [install.md](install.md) and following
it. For the whole org at once, an admin deploys
`templates/managed/managed-settings.json` (enables the plugin) and
`templates/managed/CLAUDE.md.tmpl` (says the shared skills take precedence) with
MDM or similar. The managed file is guidance, not enforcement; the rulesets
are the enforcement.

## Phase 4: Pilot

Two repos for a week: one with CI, one without, so both paths through
`repo-ci-setup` get tested.

1. Run `instructions-doctor` for each pilot engineer and in each repo; fix
   the conflicts it finds.
2. Ask the agent to set up CI for each repo (`repo-ci-setup`).
3. Take one real Linear issue end to end with `commit-and-pr`.

Done when:

- [ ] `ci` runs on every push to a draft PR
- [ ] the skill refuses to mark a draft ready while `ci` fails
- [ ] GitHub blocks the merge while `ci` fails
- [ ] the Linear issue moves to Done when a `Fixes` PR merges
- [ ] the pilot teams would keep using it

## Phase 5: Roll out

1. Announce the baseline date, then activate it (Phase 1).
2. Each engineer runs `instructions-doctor` once and removes process rules
   from their personal files.
3. Each team runs `repo-ci-setup` on its repos. A repo joins the CI ruleset
   only after its `ci` job has passed on a PR.
4. Track progress:

```bash
gh api --paginate orgs/hungovercoders/properties/values \
  --jq '.[] | select(any(.properties[]; .property_name == "ci-enabled" and .value == "true")) | .repository_name'
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| PR stuck on "Expected - Waiting for status to be reported" | No job named exactly `ci`, a matrix renamed it, or it didn't trigger | Run `repo-ci-setup`; if the repo isn't ready, set `ci-enabled` back to false |
| `ci` doesn't run on drafts | The workflow skips drafts, or its `pull_request` types are incomplete | Use types `opened, synchronize, reopened, ready_for_review` and no draft condition |
| Skill won't mark a draft ready | `ci` failing, running or missing | Fix and push, or wait with `gh pr checks --watch` |
| `setup:github:repo` returns 403 | Not a repo admin | Ask an org owner |
| CI outage blocks every merge | The required check can't report | An org admin bypasses and notes it on the PR |
| Linear issue doesn't link or move | Magic-words toggle off, or no issue ID in the branch | Turn on the toggle; use Linear's copied branch name |
| Agents still format commits differently | A competing personal or repo instruction | Run `instructions-doctor` |
