#!/usr/bin/env bash
# Usage: ./process/feedback.sh <PR> <Prénom> <message>
# Ex:    ./process/feedback.sh 2 "Nelly" "Je ne m'y connais pas trop mais sympa"

set -e

PR="${1:?Usage: feedback.sh <PR> <Prénom> <message>}"
NOM="${2:?Prénom manquant}"
MSG="${3:?Message manquant}"

gh pr comment "$PR" \
  --repo trivoallan/groove-engineering \
  --body "👂 **${NOM}** (via WhatsApp) : *${MSG}*"
