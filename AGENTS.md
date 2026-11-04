# Agent guide

This repo holds hungovercoders' shared AI agent skills (`skills/<name>/SKILL.md`),
the guidance on where instructions belong, and the GitHub configuration that
backs them up. This file carries what most tasks need; `CLAUDE.md` is
`@AGENTS.md`. Open a routed doc only when its trigger in the Routes table fires.

## Ground rules

1. **This repo sets the standard, so it follows it.** Branches, commits and
   PRs here follow the `commit-and-pr` skill, PRs open as drafts, and CI is
   the `ci` job. A change that breaks a standard for us breaks it for everyone.
2. **Reuse the Taskfile.** Run `task --list` before writing any script or
   one-off command. Add a task only when nothing covers the need, and never
   invoke `scripts/*.py` directly; the task is the stable interface.
3. **Validate before committing.** `task check` runs the skill, context and
   JSON checks. Git hooks run it (`task setup` installs them); CI runs
   `task ci`, the single definition of green.
4. **No `task`?** Run `scripts/bootstrap.sh` once. Tool versions live only
   in `mise.toml`.
5. **Budgets are the feature.** When a check fails, move content deeper
   (into `docs/` or a skill's `references/`); never raise the budget.
6. **Tool-agnostic by default.** Skills and docs must work for Claude Code,
   Codex and Copilot. Name a tool-specific feature only where a skill needs
   it, and say which tool.
7. **Low debate first.** Prefer an existing convention (Conventional
   Commits, Linear's branch names, GitHub rulesets) to inventing one.

## Commands

| Command | Does |
|---|---|
| `task setup` | one-time: install the versioned git hooks |
| `task check` | `check:skills` + `check:context` + `check:json`, what hooks and CI run |
| `task new:skill NAME=my-skill` | scaffold `skills/my-skill/` |
| `task install:skills [GROUP=..] [SKILLS=..]` | symlink skills into `~/.claude`, `~/.codex`, `~/.copilot` |
| `task setup:github:org ORG=x [APPLY=1]` | property and rulesets from `github/`, dry run unless `APPLY=1` |
| `task setup:github:repo REPO=o/n [APPLY=1]` | repo settings and `ci-enabled`, dry run unless `APPLY=1` |
| `task ci` | everything GitHub Actions runs |

## Layout

```
AGENTS.md        this file (CLAUDE.md is @AGENTS.md)
CONTRIBUTING.md  the bar for changing a skill or proposing a standard
Taskfile.yml     every runnable script: `task --list`
mise.toml        pinned tool versions
skills/<name>/   SKILL.md + references/ scripts/ assets/
docs/            topic docs, routed from here and from docs/README.md
docs/decisions/  why each standard is the way it is
templates/       starting files for each instruction layer: managed, repo, user
github/          org property, rulesets, repo settings, applied by setup:github tasks
scripts/         python behind the tasks (stdlib only; run via task)
.githooks/       pre-commit -> task check, pre-push -> task ci
.github/         CI (`ci` job), PR and issue templates, CODEOWNERS, Dependabot
.claude/ .codex/ symlinks into skills/, plus the SessionStart bootstrap hook
.claude-plugin/  marketplace whose plugin root is this repo
```

## Skill conventions

- **Frontmatter**: `name` is lowercase-hyphenated and equals the directory.
  `description` (≤1024 chars) states the capability first, then explicit
  triggers ("Use when…"). It is the only triggering mechanism and loads in
  every conversation.
- **SKILL.md** ≤500 lines / ~5000 tokens, imperative voice, reasons over
  MUSTs. Draft first and act only when asked; a step the request clearly
  implies (pushing a commit you were asked to make) is fine if the reply says so.
- **Self-contained.** A skill is installed on its own into other repos and
  tools, so it can't link to `docs/` or `templates/`. What it needs at run
  time lives in its own `references/`, `scripts/` or `assets/`.
- **References are opt-in.** Every pointer to a bundled file states a
  condition ("open X when…"); `task check:skills` warns otherwise.
- **Catalog**: every skill sits in one family in `docs/catalog.md`, and
  names its neighbours under "When not to use".
- **Hand-offs, not overlaps.** One skill owns each artefact. A new skill
  that touches commits, PRs or CI hands off to the owner instead.

## Docs conventions

- **Content depth**: needed by most tasks → this file; by one kind of task
  → `docs/<topic>.md`; by one skill → its `references/`; by nobody → delete.
- **Every doc has an explicit route**: trigger, then "read", then the file.
  `task check:context` fails on a soft route or an unrouted doc.
- **Budgets**: README ≤60 lines, this file ≤150 lines / ~2000 tokens,
  `docs/README.md` ≤100, topic docs ≤300.

## Routes: read before you act

| When you are… | Do this |
|---|---|
| changing what a skill produces, or proposing a new skill or standard | Read [CONTRIBUTING.md](CONTRIBUTING.md) first: the bar, and when a decision record is needed |
| creating or editing a skill | Read [docs/skills.md](docs/skills.md) first: anatomy, cost, tool-agnostic writing |
| deciding where an instruction belongs, or editing `templates/` | Read [docs/instruction-layers.md](docs/instruction-layers.md) first |
| changing `github/`, CI, hooks, tasks or the check scripts | Read [docs/ci.md](docs/ci.md) before you change them |
| writing docs or deciding where content lives | Read [docs/docs-style.md](docs/docs-style.md) first |
| changing a standard, or asked why one exists | Read [docs/decisions/README.md](docs/decisions/README.md) first |
| doing any task not covered above | Read [docs/README.md](docs/README.md) before you start; do not guess a convention |
