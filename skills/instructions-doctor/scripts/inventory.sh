#!/usr/bin/env bash
# List every instruction file an AI coding agent may load for the current
# user and repo, grouped by layer, then scan them for process rules and
# secrets. Read-only: it never changes a file.
#
# Usage: bash inventory.sh [shared-skills-dir]
#   shared-skills-dir  the agent-standards skills/ directory, excluded from the
#                      process-rule scan because those rules belong there.
#
# Portable to the bash 3.2 that ships with macOS: no mapfile, no globstar.
set -u

shared="${1:-}"
root=$(git rev-parse --show-toplevel 2>/dev/null || true)
list=$(mktemp)
trap 'rm -f "$list"' EXIT

show() { # layer path
  [ -f "$2" ] || return 0
  link=""
  [ -L "$2" ] && link="  (link to $(readlink "$2"))"
  printf '%-8s %5s lines  %s%s\n' "$1" "$(wc -l < "$2" | tr -d ' ')" "$2" "$link"
  printf '%s\n' "$2" >> "$list"
}

show_dir() { # layer dir name-pattern
  [ -d "$2" ] || return 0
  find -L "$2" -type f -name "$3" 2>/dev/null | sort | while read -r f; do show "$1" "$f"; done
}

skill_links() { # layer dir: one line per installed skill, noting symlinks
  [ -d "$2" ] || return 0
  for s in "$2"/*; do
    [ -e "$s" ] || continue
    if [ -L "$s" ]; then
      printf '%-8s  skill       %s -> %s\n' "$1" "$s" "$(readlink "$s")"
    else
      printf '%-8s  skill       %s\n' "$1" "$s"
    fi
    # Scan skills that are not copies of the shared ones: a personal or repo
    # skill is where a competing commit or PR rule would hide.
    if [ -f "$s/SKILL.md" ] && { [ -z "$shared" ] || [ "$(cd "$s" && pwd -P)" != "$(cd "$shared/$(basename "$s")" 2>/dev/null && pwd -P)" ]; }; then
      printf '%s\n' "$s/SKILL.md" >> "$list"
    fi
  done
}

echo "== Org (managed)"
for d in "/Library/Application Support/ClaudeCode" "/etc/claude-code" \
         "/c/Program Files/ClaudeCode" "/mnt/c/Program Files/ClaudeCode"; do
  show managed "$d/CLAUDE.md"
  show managed "$d/managed-settings.json"
done

echo "== User"
show user "$HOME/.claude/CLAUDE.md"
show_dir user "$HOME/.claude/rules" '*.md'
show_dir user "$HOME/.claude/agents" '*.md'
show_dir user "$HOME/.claude/commands" '*.md'
show user "$HOME/.claude/settings.json"
show user "$HOME/.codex/AGENTS.md"
skill_links user "$HOME/.claude/skills"
skill_links user "$HOME/.codex/skills"
skill_links user "$HOME/.copilot/skills"

if [ -n "$root" ]; then
  echo "== Repo ($root)"
  show repo "$root/AGENTS.md"
  show repo "$root/CLAUDE.md"
  show repo "$root/.claude/CLAUDE.md"
  show local "$root/CLAUDE.local.md"
  show repo "$root/.claude/settings.json"
  show local "$root/.claude/settings.local.json"
  show_dir repo "$root/.claude/rules" '*.md'
  show_dir repo "$root/.claude/agents" '*.md'
  show_dir repo "$root/.claude/commands" '*.md'
  show repo "$root/.github/copilot-instructions.md"
  show_dir repo "$root/.github/instructions" '*.md'
  show repo "$root/.cursorrules"
  show_dir repo "$root/.cursor/rules" '*'
  skill_links repo "$root/.claude/skills"
  skill_links repo "$root/.codex/skills"
  find "$root" -mindepth 2 \
    \( -name .git -o -name node_modules -o -name vendor -o -name dist -o -name build -o -name .venv -o -name .claude \) -prune \
    -o -type f \( -name AGENTS.md -o -name CLAUDE.md -o -name CLAUDE.local.md \) -print 2>/dev/null \
    | sort | while read -r f; do show nested "$f"; done

  if [ -f "$root/CLAUDE.local.md" ] && ! git -C "$root" check-ignore -q CLAUDE.local.md; then
    echo "WARN     CLAUDE.local.md is not gitignored"
  fi

  echo "== Auto memory (Claude Code)"
  mem="$HOME/.claude/projects/$(printf '%s' "$root" | tr '/.' '--')/memory"
  if [ -d "$mem" ]; then
    show_dir memory "$mem" '*.md'
  else
    echo "none found at $mem (the folder name may differ; list ~/.claude/projects/ to check)"
  fi
else
  echo "== Repo: not inside a git repository, repo layer skipped"
fi

echo "== Plugins enabled in settings (Claude Code)"
for f in "/Library/Application Support/ClaudeCode/managed-settings.json" "/etc/claude-code/managed-settings.json" \
         "$HOME/.claude/settings.json" ${root:+"$root/.claude/settings.json"}; do
  [ -f "$f" ] && grep -Ho '"[A-Za-z0-9._-]*@[A-Za-z0-9._-]*"[[:space:]]*:[[:space:]]*true' "$f"
done

echo "== Process-rule mentions (judge each: a rule, or just a fact?)"
pattern='commit message|conventional commit|commit format|pull request|PR (title|description|template)|branch nam|squash|gh pr |Fixes [A-Z]+-[0-9]|Refs [A-Z]+-[0-9]|co-authored'
while read -r f; do
  case "$f" in "$shared"/*) [ -n "$shared" ] && continue ;; esac
  grep -niE "$pattern" "$f" 2>/dev/null | cut -c1-160 | sed "s|^|$f:|"
done < "$list"

echo "== Possible secrets (file and line only)"
secrets='sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY'
while read -r f; do
  grep -HnoE "$secrets" "$f" 2>/dev/null | cut -d: -f1,2
done < "$list"
echo "== Done"
