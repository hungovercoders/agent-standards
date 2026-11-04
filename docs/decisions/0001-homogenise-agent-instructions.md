# 0001: Homogenise how we use AI agents for shared work

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
- Throughput rises as rework and back-and-forth fall; the signals in
  `docs/why.md` say whether it does.
- Each standard has an existing convention behind it, so there is little
  to debate and little to teach.
