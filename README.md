# agent-standards

Shared skills that make AI coding agents produce the same commits, pull
requests and CI setup for everyone at hungovercoders, whichever agent they
use. One copy of each skill serves Claude Code, Codex and GitHub Copilot.

## Install in two minutes

Claude Code:

```text
/plugin marketplace add hungovercoders/agent-standards
/plugin install agent-standards@hungovercoders
```

Codex, Copilot, or Claude Code without the plugin:

```bash
git clone https://github.com/hungovercoders/agent-standards
cd agent-standards
mise install   # then activate mise in your shell; or scripts/bootstrap.sh
task install:skills AGENTS=codex,copilot   # drop AGENTS= if you skip the plugin
```

## Then try it

| Say to your agent             | What happens                                                        |
| ----------------------------- | ------------------------------------------------------------------- |
| "check my agent setup"        | the doctor finds instructions that compete with the shared skills   |
| "commit this"                 | a Conventional Commit linked to your Linear issue, pushed           |
| "open a PR"                   | a draft PR with What, Why, How to test and Risks                    |
| "set up CI for this repo"     | one `ci` job that runs on drafts and gates the merge                |

The standard covers commits, PRs and CI: solved once, the same way
everywhere, so reviewers and agents share expectations. Your tone, tools
and personal workflows stay yours.

## Learn more

- [docs/why.md](docs/why.md): what we standardise, what stays personal, and why
- [docs/catalog.md](docs/catalog.md): every skill and the phrases that trigger it
- [docs/install.md](docs/install.md): per-tool install details and caveats
- [docs/external-skills.md](docs/external-skills.md): skills from outside this repo to adopt next, such as Cloudflare's
- [docs/github-setup.md](docs/github-setup.md): the org rulesets and property, and how they're applied

## Contribute

Everything here reaches every engineer on their next update, so read
[CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill. Fixes are
welcome with no ceremony; new rules need a decision record. To work on the
repo:

```bash
mise install && task setup   # pinned tools, then git hooks
task --list                  # every command; `task check` is what CI runs
```
