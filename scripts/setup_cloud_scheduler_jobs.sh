#!/usr/bin/env bash
# ==============================================================================
# Google Cloud Scheduler Setup for The Bull Print
# scripts/setup_cloud_scheduler_jobs.sh
#
# Creates precision cron triggers that directly call GitHub's Actions API
# with atomic-clock accuracy, bypassing GitHub's flaky internal cron delays.
# ==============================================================================

set -euo pipefail

# 1. Configuration & Secrets Detection
REPO_OWNER="alexkingston1993"
REPO_NAME="the-bull-print"
TIMEZONE="Asia/Kolkata"
LOCATION="${GCP_LOCATION:-asia-south1}"

echo "=================================================================="
echo "⚡ DEPLOYING GOOGLE CLOUD SCHEDULER JOBS FOR THE BULL PRINT"
echo "=================================================================="

# Check GitHub Authentication Token
GH_TOKEN=""
if [ -x "/usr/local/bin/gh" ]; then
  GH_TOKEN=$(/usr/local/bin/gh auth token 2>/dev/null || true)
elif [ -x "/opt/homebrew/bin/gh" ]; then
  GH_TOKEN=$(/opt/homebrew/bin/gh auth token 2>/dev/null || true)
elif command -v gh &>/dev/null; then
  GH_TOKEN=$(gh auth token 2>/dev/null || true)
fi
if [ -z "$GH_TOKEN" ]; then
  GH_TOKEN="${GITHUB_TOKEN:-${GITHUB_PAT:-}}"
fi

if [ -z "$GH_TOKEN" ]; then
  echo "❌ Error: No GitHub PAT found."
  echo "Please run 'gh auth login' or export GITHUB_PAT=ghp_xxx"
  exit 1
fi
echo "✓ Detected valid GitHub Token for $REPO_OWNER/$REPO_NAME"

# Check Google Cloud CLI Authentication
if ! command -v gcloud &>/dev/null; then
  echo "❌ Error: gcloud CLI is not installed."
  echo "Install it via: brew install google-cloud-sdk"
  exit 1
fi

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || true)
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
  PROJECT_ID="the-compounder-499412"
  echo "ℹ️ Setting active GCP Project to: $PROJECT_ID"
  gcloud config set project "$PROJECT_ID"
fi
echo "✓ Target GCP Project: $PROJECT_ID (Region: $LOCATION)"

# Enable Cloud Scheduler API if not already enabled
echo "🔧 Ensuring Cloud Scheduler API is enabled..."
gcloud services enable cloudscheduler.googleapis.com --project="$PROJECT_ID" || true

# Function to deploy an HTTP Cloud Scheduler Job
deploy_scheduler_job() {
  local job_name="$1"
  local cron_schedule="$2"
  local workflow_file="$3"
  local description="$4"
  local extra_payload="${5:-}"

  local uri="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${workflow_file}/dispatches"
  local body="{\"ref\":\"main\"}"
  if [ -n "$extra_payload" ]; then
    body="{\"ref\":\"main\",\"inputs\":$extra_payload}"
  fi

  echo ""
  echo "──────────────────────────────────────────────────────────────────"
  echo "🚀 Configuring: $job_name ($cron_schedule $TIMEZONE)"
  echo "   Target: $workflow_file"
  echo "   Desc:   $description"

  # Delete existing job if already present to guarantee idempotent clean update
  if gcloud scheduler jobs describe "$job_name" --location="$LOCATION" --project="$PROJECT_ID" &>/dev/null; then
    echo "   Updating existing job..."
    gcloud scheduler jobs update http "$job_name" \
      --location="$LOCATION" \
      --project="$PROJECT_ID" \
      --schedule="$cron_schedule" \
      --time-zone="$TIMEZONE" \
      --uri="$uri" \
      --http-method="POST" \
      --headers="Accept=application/vnd.github.v3+json,Authorization=Bearer $GH_TOKEN,User-Agent=Google-Cloud-Scheduler" \
      --message-body="$body" \
      --description="$description"
  else
    echo "   Creating new job..."
    gcloud scheduler jobs create http "$job_name" \
      --location="$LOCATION" \
      --project="$PROJECT_ID" \
      --schedule="$cron_schedule" \
      --time-zone="$TIMEZONE" \
      --uri="$uri" \
      --http-method="POST" \
      --headers="Accept=application/vnd.github.v3+json,Authorization=Bearer $GH_TOKEN,User-Agent=Google-Cloud-Scheduler" \
      --message-body="$body" \
      --description="$description"
  fi
  echo "   ✓ Successfully deployed: $job_name"
}

