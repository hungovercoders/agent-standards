# 0009: GitHub configuration as files, applied by a task

Status: Proposed · 2026-11-04

## Context

The skills depend on GitHub being set up a certain way: a custom property,
two rulesets, a few repo settings. Settings clicked into the UI drift, go
unreviewed, and stop matching what the docs say.

## Decision

- The property, rulesets and repo settings live as JSON in `github/`.
- `task setup:github:org` and `task setup:github:repo` apply them via
  `gh api`. Both dry-run unless `APPLY=1`, and are safe to re-run.
- Changes go through a PR to this repo, then get re-applied.
- The baseline ruleset ships disabled; it is switched on by a PR once
  announced.

## Consequences

- Org setup is reviewed like code and repeatable for a second org.
- Edits made in the GitHub UI are overwritten on the next apply, so they
  must be made in the files instead.
- Applying needs an org owner (rulesets, property) or a repo admin (repo
  settings).
