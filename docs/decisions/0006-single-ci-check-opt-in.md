# 0006: One required check named `ci`, opted into per repo

## Context

An org ruleset requires a status check by name. A required check that never
runs doesn't fail; it waits forever, so a single org-wide rule would block
every repo without CI on day one.

## Decision

- Every repo's CI exposes one job named exactly `ci`, running on draft PRs.
- A baseline ruleset applies to all repos: PR required, no force pushes, no
  deleting the default branch.
- A second ruleset requires `ci`, targeting repos whose `ci-enabled`
  custom property is true. `repo-ci-setup` sets it only after `ci` has
  passed on a PR.
- Org admins can bypass, for CI outages.

## Consequences

- Nothing blocks a repo without CI; repos join when `ci` passes, and the
  opted-in set is a query on one property.
- Renaming the job, or adding a matrix to it, breaks the ruleset match.
- Required approvals are 0, because review happens on the draft.
