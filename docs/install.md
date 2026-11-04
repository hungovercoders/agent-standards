# Installing the skills

Claude Code, Codex and GitHub Copilot all read the same Agent Skills format
(`skills/<name>/SKILL.md`), so there is one canonical copy of every skill
and everything else points at it. Nothing is duplicated, and a `git pull`
or plugin update reaches every agent at once. This is the pattern from
[dataGriff/skills](https://github.com/dataGriff/skills).

## Claude Code: plugin (no clone)

`.claude-plugin/marketplace.json` makes this repo a plugin marketplace whose
single plugin is the repo itself (`source: "./"`, `strict: false`), so the
`skills/` directory doubles as the plugin's skills and a new skill ships
with no manifest edit.

```text
/plugin marketplace add hungovercoders/agent-standards
/plugin install agent-standards@hungovercoders
```

Updates arrive with `/plugin marketplace update hungovercoders`. Plugin
skills are namespaced, e.g. `/agent-standards:commit-and-pr`, but trigger
on plain requests all the same. After editing the manifest, check it with
`claude plugin validate .`.

**For everyone at once:** an admin can enable the plugin on every machine
through managed settings; start from
`templates/managed/managed-settings.json`. Managed settings win over every
other scope, so nobody has to remember to install it.

**Offered per repo:** commit `templates/repo/.claude/settings.json` into a
repo and anyone who trusts the folder is offered the plugin. Some users
report the prompt not appearing
([issue](https://github.com/anthropics/claude-code/issues/32606)), so keep
the two commands above in onboarding.

## Codex and Copilot: symlinks (clone once)

Codex and Copilot have no marketplace, so clone this repo and link the
skills into each agent's personal skills directory:

```bash
task install:skills AGENTS=codex,copilot   # alongside the Claude Code plugin
task install:skills                        # all three agents, if you skip the plugin
task install:skills GROUP=work             # one family (see catalog.md)
task install:skills SKILLS=commit-and-pr   # single skills; combines with GROUP
task uninstall:skills                      # remove our links, nothing else
```

This links each `skills/<name>` into `~/.claude/skills/`, `~/.codex/skills/`
and `~/.copilot/skills/`, one link per skill, so they sit alongside skills
from other sources. The installer never touches entries it didn't create,
re-points stale links after the clone moves, and removes links to skills
that no longer exist after a pull.

Use the plugin or the symlinks for Claude Code, not both: two copies of the
same skill compete, and `instructions-doctor` flags it.

## In this repo

| Symlink | Served agents |
|---|---|
| `.claude/skills -> ../skills` | Claude Code, and Copilot (it reads `.claude/skills`) |
| `.codex/skills -> ../skills` | Codex (it reads only `.codex` paths; symlinks work) |

Open this repo in any of the three tools and the skills are available with
no install step. `.agents/skills`, the emerging cross-agent location, is
deliberately absent: Copilot already finds `.claude/skills`, and a second
discovery path risks double-loading.

## Caveats

- **`task` not found after `mise install`**: mise only puts tools on PATH
  once it is activated in your shell (`eval "$(mise activate bash)"`, or
  the equivalent for your shell from the mise docs). `scripts/bootstrap.sh`
  installs `task` to `~/.local/bin`, which must be on your PATH.
- **Windows**: committed symlinks need `core.symlinks=true` and Developer
  Mode (or admin); otherwise they check out as text files. The installer
  needs the same. WSL works out of the box.
- **Agents other than these three**: any tool that reads the Agent Skills
  format can be pointed at `skills/`. Add it to `install_skills.py` through
  a PR rather than copying files.
