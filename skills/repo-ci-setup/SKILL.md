---
name: repo-ci-setup
description: >-
  Brings a repository up to the org CI standard: adds or adapts a GitHub
  Actions job named exactly `ci` that runs on draft PRs, proves it passes on a
  draft PR, then opts the repo into the org's CI-required ruleset by setting
  its `ci-enabled` custom property. Use when setting up CI for a repo, onboarding
  a repo to the standard, or when a PR shows the required `ci` check as
  "Expected - Waiting for status to be reported".
---

# Repo CI setup

Brings a repository up to the org standard so it can join the "CI required" ruleset.

## How the standard works

- The org has two rulesets on every repo's default branch:
  - **Baseline** (all repos): changes go through a PR, no force pushes, the default branch can't be deleted.
  - **CI required** (opted-in repos only): the `ci` check must pass before a PR can merge.
- A repo joins "CI required" when its custom property `ci-enabled` is set to `true`.
- The check is matched by name. The repo needs a GitHub Actions job named exactly `ci`. If it doesn't exist, PRs wait forever and can't merge. That's why the property is only set **after** CI is proven to work.

## Steps

### 1. Check where the repo stands

- Read the current property: `gh api repos/{owner}/{repo}/properties/values`. If `ci-enabled` is already `true`, check that a check named exactly `ci` reported on a recent PR (`gh pr checks <number>` on an open or recently merged one). If it did, say the repo is already set up and stop. If it didn't, the job is misnamed, matrixed or skips drafts, and every PR is waiting on it: carry on, and step 3 fixes the workflow.
- List `.github/workflows/`. Note any existing CI and what its jobs are called.
- Find the default branch: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.

### 2. Work out the build commands

Detect the stack from the files in the repo root and read the commands the repo already uses. Do not invent commands.

| File | Look at |
|------|---------|
| `package.json` | `scripts` (install with `npm ci`, `pnpm install --frozen-lockfile` or `yarn install --immutable` to match the lockfile) |
| `pyproject.toml` / `requirements*.txt` | test runner config, `uv`/`poetry` lockfiles |
| `*.sln` / `*.csproj` | `dotnet restore`, `dotnet build`, `dotnet test` |
| `go.mod` | `go build ./...`, `go test ./...` |
| `Makefile` / `justfile` | existing `test`, `lint`, `build` targets — prefer these |
| `README.md` | how the team says to build and test |

If the commands aren't clear, ask the user. Show them the install, lint, test and build commands you plan to use before writing the workflow.

### 3. Add the workflow

Follow the commit-and-pr skill: a Linear issue and Linear's branch name are needed first.

**No existing CI:** when the repo has no workflow yet, copy `assets/ci.yml` to `.github/workflows/ci.yml`. Fill in the toolchain setup and the commands from step 2. Set the `push` branch to the default branch. Use the current major version of each action.

**One definition of green:** if the repo already has a single entry point for its checks (a Taskfile `ci` task, a `make ci` target, an npm `ci` script), make the `ci` job run that one command instead of listing steps. Local runs, hooks and CI then can't disagree about what passing means.

**Existing CI with several jobs:** don't rewrite it. Add a fan-in job named `ci` to the existing workflow so the check name matches:

```yaml
  ci:
    name: ci
    needs: [lint, test, build] # the existing job ids
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: All required jobs passed
        # 'skipped' counts as a failure: a needed job that was skipped by its own `if:` never ran.
        if: contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') || contains(needs.*.result, 'skipped')
        run: exit 1
      - run: echo "All required jobs passed"
```

Then check the existing workflow's triggers match the standard:
- `pull_request` with types `opened, synchronize, reopened, ready_for_review`
- No job condition that skips draft PRs (e.g. `if: github.event.pull_request.draft == false`). Drafts must run CI.
- A `concurrency` block with `cancel-in-progress` for pull requests.

Explain any trigger changes to the user before making them.

**Rules for the `ci` job either way**
- Name it exactly `ci`, with `name: ci`.
- No `strategy.matrix` on it. A matrix renames the check (e.g. `ci (20.x)`) and the ruleset won't find it. Put matrices on other jobs and fan in.

### 4. Prove it works

1. Show the user the commit and draft PR you'd create, following the commit-and-pr skill with type `ci`, e.g. `ci: add standard ci workflow`.
2. Once they confirm, commit, push and open the draft PR.
3. Watch the run: `gh pr checks --watch`.
4. Confirm a check named exactly `ci` appears and passes. If it fails, fix it and push again. If it doesn't appear at all, the triggers or job name are wrong.

Do not continue until `ci` has passed on the PR.

### 5. Opt the repo in

Only after the PR is merged, so the workflow is on the default branch. Tell the user this switches on the merge block, and set the property when they confirm:

```bash
gh api --method PATCH repos/{owner}/{repo}/properties/values --input - <<'EOF'
{ "properties": [ { "property_name": "ci-enabled", "value": "true" } ] }
EOF
```

This needs repo admin access, or the "edit custom property values" permission. If the call returns 403 or 404, don't retry. Tell the user to ask an org owner to set `ci-enabled` to `true` for this repo.

### 6. Confirm

- `gh api repos/{owner}/{repo}/rules/branches/{default-branch}` should now list a `required_status_checks` rule containing `ci`.
- Tell the user the repo is in, and that every PR now needs `ci` green before merging.

## Don'ts

- Don't set `ci-enabled` before `ci` has passed on a PR. It blocks every PR in the repo.
- Don't edit org rulesets. Those are owned centrally.
- Don't disable or delete existing checks to make `ci` pass.

## When not to use

- Committing, pushing or opening the PR that adds the workflow: follow `commit-and-pr` for those steps.
- Editing the org rulesets themselves: those are owned centrally, through the agent-standards repo.
