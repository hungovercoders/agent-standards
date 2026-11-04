---
name: instructions-doctor
description: >-
  Audits where AI agent instructions live across org, user, repo, skill and
  subagent layers for Claude Code, Codex and Copilot, and reports anything
  that conflicts with, duplicates or is misplaced relative to the shared
  engineering skills, without changing files unless asked. Use when someone
  asks to check, audit or doctor their agent setup, when agents follow
  instructions inconsistently, after installing the shared skills, or before
  onboarding a repo to the standards.
---

# Instructions doctor

Agents load every instruction file they find and concatenate them. Nothing overrides anything, so when two files disagree the agent may follow either, and two engineers asking for the same thing get different results. This skill finds those disagreements and says where each instruction belongs, so that shared work comes out the same whoever asked.

It complements Claude Code's built-in `/doctor prompt-audit` (v2.1.283 or later), which finds stale or contradictory instructions in general. This skill checks placement against our standards.

## Where things belong

- **Shared skills** own process for shared artefacts: branches, commits, PRs, CI setup.
- **Repo `AGENTS.md`** owns facts about the repo: build, test and run commands, structure, gotchas. `CLAUDE.md` is `@AGENTS.md` so every tool reads one file.
- **User files** own personal style: tone, verbosity, shortcuts. Nothing that changes how shared artefacts are produced.
- **Org managed files** hold the few rules every repo shares, and say the shared skills take precedence.
- **Local files** (`CLAUDE.local.md`) hold personal notes for one repo and are gitignored.

The full table, covering every location per tool and the checks C1 to C14, is in `references/layers.md`. Open it when a file doesn't fit the summary above, or when you need a check's ID and severity for the report.

## Workflow

### 1. Inventory

Run the bundled script from the user's current directory. It lists every instruction file by layer, flags lines that mention process, and reports possible secrets by file and line only:

```bash
bash <this skill's directory>/scripts/inventory.sh <path to the shared skills/ directory, if known>
```

It only reads. If the user isn't in a git repository, it covers the org and user layers and says the repo layer was skipped.

### 2. Judge each finding

Read only the files the inventory flagged, plus the repo's `AGENTS.md` and `CLAUDE.md`. For each process mention, decide whether it's a rule or just a fact. "Use Conventional Commits" is a rule. "The release job runs when a PR merges" is a repo fact and stays where it is.

Then classify each finding, most serious first:

1. **Critical**: a secret in an instruction file.
2. **Conflict**: contradicts a shared skill, or a personal or repo skill overlaps one.
3. **Misplaced**: right content, wrong layer.
4. **Duplicate**: restates something that has a home elsewhere.
5. **Missing**: shared skills not available to an agent the user runs, no `AGENTS.md`, no build and test commands, no managed layer.
6. **Hygiene**: `CLAUDE.md` not importing `AGENTS.md`, an ungitignored `CLAUDE.local.md`, an oversized file.

Personal files are the user's own, so describe what's in them without quoting more than the line that matters. Never print a secret, only where it is.

### 3. Report

Open with one line of counts, e.g. "2 conflicts, 1 misplaced, 3 hygiene". Then one table, most serious first:

| Severity | Layer | File:line | Finding | Fix |
|---|---|---|---|---|
| Conflict | User | `~/.claude/CLAUDE.md:14` | Says to put the ticket in brackets at the start of commit subjects | Delete the line; `commit-and-pr` owns commit format |

After the table, list in one line what's already in the right place, so the user knows what was checked. If the org layer is missing, say so once as a note for admins rather than as the user's problem.

### 4. Fix, only when asked

- **Repo files**: make the change on a branch and open a draft PR, following `commit-and-pr`.
- **User files and auto memory**: show the exact lines to remove or move, and change them only after the user says yes. They're personal.
- **Managed files**: never edit them. Draft a short note the user can send to whoever owns them.

## When not to use

- General staleness, broken references or instructions written for older models: run Claude Code's `/doctor prompt-audit`.
- Writing commits or PRs: `commit-and-pr`.
- Setting up a repo's CI: `repo-ci-setup`.
