---
name: commit-and-pr
description: >-
  Drafts Conventional Commits messages and draft-first pull requests from the
  actual diff, linked to Linear issues through Linear's branch names and magic
  words, and refuses to mark a draft ready until CI is green. Use when creating
  a branch, committing, pushing, writing a commit message, opening or updating
  a pull request, or marking a draft PR ready for review.
---

# Commits and Pull Requests

Write commit messages and PR descriptions in one consistent format, based on what the diff actually does, and linked to the right Linear issue. Reviewers then know what every PR holds and that CI passed before they were asked to look.

## Linear issues

Every branch, commit and PR should trace back to a Linear issue.

**Issue IDs** look like `ABC-123`: the team key, a hyphen, then the number. Always write them in uppercase in commits and PRs.

**Finding the issue ID**
1. Read the current branch with `git branch --show-current`.
2. Match the first issue ID in it, ignoring case (pattern `[A-Za-z]+-[0-9]+`). Linear branch names are lowercase, e.g. `jo/abc-123-add-card-retry` → `ABC-123`.
3. If there's no ID in the branch name, ask the user for it. Do not guess or invent one.

**Branch names**
- Use the branch name Linear generates. In Linear, open the issue and use *Copy git branch name* (Cmd/Ctrl + Shift + .).
- Do not hand-craft branch names. If asked to create a branch and the user hasn't given Linear's branch name, ask them to copy it from the issue.

**Magic words** link commits and PRs to the issue and drive its status in Linear.

| Word | Effect | Use when |
|------|--------|----------|
| `Fixes ABC-123` | Links, and moves the issue to Done when merged to the default branch | The PR completes the issue |
| `Part of ABC-123` | Links without closing | The PR is one step of a larger issue |
| `Refs ABC-123` | Links without closing | Commits, or loosely related work |

Write magic words without a colon, e.g. `Fixes ABC-123`, not `Fixes: ABC-123`.

## Commit messages

### Steps

1. Read the staged changes with `git diff --staged`. If nothing is staged, say so and ask what should be included. Do not stage files without being asked.
2. Check the change is one logical unit. If it mixes unrelated work (e.g. a feature plus an unrelated refactor), suggest splitting it before writing a message.
3. Find the Linear issue ID as described above.
4. Draft the message using the format below and show it to the user.
5. Commit only when the user asks.
6. Push the commit to the remote with `git push` (`git push -u origin HEAD` on a branch's first push). The team commits small and pushes every commit, so a request to commit covers pushing it to its own feature branch: say in your reply that you pushed. Skip the push if the user says not to, and never push to the default branch.

### Format

Follow [Conventional Commits](https://www.conventionalcommits.org):

```
<type>(<optional scope>): <subject>

<optional body>

Refs ABC-123
```

**Types**

| Type | Use for |
|------|---------|
| `feat` | A new feature or behaviour |
| `fix` | A bug fix |
| `refactor` | Code change with no behaviour change |
| `test` | Adding or changing tests only |
| `docs` | Documentation only |
| `perf` | Performance improvement |
| `build` | Build system or dependencies |
| `ci` | Pipeline configuration |
| `chore` | Anything else that doesn't touch production code |

**Subject**
- Imperative mood: "add", not "added" or "adds"
- 72 characters or fewer, lowercase start, no full stop
- Says what changed, not how

**Body** (include when the reason isn't obvious from the subject)
- Explain *why* the change was made, not what each line does
- Wrap at 72 characters

**Footer**
- Always end with `Refs ABC-123`. Use the non-closing word in commits; the PR decides whether the issue closes.
- Breaking changes: add `BREAKING CHANGE: <what breaks and what to do instead>` above the issue reference.

### Examples

```
feat(payments): add retry for failed card authorisations

Card auths fail intermittently when the provider times out. Retrying
once with backoff recovers most of these without user action.

Refs PAY-412
```

```
fix: handle empty basket on checkout page

Refs SHOP-88
```

## Pull requests

### Steps

1. Compare the branch with its base: `git log --oneline <base>..HEAD` and `git diff <base>...HEAD`. Use the repo's default branch as the base (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`) unless told otherwise.
2. Find the Linear issue ID as described above.
3. Decide the magic word: `Fixes` if this PR completes the issue, `Part of` if more work will follow. If it isn't clear, ask the user.
4. Write the title in the same format as a commit subject, summarising the whole PR.
5. Fill in the description template below from the diff and commits. Leave out any section that genuinely doesn't apply. Never invent testing that wasn't done.
6. Show the title and description to the user.
7. Only open the PR when asked. Always open it as a draft: with the GitHub CLI, use `gh pr create --draft`. The team reviews drafts before marking them ready.

### Description template

```markdown
Fixes ABC-123

## What
<One or two sentences on what this PR changes.>

## Why
<The problem or need behind it.>

## How to test
<Steps a reviewer can follow to check it works.>

## Risks
<Anything that could break, migrations, feature flags, rollout notes. Write "Low" if there's nothing notable.>
```

### Marking a draft ready for review

Draft PRs are code reviewed first, then converted to a full PR. A draft must pass CI before it is marked ready. GitHub does not enforce this itself, so this skill does. When the user asks to mark a draft ready:

1. Check CI with `gh pr checks`. All checks must have passed.
   - **Failing:** stop. Show which checks failed and offer to look at the logs with `gh run view --log-failed`. Do not mark it ready.
   - **Still running:** stop and say so. Offer to wait with `gh pr checks --watch`, then carry on if they pass.
   - **No checks reported:** stop. The repo has no CI job yet, or it didn't trigger. Point the user to the `repo-ci-setup` skill. Do not mark it ready.
2. Compare the branch with its base again. Commits added during review often make the original description out of date.
3. Update the title and description so they match the final diff. Check the magic word still fits (`Fixes` or `Part of`).
4. Show the user what changed in the description.
5. Mark it ready only when the user confirms. With the GitHub CLI, use `gh pr ready`.

Never skip the CI check, even if the user says the failure is unrelated. Tell them to fix it or re-run it, or to mark the PR ready themselves if they accept the risk.

### Guidance

- After the first push on a branch with no PR, offer to open the draft. CI runs on pull requests, not on pushes to feature branches, so an early draft gets every later push checked.
- If the PR is large (roughly 400+ changed lines across many files), mention that splitting it would make review easier.
- Point reviewers to the files that matter most if the change is spread out.
- Keep it short. Reviewers should understand the PR in under a minute.

## When not to use

- Setting a repo up so the `ci` check exists and is required: that's `repo-ci-setup`.
- Instructions elsewhere tell you to format commits or PRs differently: don't merge the two styles. Follow this skill and suggest running `instructions-doctor` to find and remove the competing rule.
