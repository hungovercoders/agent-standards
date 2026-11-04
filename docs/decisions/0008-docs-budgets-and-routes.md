# 0008: Docs have budgets and explicit routes

Status: Proposed · 2026-11-04

## Context

Agents load `AGENTS.md` on every task, and instruction-following degrades
as rules pile up. Docs that agents never find might as well not exist, and
"see docs/x.md" is a pointer agents tend to skip.

## Decision

- `AGENTS.md` carries what most tasks need, within ~150 lines.
- Everything else lives in `docs/`, reached by explicit routes: a trigger,
  then "read", then the file.
- Budgets and routes are checked by `task check:context` in hooks and CI.
- The same layout is what `templates/repo/AGENTS.md.tmpl` gives other repos.

Pattern taken from [dataGriff/skills](https://github.com/dataGriff/skills).

## Consequences

- A failing budget means moving content deeper, never raising the limit.
- Every new doc needs a route, or CI fails.
