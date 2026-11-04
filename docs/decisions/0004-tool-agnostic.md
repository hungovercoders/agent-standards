# 0004: Tool-agnostic skills and repo instructions

## Context

Engineers use Claude Code, Codex and GitHub Copilot, and the set changes.
All three read the open Agent Skills format (`SKILL.md`), and all read a
repo's `AGENTS.md`; Claude Code reads `AGENTS.md` only when there's no
`CLAUDE.md`, or through an `@AGENTS.md` import.

## Decision

- One canonical copy of each skill in `skills/`, served by a Claude Code
  plugin whose root is this repo, by committed `.claude/skills` and
  `.codex/skills` symlinks, and by `task install:skills` for user installs.
- Repo facts live in `AGENTS.md`; `CLAUDE.md` contains `@AGENTS.md`.
- Skills use plain `git` and `gh` and name a tool only for a tool-only step.

Pattern taken from [dataGriff/skills](https://github.com/dataGriff/skills).

## Consequences

- No copies to keep in sync; a `git pull` or plugin update reaches every tool.
- Some Claude Code features (managed `CLAUDE.md`, auto memory, plugin
  namespacing) have no equivalent elsewhere. Skills treat them as optional.
- Windows users need symlinks enabled, or use the plugin.
