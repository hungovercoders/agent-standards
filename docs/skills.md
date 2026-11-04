# Creating and changing skills

A skill earns its place here when it shapes something other people consume
(a commit, a PR, a ticket, a repo's setup) and the same process applies in
every repo. Personal workflows belong in people's own skills directories;
repo-specific procedures belong in that repo's `.claude/skills/`.

## Before you start

Whether a skill belongs here at all, and when a change needs a decision
record, is decided in [CONTRIBUTING.md](../CONTRIBUTING.md); read it when
you're proposing a skill or changing what one produces. This doc covers
how to write one that works in every agent.

## Anatomy

```
skills/my-skill/
├── SKILL.md          required: frontmatter + instructions
├── references/       detail loaded only when a stated condition fires
├── scripts/          helpers the skill runs (run, not read)
└── assets/           templates and files the skill copies
```

Scaffold with `task new:skill NAME=my-skill`, then add it to a family in
[catalog.md](catalog.md); `task check:skills` fails until you do.

## Writing it

- **Description first.** It's the only trigger and loads in every
  conversation. Say what the skill does, then "Use when…" with the phrases
  people actually type.
- **Imperative, with reasons.** Agents follow reasoning better than stacked
  MUSTs, and a reason lets them handle cases you didn't foresee.
- **Draft before side effects.** Show the message, PR or change and act only
  when asked. A step the request clearly implies, such as pushing a commit
  you were asked to make, is fine if the reply says it happened. Never invent facts such as a ticket ID or testing that wasn't
  done; ask instead.
- **Opt-in references.** Every pointer to a bundled file states when to open
  it. Unconditional loads cost a tool turn on every use.
- **Self-contained.** Installed skills don't get `docs/` or `templates/`, so
  anything needed at run time goes in the skill's own folders.

## Tool-agnostic writing

Skills run in Claude Code, Codex and Copilot. To keep them portable:

- Use plain shell commands (`git`, `gh`) rather than a tool's built-in
  command names.
- Say "the user" and "ask", not a specific tool's question widget.
- Refer to other skills by bare name (`commit-and-pr`), not the Claude
  plugin namespace.
- Where a step only exists in one tool (Claude Code's auto memory, its
  managed `CLAUDE.md`), name the tool and make the step skip cleanly when
  it's absent.
- Bundled scripts are POSIX shell or stdlib Python 3, and run on the bash
  3.2 that macOS ships.

## Review

Changes go through a draft PR like anything else. The PR template's "How to
test" asks for the prompt you tried and what came back, so reviewers can
judge the behaviour rather than the prose. A change that alters output
people rely on (a commit format, a PR section) needs a decision record
first; read [decisions/README.md](decisions/README.md) when you're about to
change a standard.

## Measuring effect

Structural checks can't tell whether a skill helps. A contested or
expensive skill gets with/without-skill evals following the pattern in
[dataGriff/skills](https://github.com/dataGriff/skills): realistic prompts,
a grader, and a committed results table.
