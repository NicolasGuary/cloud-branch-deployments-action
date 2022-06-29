#!/bin/sh -

env

TIMESTAMP=$(git log -1 --format='%cd' --date=unix origin/$GITHUB_HEAD_REF)
MESSAGE=$(git log -1 --format='%s' origin/$GITHUB_HEAD_REF)
EMAIL=$(git log -1 --format='%ae' origin/$GITHUB_HEAD_REF)
NAME=$(git log -1 --format='%an' origin/$GITHUB_HEAD_REF)
PR_NUMBER=$1
PR_URL="https://github.com/${GITHUB_REPOSITORY}/pull/${PR_NUMBER}"
if [ -z $PR_NUMBER ]
then
    PR_URL=""
fi
dagster-cloud branch-deployment create-or-update \
    --url https://7151-136-24-32-204.ngrok.io/1/prod \
    --api-token "agent:test:hardcoded" \
    --git-repo-name "$GITHUB_REPOSITORY" \
    --branch-name "$GITHUB_HEAD_REF" \
    --branch-url "https://github.com/${GITHUB_REPOSITORY}/tree/${GITHUB_REF_NAME}" \
    --pull-request-url "$PR_URL" \
    --commit-hash "$GITHUB_SHA" \
    --timestamp "$TIMESTAMP" \
    --commit-message "$MESSAGE" \
    --author-name "$NAME" \
    --author-email "$EMAIL"
