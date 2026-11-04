# Skills from outside this repo

This repo's own skills are the generic layer: commits, PRs and CI, for
everyone, from day one. As your work moves from generic into platform
and practice, other people's skill sets earn a place next to ours. This
page lists the ones engineers here should adopt, in the order they
usually become relevant. Nothing is copied into this repo: each source
is installed from where it lives, so its updates reach you and its
authors keep owning it.

## Tiers

| Tier | Who | Covers |
|---|---|---|
| **Generic** | everyone, day one | shared artefacts: this repo's skills ([catalog.md](catalog.md)) |
| **Platform** | anyone building or running a service here | the platform we run on: Cloudflare |
| **Practice** | by role, optional | engineering practices: API design, data contracts, BDD, repo health |

Install the generic tier first and run `instructions-doctor`. Add a tier
when you start the work it covers, not before: every installed skill's
description loads into every conversation, whether or not it triggers.

## Platform: Cloudflare

[cloudflare/skills](https://github.com/cloudflare/skills) (Apache-2.0) is
Cloudflare's own set: Workers best practices, Wrangler, Durable Objects,
the Agents SDK, Cloudflare One, Next.js on Cloudflare and more, plus a
`cloudflare` skill that picks the right product and docs for a request.
The plugin also bundles Cloudflare's remote MCP server for its API and
current docs.

Claude Code:

```text
/plugin marketplace add cloudflare/skills
/plugin install cloudflare@cloudflare
```

Codex:

```text
codex plugin marketplace add cloudflare/skills
codex plugin add cloudflare@cloudflare
```

Copilot in VS Code: enable `chat.plugins.enabled`, then run **Chat:
Install Plugin From Source** with `https://github.com/cloudflare/skills`.
Its README also covers Cursor, OpenCode and a plain clone-and-copy route.

Use it when you're building on Workers or any Cloudflare product. It
owns none of our shared artefacts, so it sits alongside our skills
without conflict.

## Practice: dataGriff/skills

[dataGriff/skills](https://github.com/dataGriff/skills) is the upstream
of this repo's layout and tooling, and holds five families of practice
skills: API design and testing (OpenAPI, AsyncAPI, Microcks, API
security), data contracts (ODCS, datacontract-cli), requirements and BDD
(Gherkin, Cucumber.js), repo health (bus factor, consistency, declutter,
agent optimisation) and planning and writing.

Claude Code installs everything:

```text
/plugin marketplace add dataGriff/skills
/plugin install datagriff-skills@datagriff
```

For one family, or for Codex and Copilot, clone it and use its own
installer (`task install:skills GROUP=api`, for example); its
`docs/install.md` has the details. Pick the families your role uses.

## Keeping external skills honest

- **Shared artefacts stay ours.** If an external skill would write
  commits, PRs or CI its own way, our skill owns that artefact. Leave the
  overlapping skill out (most installers take a subset) and run
  `instructions-doctor` after installing anything new.
- **Plugin or symlinks, not both.** Two copies of one skill compete.
- **Don't fork or copy.** A copied SKILL.md is a fork nobody maintains.
  If a source needs a change, send it a PR; if it's abandoned, propose a
  replacement here.
- **Say what you installed.** When agents behave oddly, the doctor's
  inventory shows every skill by source, so the answer is one run away.

## Adding a source

A new section on this page, through a PR, when all of these hold:

- engineers here use the product or practice it covers, and you've tried
  it on real work (the PR's "How to test" says what you asked and what
  came back);
- its licence allows our use, and it's maintained by the people who own
  the product or practice, or by someone we'd accept a PR from;
- it doesn't overlap a skill we own, or you say which of its skills to
  leave out;
- it has a tier, and an install route for each of Claude Code, Codex and
  Copilot, even if that route is "clone and copy".

The bar is the same as for our own skills: read
[../CONTRIBUTING.md](../CONTRIBUTING.md) before you open the PR.
