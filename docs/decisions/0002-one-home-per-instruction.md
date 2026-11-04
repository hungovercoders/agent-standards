# 0002: One home per instruction

Status: Proposed · 2026-11-04

## Context

Agents load managed, user, repo, local and skill instructions together and
concatenate them. Nothing overrides anything, and contradictions are
resolved arbitrarily. Two engineers with different personal files get
different output from the same repo.

## Decision

Each kind of instruction lives in exactly one layer, defined in the
`instructions-doctor` skill's `references/layers.md`. The doctor checks
placement; it doesn't change files unless asked.

## Consequences

- Fixing inconsistency means moving or deleting instructions, not adding
  more "always do X" lines that compete further.
- The layer table lives inside the skill because the skill runs in other
  repos; `docs/instruction-layers.md` explains it and links there.
- People will need to remove process rules from their personal files.
  The doctor shows them exactly which lines.
