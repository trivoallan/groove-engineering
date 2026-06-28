#!/usr/bin/env bash
# Usage: ./process/feedback.sh <PR> <Name> <message>
# Ex:    ./process/feedback.sh 2 "Alex" "Not really my field but I dig it"

set -e

PR="${1:?Usage: feedback.sh <PR> <Name> <message>}"
NAME="${2:?Name missing}"
MSG="${3:?Message missing}"

gh pr comment "$PR" \
  --repo trivoallan/groove-engineering \
  --body "👂 **${NAME}** (via WhatsApp): *${MSG}*"
