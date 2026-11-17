#!/usr/bin/env bash
set -euo pipefail

if [[ -x "/usr/local/bin/gh" ]]; then
  GH="/usr/local/bin/gh"
elif [[ -x "/opt/homebrew/bin/gh" ]]; then
  GH="/opt/homebrew/bin/gh"
elif [[ -x "/usr/bin/gh" ]]; then
  GH="/usr/bin/gh"
else
  GH="gh"
fi

SINCE_UTC=$(date -u -v-10H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "10 hours ago" +"%Y-%m-%dT%H:%M:%SZ")

echo "=========================================================================="
echo "🌅 THE BULL PRINT — 9:00 AM IST MORNING PRODUCTION AUDIT"
echo "   Window: Runs since ${SINCE_UTC} (Last 10 Hours)"
echo "=========================================================================="

echo -e "\n1. MASTER ORCHESTRATOR & SUPERVISOR RUNS:"
$GH run list --workflow=daily_5am_production_master.yml --limit 3 \
  --json databaseId,status,conclusion,event,createdAt \
  --jq '.[] | "   [Master]     ID: \(.databaseId) | Trigger: \(.event) | Status: \(.status) (\(.conclusion // "running")) | Created: \(.createdAt)"' || true

$GH run list --workflow=daily_production_supervisor.yml --limit 3 \
  --json databaseId,status,conclusion,createdAt \
  --jq '.[] | "   [Supervisor] ID: \(.databaseId) | Status: \(.status) (\(.conclusion // "running")) | Created: \(.createdAt)"' || true

echo -e "\n2. 12-VIDEO MATRIX RUNS (parallel_video_matrix.yml):"
$GH run list --workflow=parallel_video_matrix.yml --limit 14 \
  --json databaseId,status,conclusion,createdAt,updatedAt,displayTitle \
  --jq '.[] | "   Run #\(.databaseId) | \(.status) (\(.conclusion // "in_progress")) | Created: \(.createdAt) | \(.displayTitle)"' || true

echo -e "\n3. GENERATED MASTER BROADCAST ARTIFACTS (Last 12):"
$GH api "repos/:owner/:repo/actions/artifacts?per_page=30" \
  --jq '.artifacts[] | select(.name | startswith("master-broadcast-")) | "   📦 \(.name) | Size: \((.size_in_bytes / 1048576 * 10 | round) / 10) MB | Created: \(.created_at)"' | head -n 12 || true

echo -e "\n4. SUMMARY COUNTS (Last 14 Matrix Runs):"
$GH run list --workflow=parallel_video_matrix.yml --limit 14 --json status,conclusion \
  --jq 'group_by(.conclusion // .status) | map("   \(. [0].conclusion // .[0].status): \(length)") | .[]' || true

echo "=========================================================================="
echo "💡 Tip: If any artifacts are deferred waiting for 1:30 PM IST quota reset,"
echo "   run: python scripts/publish_deferred_artifacts.py at 1:35 PM IST."
echo "=========================================================================="
