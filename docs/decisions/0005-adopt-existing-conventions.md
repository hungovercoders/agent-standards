# 0005: Adopt existing conventions for commits, branches and links

## Context

Inventing a commit or branch format invites weeks of debate, and every
new joiner has to learn it. We already use Linear, which generates branch
names and links commits and PRs through "magic words".

## Decision

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org).
- Branch names are the ones Linear generates; skills don't hand-craft them.
- Commits end `Refs ABC-123`; PRs start `Fixes ABC-123` (closes on merge)
  or `Part of ABC-123`.

## Consequences

- Little to debate; most engineers know these already.
- Every change traces to a Linear issue, and issues move to Done on merge.
- Linear's "Link commits to issues with magic words" toggle must be on.
