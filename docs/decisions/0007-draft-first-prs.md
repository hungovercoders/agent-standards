# 0007: Draft-first PRs, green CI before review

Status: Proposed · 2026-11-04

## Context

The team raises draft PRs, reviews them, then converts them to full PRs.
We commit small and push often. GitHub can block a merge on CI but can't
stop a draft being marked ready while CI fails.

## Decision

- `commit-and-pr` pushes each commit it's asked to make, offers to open a
  draft PR after the first push, and only ever opens PRs as drafts.
- CI runs on every push to a draft.
- Before marking a draft ready, the skill runs `gh pr checks` and refuses if
  anything is failing, running or missing. It refreshes the description to
  match the final diff.
- The merge itself is hard-blocked by the CI-required ruleset.

## Consequences

- Reviewers are only asked to look at green PRs.
- The ready-gate is guidance, not enforcement: someone can still click
  "Ready for review" in the UI. The merge gate catches it.
- Frequent pushes mean more CI runs; `concurrency` cancels superseded ones.