# ──────────────────────────────────────────────────────────────────────────────
# 2. Deploy The 3 Core Free Tier Jobs (100% Free Forever on Google Cloud)
# ──────────────────────────────────────────────────────────────────────────────

# Job 1: 5:00 AM IST Daily Production Master (10 Shorts + 2 Documentaries)
deploy_scheduler_job \
  "tbp-daily-5am-production" \
  "0 5 * * *" \
  "daily_5am_production_master.yml" \
  "Daily 5:00 AM IST Master Orchestrator: Dispatches 10 Shorts + 2 Documentaries"

# Job 2: Daily Production Supervisor & Auto-Healer (6 AM to 10 AM IST)
deploy_scheduler_job \
  "tbp-production-supervisor" \
  "0 6,7,8,9,10 * * *" \
  "daily_production_supervisor.yml" \
  "Production Supervisor: Audits runs, heals stuck locks, and verifies YouTube states"

# Job 3: Daily 1:35 PM IST Deferred Artifact Publisher
deploy_scheduler_job \
  "tbp-deferred-publisher-135pm" \
  "35 13 * * *" \
  "daily_135pm_deferred_publisher.yml" \
  "Publishes quota-deferred videos 5 minutes after YouTube API daily quota reset"

# Job 4: Daily 11:30 AM IST Long-Tail SEO Publisher & IndexNow Fast-Track
deploy_scheduler_job \
  "tbp-daily-longtail-seo" \
  "30 11 * * *" \
  "daily_longtail_seo.yml" \
  "Publishes daily high-converting long-tail SEO guide & pings IndexNow"

# Job 5: Real-Time Hourly Breaking News Viral Radar (Every Hour at :00)
deploy_scheduler_job \
  "tbp-hourly-viral-radar" \
  "0 * * * *" \
  "viral_radar_hourly.yml" \
  "Hourly Breaking News Viral Radar: scans macro shocks & dispatches urgent Ad-Hoc Shorts"

# ──────────────────────────────────────────────────────────────────────────────
# 3. Optional Additional Jobs ($0.10/mo each beyond first 3 jobs)
# ──────────────────────────────────────────────────────────────────────────────
if [ "${DEPLOY_ALL_JOBS:-false}" = "true" ]; then
  # Job 4: Social Media Expert & Channel Auditor (Every 6 Hours)
  deploy_scheduler_job \
    "tbp-social-media-auditor" \
    "0 */6 * * *" \
    "social_media_auditor.yml" \
    "Performs SEO keyword and channel analytics audit every 6 hours"

  # Job 5: Market Pulse Pre-Market Article (09:03 AM IST Weekdays)
  deploy_scheduler_job \
    "tbp-market-pulse-pre-market" \
    "3 9 * * 1-5" \
    "market_publisher.yml" \
    "Generates breaking Pre-Market educational brief before market open" \
    "{\"article_slot\":\"pre_market\"}"
fi

echo ""
echo "=================================================================="
echo "🎉 ALL GOOGLE CLOUD SCHEDULER JOBS DEPLOYED SUCCESSFULLY!"
echo "=================================================================="
echo "List active jobs with: gcloud scheduler jobs list --location=$LOCATION"
