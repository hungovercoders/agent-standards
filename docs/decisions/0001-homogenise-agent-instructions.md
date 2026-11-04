# 0001: Homogenise how we use AI agents for shared work

Status: Proposed · 2026-11-04

## Context

Every engineer works with an AI agent, and each agent follows whatever
instructions it finds. The same request produces different commits, PRs
and repo setups depending on who asked, where, and with which tool.
Reviewers can't predict what they'll get, and time goes on reformatting,
chasing context and re-review.

## Decision

Standardise the artefacts other people consume (branches, commits, PRs, CI,
instruction files) through shared skills and a small amount of enforcement.
Leave everything personal alone: tone, verbosity, tools, private workflows.

## Consequences

- Reviewers and agents share expectations about every PR and repo.
- Throughput rises as rework and back-and-forth fall. We'll check this
  against the signals in `docs/why.md` rather than assume it.
- Each new standard costs some debate, so we start with low-debate ones
  and add more only when the first have earned trust.
