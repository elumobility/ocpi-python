# Branch Protection Setup Guide

This document explains how to set up branch protection for the `main` branch using GitHub CLI or the web interface.

## Using GitHub CLI (Recommended)

Run the following command to protect the `main` branch:

```bash
gh api repos/elumobility/ocpi-python/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Lint","Type Check","Test (3.11)","Test (3.12)"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"require_last_push_approval":false}' \
  --field restrictions=null \
  --field required_linear_history=false \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## Using GitHub Web Interface

1. Go to: `https://github.com/elumobility/ocpi-python/settings/branches`
2. Click "Add rule" or edit the existing rule for `main`
3. Configure the following settings:

### Branch Protection Settings

- **Require a pull request before merging**
  - ✅ Require approvals: `1`
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners
  - ✅ Require last push approval (optional)

- **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Required status checks:
    - `Lint`
    - `Type Check`
    - `Test (3.11)`
    - `Test (3.12)`

- **Require conversation resolution before merging**
  - ✅ (Recommended)

- **Do not allow bypassing the above settings**
  - ✅ (Recommended for security)

- **Restrict who can push to matching branches**
  - (Optional - only if you want to restrict pushes)

- **Allow force pushes**
  - ❌ (Disabled for security)

- **Allow deletions**
  - ❌ (Disabled for security)

## Benefits

1. **Code Quality**: All code must pass CI checks before merging
2. **Code Review**: At least one approval required (from code owners when CODEOWNERS file applies)
3. **History Protection**: Prevents force pushes and branch deletion
4. **Consistency**: Ensures all changes go through the same review process

## Note

If you need to create a team for code owners:
1. Go to: `https://github.com/orgs/elumobility/teams`
2. Create a team named `ocpi-python-maintainers`
3. Add maintainers to the team
4. The CODEOWNERS file will automatically request reviews from team members
