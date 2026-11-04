# Where instructions belong

Agents read instructions from several layers at once: the org's managed
files, the person's own files, the repo, installed skills and subagents.
They load all of them together and concatenate them. Nothing overrides
anything, and when two instructions disagree, the agent may follow either
([Claude Code docs](https://code.claude.com/docs/en/memory)). The only
reliable fix is placement: each kind of instruction gets one home.

## The model

| Layer | Owns | Why here |
|---|---|---|
| Org (managed) | A few lines every repo shares; that shared skills take precedence | Loads for everyone and can't be excluded, so keep it tiny |
| Shared skills | Process for shared artefacts: branches, commits, PRs, CI setup | Same everywhere, versioned once, loaded only when relevant |
| Repo `AGENTS.md` | Facts: build, test, run, structure, gotchas | Differs per repo; every agent reads `AGENTS.md` |
| User | Personal style: tone, verbosity, shortcuts | Nobody else consumes it |
| Local (`CLAUDE.local.md`) | Personal notes for one repo | Gitignored, so it can't leak into the team's files |
| Enforcement (rulesets, CI, managed settings) | The few rules that must hold | Instructions can be ignored; these can't |

The full table, with every location per tool and the checks the doctor runs,
lives in the doctor skill at
[references/layers.md](../skills/instructions-doctor/references/layers.md).
It lives there rather than here because the skill is installed on its own
into other repos and needs its rules at run time. This doc explains why;
that file is the single source of the what.

## Decisions that follow from the model

**`AGENTS.md` is the repo's canonical file, and `CLAUDE.md` is `@AGENTS.md`.**
Codex and Copilot read `AGENTS.md`. Claude Code reads it only when there's
no `CLAUDE.md`, so a `CLAUDE.md` that imports it keeps one source for every
tool. Claude-only lines can sit under the import, but most repos need none.

**No pointers needed for skills, but routes are cheap.** A skill fires from
its description, so a repo's `AGENTS.md` doesn't have to mention it. One
"Ways of working" line routing commits and PRs to `commit-and-pr` helps
tools whose skill discovery is weaker, and tells humans who owns the rule.

**Personal files lose process rules.** A personal "write commits like X"
competes with `commit-and-pr` in every repo that person touches. Style stays;
process goes.

**Subagents point at skills.** A subagent runs on its own prompt. One that
commits or opens PRs says to follow `commit-and-pr` instead of carrying its
own copy of the rules.

**Auto memory can learn the wrong thing.** Claude Code saves learnings per
repo. If it saved "user prefers commit subjects in brackets", that now
competes with the skill. The doctor checks for it.

**Tool-specific files only for tool-specific needs.**
`.github/copilot-instructions.md`, `.cursor/rules/` and `.claude/rules/` are
for things one tool needs and others don't. Copying `AGENTS.md` content into
them makes copies that drift apart.

## Templates

Starting files for each layer are in `templates/`. The instruction files
carry a `.tmpl` suffix because agents load any `CLAUDE.md` or `AGENTS.md`
they find as live instructions; drop the suffix when you copy one into place.

| File | Use |
|---|---|
| `templates/managed/CLAUDE.md.tmpl` | The org's managed instructions, deployed centrally |
| `templates/managed/managed-settings.json` | Enables the plugin for everyone; pairs with the file above |
| `templates/repo/AGENTS.md.tmpl` | A repo's facts, ready to fill in |
| `templates/repo/CLAUDE.md.tmpl` | `@AGENTS.md`, nothing else |
| `templates/repo/.claude/settings.json` | Offers the plugin to anyone who trusts the repo. Same content as `managed-settings.json`, which is the source: copy it here when it changes |
| `templates/user/CLAUDE.md.tmpl` | An example of what a personal file should and shouldn't hold |

When you change a template, check it still agrees with the doctor's
`references/layers.md`. They describe the same model.
