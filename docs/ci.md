# CI, hooks, tasks and GitHub setup

One principle: **`task ci` is the single definition of "the checks pass."**
Git hooks and GitHub Actions are both thin wrappers around the Taskfile, so
local and remote can't disagree.

```
.githooks/pre-commit ─→ task pre-commit ─→ task check
.githooks/pre-push   ─→ task pre-push   ─→ task ci ─→ task check
.github/workflows/ci.yml ──────────────────→ task ci
```

The workflow's job is named `ci` and runs on draft PRs, the same standard
`repo-ci-setup` gives every other repo. Renaming the job breaks the org
ruleset, which requires a check with that exact name.

## The checks

- `task check:skills` (`scripts/check_skills.py`): frontmatter, name matches
  directory, description states capability then triggers, SKILL.md under
  500 lines, referenced files exist, no orphaned bundled files, every skill
  in one `docs/catalog.md` family, and a warning for files loaded on every
  use.
- `task check:context` (`scripts/check_context.py`): line and token budgets
  on README, AGENTS.md, `docs/README.md` and topic docs; `CLAUDE.md` is
  exactly `@AGENTS.md`; every doc has an explicit route from AGENTS.md,
  `docs/README.md` or `docs/decisions/README.md`; relative links resolve.
- `task check:json` (`scripts/check_json.py`): every JSON file parses, so a
  broken ruleset or settings template fails here rather than in an
  admin's terminal.

`check_skills.py`, `check_context.py`, `catalog.py`, `install_skills.py`,
`new_skill.py` and `bootstrap.sh` come from
[dataGriff/skills](https://github.com/dataGriff/skills). Local changes
to keep when re-syncing: `check_context.py` treats
`docs/decisions/README.md` as a routing file; `new_skill.py` tells you to
add the skill to a catalog family; `install_skills.py` names this repo's
families in its help text; `install_skills.py` re-points dangling links
left by a moved clone. Budgets are constants
at the top of each script; change one deliberately, with a reason in the
commit.

## Tasks

`Taskfile.yml` is the single home for everything runnable. Run
`task --list` first and reuse what exists. To add a task:

1. Give it a `desc:` written for someone who's never seen it.
2. Name it `namespace:action` (`check:json`, `setup:github:org`).
3. Put non-trivial logic in a stdlib-only Python script under `scripts/`.
4. If CI should run it, add it to the `ci` chain, never to the workflow.

## GitHub setup

`github/` holds the configuration the skills depend on:

| File | Applied by | Holds |
|---|---|---|
| `github/properties/ci-enabled.json` | `task setup:github:org` | The opt-in property for the CI ruleset |
| `github/rulesets/*.json` | `task setup:github:org` | Baseline (all repos) and CI required (opted-in repos) |
| `github/repo-settings.json` | `task setup:github:repo` | Delete head branches on merge, allow updating from base; the task also sets `ci-enabled`, but only once `ci` has passed on a merged PR |

Both tasks dry-run unless `APPLY=1`, and are safe to re-run. Change the
files through a PR and re-apply. Never edit rulesets in the GitHub UI:
the next apply overwrites the change, and the files stop matching reality.

`.github/` holds this repo's own PR template (the same sections
`commit-and-pr` writes), CODEOWNERS, and Dependabot for GitHub Actions
versions, with `ci:` commit prefixes.

## Hooks

Versioned in `.githooks/`, activated by `task setup`. They hard-fail when
`task` is missing rather than silently skipping checks. In an emergency,
`git commit --no-verify` bypasses them, and CI still catches the problem.
