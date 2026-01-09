#!/bin/bash
# Script to set up branch protection for the main branch
# Run this script to protect the main branch with appropriate rules

set -e

REPO="elumobility/ocpi-python"
BRANCH="main"

echo "Setting up branch protection for $REPO:$BRANCH..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Run: gh auth login"
    exit 1
fi

# Set up branch protection using stdin
cat << 'JSON' | gh api repos/$REPO/branches/$BRANCH/protection --method PUT --input -
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Lint", "Type Check", "Test (3.11)", "Test (3.12)"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

echo "✅ Branch protection enabled for $BRANCH branch!"
echo ""
echo "Protection rules:"
echo "  - Require pull request reviews: 1 approval"
echo "  - Require code owner reviews: Yes"
echo "  - Require status checks: Lint, Type Check, Test (3.11), Test (3.12)"
echo "  - Require branches to be up to date: Yes"
echo "  - Allow force pushes: No"
echo "  - Allow deletions: No"
echo ""
echo "Note: Make sure to:"
echo "  1. Create a team 'ocpi-python-maintainers' in your organization"
echo "  2. Add maintainers to the team"
echo "  3. Update .github/CODEOWNERS with actual usernames/team names"
