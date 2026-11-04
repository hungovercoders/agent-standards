# Instruction layers: the rules the doctor checks

Agents load every instruction file they find and concatenate them. Nothing overrides anything, and when two instructions contradict each other the agent may follow either. So each kind of instruction has one home.

## Where things belong

| Layer | Locations | Belongs here | Keep out |
|-------|-----------|--------------|----------|
| Org guidance | Claude Code managed `CLAUDE.md`: macOS `/Library/Application Support/ClaudeCode/`, Linux and WSL `/etc/claude-code/`, Windows `C:\Program Files\ClaudeCode\`; or the `claudeMd` key in managed settings | A few lines every repo shares, and the statement that the shared skills win on their topics | Repo facts, personal style, detailed process |
| Org enforcement | `managed-settings.json` in the same folder; GitHub org rulesets | Enabling the `agent-standards` plugin; hard limits such as `permissions.deny`; the merge rules | Behavioural guidance |
| Shared skills | The agent-standards repo's `skills/`, reached through the Claude Code plugin or symlinks in `~/.claude/skills`, `~/.codex/skills`, `~/.copilot/skills` | Process that produces shared artefacts: branches, commits, PRs, CI setup | Repo facts, personal preferences |
| User | `~/.claude/CLAUDE.md`, `~/.claude/rules/`, `~/.codex/AGENTS.md` | Personal style: tone, verbosity, how much to explain, personal tool shortcuts | Rules for commits, branches, PRs, tickets or CI; facts about one repo |
| User skills | `~/.claude/skills/`, `~/.codex/skills/`, `~/.copilot/skills/` (other than links to shared skills) | Personal workflows nobody else consumes | Anything overlapping a shared skill |
| User agents | `~/.claude/agents/` | Personal subagents | Their own commit or PR rules; an agent that commits or opens PRs follows `commit-and-pr` |
| Repo | `AGENTS.md` at the root (read by Codex, Copilot and Claude Code); `CLAUDE.md` containing `@AGENTS.md`; nested `AGENTS.md` for subprojects | Facts about this repo: build, test and run commands, structure, domain rules, gotchas; routes into `docs/` | Org-wide process, personal preferences, secrets |
| Repo, tool-specific | `.claude/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, `.cursor/rules/` | Only what one tool genuinely needs and others don't | Copies of `AGENTS.md` content, which drift apart |
| Repo skills and agents | `.claude/skills/`, `.codex/skills/`, `.claude/agents/` | Procedures specific to this repo, e.g. running its migrations | Copies or variants of shared skills |
| Local | `CLAUDE.local.md` (gitignored), `.claude/settings.local.json` | Personal notes for one repo: sandbox URLs, test data | Anything the team needs |
| Auto memory | `~/.claude/projects/<project>/memory/` | Learnings the agent saves for itself | Process preferences that compete with shared skills |

## Checks

| ID | Check | Severity if it fails |
|----|-------|----------------------|
| C1 | The shared skills are available to each agent the person uses: plugin `agent-standards@hungovercoders` enabled for Claude Code, symlinks into agent-standards for Codex or Copilot | Missing |
| C2 | No instructions about commits, branches, PRs, tickets or CI setup outside the shared skills | Conflict if it contradicts a skill, Duplicate if it restates one |
| C3 | No user or repo skill overlaps a shared skill by name or by what its description triggers on | Conflict |
| C4 | Subagents that commit, push or open PRs point to `commit-and-pr` instead of carrying their own rules | Conflict or Duplicate |
| C5 | Repo files hold no personal preferences or machine paths such as `/Users/<name>/` | Misplaced |
| C6 | User files hold no facts about one specific repo | Misplaced |
| C7 | The repo has an `AGENTS.md` with build and test commands | Missing |
| C8 | `CLAUDE.md`, if present, is `@AGENTS.md` plus at most a few Claude-only lines. With both files and no import, Claude Code reads only `CLAUDE.md` and other tools only `AGENTS.md`, so they drift | Hygiene |
| C9 | Tool-specific repo files don't repeat `AGENTS.md` content | Duplicate |
| C10 | `CLAUDE.local.md`, if present, is gitignored | Hygiene |
| C11 | `AGENTS.md` stays under about 150 lines and each other instruction file under about 200; past that, agents start dropping rules | Hygiene |
| C12 | No secrets in any instruction file | Critical |
| C13 | Auto memory holds no process preferences for commits, PRs or branches | Conflict |
| C14 | A managed layer exists and says the shared skills take precedence | Missing (for admins) |

## Severity order

1. **Critical**: a secret in an instruction file. Fix now.
2. **Conflict**: contradicts a shared skill, so output depends on which instruction the agent happens to follow.
3. **Misplaced**: right content, wrong layer.
4. **Duplicate**: restates something with a home elsewhere. Harmless today, drifts tomorrow.
5. **Missing**: something the standard expects isn't there.
6. **Hygiene**: size, gitignore, AGENTS.md wiring.

## Telling a rule from a mention

Only flag instructions that tell the agent how to do the process. "Use Conventional Commits" or "PR titles start with the ticket" is a rule. "The release job runs when a PR merges" is a repo fact, so it stays.
