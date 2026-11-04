# Why we homogenise how we use AI agents

Every engineer now works with an AI coding agent, and each agent follows
whatever instructions it finds: the org's, the person's, the repo's, and any
skills installed. Without a shared shape, the same request produces different
commits, PRs and setups depending on who asked, in which repo, with which
tool. This repo gives the shared parts of that work one shape.

## The goal

**Shared work comes out the same, whoever produced it and whichever agent
they used.** "Shared work" means the artefacts other people consume:
branches, commits, pull requests, CI, and the instruction files themselves.

That gives us two things we care about.

**Shared expectations.** A reviewer opening any PR knows it links to a
Linear issue, says what changed, why, how to test it and what could break,
and that CI was green before they were asked to look. A new joiner learns
one way of working, not one per team. An agent in any repo finds the build
and test commands in the same place.

**Throughput.** Less time goes on reformatting, chasing missing context and
re-running review after CI fails. Agents produce mergeable output first time
because they aren't choosing between competing instructions. Repos can be
picked up by anyone, human or agent, without a guided tour.

Two smaller benefits follow. Every change traces back to a Linear issue,
and a standard changes in one place, through a PR, and reaches everyone on
their next update.

## What we deliberately don't standardise

How individuals work stays theirs: tone, verbosity, how much the agent
explains, editor and tool choice, personal shortcuts and workflows nobody
else consumes. The test is simple: **does anyone else consume the output?**
If yes, it follows the shared standard. If no, it's personal.

We're also not standardising opinions that people argue about: code review
style, testing philosophy, API naming. Those come later, if at all, once the
low-debate standards have earned trust.

## Principles

1. **One home per instruction.** Agents load every instruction file together
   and don't resolve contradictions; they may follow either one. So each kind
   of instruction lives in exactly one layer.
2. **Skills own process, repos own facts, people own style.** Process is the
   same everywhere, so it's versioned once as a skill. Facts differ per repo,
   so they live in the repo's `AGENTS.md`. Style is personal.
3. **Tool-agnostic.** One canonical copy of each skill in the open Agent
   Skills format, served to Claude Code, Codex and Copilot. Repo facts in
   `AGENTS.md`, which they all read.
4. **Adopt, don't invent.** Conventional Commits, Linear's branch names and
   magic words, GitHub rulesets. There's less to debate and less to teach.
5. **Start with low debate.** Commits and PRs first. They're used daily and
   few people feel strongly about them.
6. **Guide with skills, enforce with machines.** Skills shape behaviour.
   Rulesets and CI make the few non-negotiables hard rules, because
   instructions alone can be ignored.
7. **Opt in, never break.** Repos join stricter rules once they're ready,
   so nothing stops working on rollout day.
8. **Change by PR.** Every standard here has a decision record and changes
   through review like any other code.

The reasoning behind each standard is in [decisions/](decisions/README.md).

## How we'll know it's working

Take a baseline before rollout, then watch:

- the share of repos opted into the CI ruleset (`ci-enabled`)
- the share of PRs linked to a Linear issue
- time from "ready for review" to merge
- findings from `instructions-doctor` falling over time
- what reviewers and pilot teams say

If a standard adds friction without moving any of these, change it or drop
it. That's what the decision records are for.
