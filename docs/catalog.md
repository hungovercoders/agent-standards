# Skill catalog

Three skills in two families. You don't run them by hand: an agent picks a
skill when your request matches its description, so ask for the outcome
("commit this", "open a draft PR", "check my agent setup"). To force one,
name it ("use the instructions-doctor skill"), or in Claude Code type
`/agent-standards:instructions-doctor`.

## Everyday work: `GROUP=work`

| Skill | Use when |
|---|---|
| `commit-and-pr` | creating a branch, committing, pushing, opening a PR, or marking a draft ready |

This one owns every branch, commit and PR. Other skills hand off to it
rather than writing their own.

## Setup and hygiene: `GROUP=setup`

| Skill | Use when |
|---|---|
| `repo-ci-setup` | a repo needs the standard `ci` job, or a PR waits forever on the `ci` check |
| `instructions-doctor` | checking that instructions sit in the right layer and don't compete with the shared skills |

Run `instructions-doctor` once after installing, and again whenever agents
behave inconsistently. Run `repo-ci-setup` once per repo.

## Install only what you use

Every installed skill's name and description load into every conversation,
whether or not it triggers. With three skills this barely matters; it will
as the catalog grows.

```bash
task install:skills GROUP=work          # one family
task install:skills SKILLS=commit-and-pr
```

The Claude Code plugin installs everything. To set it up, read
[install.md](install.md) when you're installing for the first time.

## Next candidates

Low-debate skills to add once these are in daily use: repo conventions
(writes a standard `AGENTS.md`), ticket refinement (Given/When/Then
acceptance criteria) and incident write-up (the existing postmortem
template). Before proposing one, read [CONTRIBUTING.md](../CONTRIBUTING.md).
