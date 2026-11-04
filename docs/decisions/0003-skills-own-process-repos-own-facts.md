# 0003: Skills own process, repos own facts, people own style

Status: Proposed · 2026-11-04

## Context

Process (how to commit, open a PR, set up CI) is the same in every repo.
Facts (how to build and test this service) differ per repo. Style (how
chatty the agent is) differs per person. Mixing them in one file means
copying process into every repo and drifting.

## Decision

- Process for shared artefacts lives in shared skills, versioned here.
- Repo facts live in the repo's `AGENTS.md`.
- Personal style lives in personal files and never changes shared output.
- The org's managed file stays tiny: it says the shared skills take precedence.

## Consequences

- Changing a process is one PR here, not a sweep across repos.
- Repo `AGENTS.md` files get shorter and agents follow them more reliably.
- Subagents that commit or open PRs point to `commit-and-pr` rather than
  carrying their own rules.
