# Contributing

Everything in `skills/` reaches every engineer on their next plugin update
or `git pull`, in every repo they open, in whichever agent they use. That
makes fixes cheap and new rules expensive. This page is the bar for both.

## Fixes: just open a PR

A typo, a clearer sentence, a broken command, a step agents keep getting
wrong. Open a draft PR; the template asks what changed and how you tested
it. For a skill, "how you tested" is the prompt you gave the agent and
what came back.

## Changing what a skill produces

A commit format, a PR section, a check name: anything other people consume
is a standard, and changing it changes everyone's output.

1. Add a record in `docs/decisions/` that supersedes the old one: context,
   decision, consequences. Keep it short.
2. Change the skill in the same PR.
3. Paste the before-and-after prompt and output under "How to test".

The owners in `.github/CODEOWNERS` review it. Expect questions about who
is affected and what breaks for people mid-flow.

## Proposing a new skill or standard

Open an issue with the "Propose a standard" template, or a draft PR that
holds only the decision record. Four questions decide whether it belongs:

- **Does anyone else consume the output?** If not, it is personal: keep it
  in your own skills directory. Shared skills own shared artefacts.
- **Is there an existing convention?** Adopt it (Conventional Commits,
  Linear's branch names, GitHub rulesets). Inventing one invites debate and
  gives new joiners one more thing to learn.
- **Is it low debate?** If people argue about it, settle the argument in
  the decision record first and write the skill second.
- **Does it overlap a skill we have?** One skill owns each artefact. A
  skill that needs a commit or PR hands off to `commit-and-pr`.

If all four pass, scaffold it with `task new:skill NAME=my-skill` and
follow [docs/skills.md](docs/skills.md) for how to write it so it works in
Claude Code, Codex and Copilot alike.

## What we are not standardising yet

Code review style, testing philosophy, API naming, anything people feel
strongly about. Those come after commits, PRs and CI have earned trust.
Proposals for them are welcome as issues, so the discussion has a home.

## Working on this repo

This repo follows its own standard: branches come from Linear, commits
follow `commit-and-pr`, PRs open as drafts, and the `ci` check must be
green before a draft is marked ready.

```bash
mise install    # pinned tools (task, python); or scripts/bootstrap.sh
task setup      # git hooks: pre-commit runs `task check`, pre-push runs `task ci`
task check      # skill, context-budget and JSON checks, same as CI
```

When a check fails on a budget, move content deeper (into `docs/` or a
skill's `references/`) rather than raising the budget. The budgets are
what keep agents following the rules we write.
