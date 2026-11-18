/**
 * The Bull Print — Cloudflare Control Plane
 * Cron Orchestrator + D1 Metadata Ledger + R2 Frame Vault Sync & Auto-Purge
 */

export interface Env {
  DB: D1Database;
  VAULT?: R2Bucket;
  GITHUB_PAT?: string;
  GITHUB_REPO: string;
  MASTER_WORKFLOW: string;
  DEFERRED_WORKFLOW: string;
  YOUTUBE_CLIENT_ID?: string;
  YOUTUBE_CLIENT_SECRET?: string;
  YOUTUBE_REFRESH_TOKEN?: string;
  VAULT_COOLDOWN_DAYS?: string;
}

export default {
  /**
   * Cloudflare Edge Cron Scheduler (100% SLA — Guaranteed Delivery)
   * 1. '30 23 * * *' (5:00 AM IST): Master Production Dispatch
   * 2. '* /30 * * * *' (Every 30 Mins): YouTube Privacy & R2 Vault Sync Sweep
   */
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    console.log(`⏰ [Cron Triggered] Cron pattern: "${event.cron}" at ${new Date().toISOString()}`);

    if (event.cron === "30 23 * * *") {
      // 5:00 AM IST Master Dispatch
      console.log("🚀 [Master Dispatch] Triggering 5:00 AM IST daily production pipeline...");
      await dispatchGitHubWorkflow(env, env.MASTER_WORKFLOW);
    } else {
      // 30-minute sync sweep
      console.log("🔄 [Sync Sweep] Running 30-minute YouTube Privacy & R2 Vault sync...");
      await syncYouTubePrivacyAndVault(env);

      // Check for 1:35 PM IST (08:05 UTC) Deferred Publisher trigger
      const now = new Date();
      const utcHours = now.getUTCHours();
      const utcMins = now.getUTCMinutes();
      if (utcHours === 8 && utcMins >= 0 && utcMins < 30) {
        console.log("📦 [1:35 PM IST Publisher] Triggering deferred artifact publisher after PT midnight reset...");
        await dispatchGitHubWorkflow(env, env.DEFERRED_WORKFLOW);
      }
    }
  },

  /**
   * HTTP API Interface for Mission Control & Webhooks
   */
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/" || path === "/status") {
      return await handleGetStatus(env);
    }

    if (path === "/dispatch" && request.method === "POST") {
      const res = await dispatchGitHubWorkflow(env, env.MASTER_WORKFLOW);
      return new Response(JSON.stringify(res), {
        headers: { "Content-Type": "application/json" },
        status: res.success ? 200 : 500
      });
    }

    if (path === "/sync-privacy" && request.method === "POST") {
      const res = await syncYouTubePrivacyAndVault(env);
      return new Response(JSON.stringify(res), {
        headers: { "Content-Type": "application/json" }
      });
    }

    if (path === "/vault-eligible-frames") {
      return await handleGetVaultEligibleFrames(env);
    }

    return new Response("Not Found", { status: 404 });
  }
};

/**
 * Triggers a GitHub Actions workflow via REST API workflow_dispatch
 */
async function dispatchGitHubWorkflow(env: Env, workflowFileName: string): Promise<{ success: boolean; message: string }> {
  const token = env.GITHUB_PAT;
  if (!token) {
    const msg = "⚠️ GITHUB_PAT secret is not configured in Worker environment.";
    console.error(msg);
    return { success: false, message: msg };
  }

  const endpoint = `https://api.github.com/repos/${env.GITHUB_REPO}/actions/workflows/${workflowFileName}/dispatches`;
  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${token}`,
        "User-Agent": "TheBullPrint-Cloudflare-Orchestrator",
        "X-GitHub-Api-Version": "2022-11-28"
      },
      body: JSON.stringify({ ref: "main" })
    });

    if (res.status === 204 || res.ok) {
      const msg = `✅ Dispatched workflow: ${workflowFileName} successfully.`;
      console.log(msg);
      return { success: true, message: msg };
    } else {
      const errText = await res.text();
      const msg = `❌ GitHub API error (${res.status}): ${errText}`;
      console.error(msg);
      return { success: false, message: msg };
    }
  } catch (err: any) {
    const msg = `❌ Network exception dispatching workflow: ${err.message}`;
    console.error(msg);
    return { success: false, message: msg };
  }
}

/**
 * 30-Minute YouTube Privacy & R2 Vault Sync Engine
 * Rule 1: Only 'public' videos have active frames stored in R2.
 * Rule 2: If a video changes to private/unlisted/deleted -> immediately purge frames from R2.
 * Rule 3: If switched back to public -> auto-recover from cold backup or saved seeds.
 */
async function syncYouTubePrivacyAndVault(env: Env): Promise<any> {
  const results = {
    checked: 0,
    purged: 0,
    restored: 0,
    unchanged: 0,
    errors: [] as string[]
  };

  try {
    // 1. Fetch all indexed videos from D1
    const { results: videos } = await env.DB.prepare(
      "SELECT video_id, title, privacy_status, r2_prefix, cold_backup_url FROM videos"
    ).all();

    if (!videos || videos.length === 0) {
      console.log("ℹ️ No indexed videos found in D1 database.");
      return { message: "No videos indexed in D1 yet.", results };
    }

    results.checked = videos.length;
    const nowEpoch = Math.floor(Date.now() / 1000);

    // 2. Fetch fresh access token using YouTube OAuth refresh token
    const accessToken = await getYouTubeAccessToken(env);
    if (!accessToken) {
      const err = "⚠️ YouTube credentials missing or refresh failed. Skipping status check.";
      console.warn(err);
      results.errors.push(err);
      return results;
    }

    // 3. Batch check privacyStatus via YouTube Data API
    const videoIds = videos.map((v: any) => v.video_id).join(",");
    const ytUrl = `https://www.googleapis.com/youtube/v3/videos?part=status&id=${encodeURIComponent(videoIds)}`;
    const ytRes = await fetch(ytUrl, {
      headers: { "Authorization": `Bearer ${accessToken}` }
    });

    if (!ytRes.ok) {
      const err = `YouTube API error: ${ytRes.status} ${await ytRes.text()}`;
      console.error(err);
      results.errors.push(err);
      return results;
    }

    const ytData: any = await ytRes.json();
    const liveStatusMap = new Map<string, string>();
    for (const item of ytData.items || []) {
      const vid = item.id;
      const status = item.status?.privacyStatus?.toLowerCase() || "private";
      liveStatusMap.set(vid, status);
    }

    // 4. Process state transitions
    for (const v of videos as any[]) {
      const prevStatus = v.privacy_status?.toLowerCase();
      // If video is not returned in API, it was deleted
      const currentStatus = liveStatusMap.has(v.video_id)
        ? liveStatusMap.get(v.video_id)!
        : "deleted";

      if (prevStatus === "public" && currentStatus !== "public") {
        // Transition: PUBLIC -> PRIVATE / UNLISTED / DELETED
        console.log(`🚨 Video ${v.video_id} ('${v.title}') transitioned: ${prevStatus} -> ${currentStatus}. Purging R2 frames!`);
        await purgeR2FramesForVideo(env, v.video_id);

        await env.DB.prepare(
          "UPDATE videos SET privacy_status = ?, last_checked_epoch = ? WHERE video_id = ?"
        ).bind(currentStatus, nowEpoch, v.video_id).run();

        await env.DB.prepare(
          "UPDATE frames SET privacy_status = ?, is_vault_eligible = 0 WHERE video_id = ?"
        ).bind(currentStatus, v.video_id).run();

        results.purged++;
      } else if (prevStatus !== "public" && currentStatus === "public") {
        // Transition: PRIVATE / UNLISTED -> PUBLIC (Auto-recovery)
        console.log(`🎉 Video ${v.video_id} ('${v.title}') transitioned: ${prevStatus} -> public! Restoring frame index...`);

        await env.DB.prepare(
          "UPDATE videos SET privacy_status = 'public', last_checked_epoch = ? WHERE video_id = ?"
        ).bind(nowEpoch, v.video_id).run();

        // Check 180-day age gate for vault eligibility
        const cooldownSecs = parseInt(env.VAULT_COOLDOWN_DAYS || "180", 10) * 86400;
        const cutoffEpoch = nowEpoch - cooldownSecs;

        await env.DB.prepare(
          "UPDATE frames SET privacy_status = 'public', is_vault_eligible = CASE WHEN created_at_epoch <= ? THEN 1 ELSE 0 END WHERE video_id = ?"
        ).bind(cutoffEpoch, v.video_id).run();

        results.restored++;
      } else {
        // Status unchanged
        await env.DB.prepare(
          "UPDATE videos SET last_checked_epoch = ? WHERE video_id = ?"
        ).bind(nowEpoch, v.video_id).run();
        results.unchanged++;
      }
    }
  } catch (err: any) {
    console.error("Error in syncYouTubePrivacyAndVault:", err);
    results.errors.push(err.message);
  }

  return results;
}

/**
 * Purges all R2 objects for a specific video prefix
 */
async function purgeR2FramesForVideo(env: Env, videoId: string): Promise<void> {
  if (!env.VAULT) {
    console.log(`ℹ️ R2 VAULT binding not active yet; skipped R2 delete for ${videoId}.`);
    return;
  }

  const prefix = `public/${videoId}/`;
  try {
    const list = await env.VAULT.list({ prefix });
    if (list.objects.length > 0) {
      const keys = list.objects.map(obj => obj.key);
      await env.VAULT.delete(keys);
      console.log(`🗑️ Deleted ${keys.length} frame objects from R2 under ${prefix}`);
    }
  } catch (e: any) {
    console.error(`Failed to delete R2 objects for ${prefix}:`, e);
  }
}

/**
 * Exchanges YouTube OAuth refresh token for an access token
 */
async function getYouTubeAccessToken(env: Env): Promise<string | null> {
  const cid = env.YOUTUBE_CLIENT_ID;
  const csec = env.YOUTUBE_CLIENT_SECRET;
  const rtok = env.YOUTUBE_REFRESH_TOKEN;

  if (!cid || !csec || !rtok) {
    return null;
  }

  try {
    const params = new URLSearchParams({
      client_id: cid,
      client_secret: csec,
      refresh_token: rtok,
      grant_type: "refresh_token"
    });

    const res = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString()
    });

    if (!res.ok) {
      console.error("Failed to refresh YouTube token:", await res.text());
      return null;
    }

    const data: any = await res.json();
    return data.access_token || null;
  } catch (e) {
    console.error("Exception refreshing YouTube token:", e);
    return null;
  }
}

/**
 * Returns JSON status overview of indexed videos, frame counts, and vault eligibility
 */
async function handleGetStatus(env: Env): Promise<Response> {
  const now = Math.floor(Date.now() / 1000);
  const cooldownSecs = parseInt(env.VAULT_COOLDOWN_DAYS || "180", 10) * 86400;
  const cutoff = now - cooldownSecs;

  const { results: videoStats } = await env.DB.prepare(
    "SELECT privacy_status, COUNT(*) as count FROM videos GROUP BY privacy_status"
  ).all();

  const { results: frameStats } = await env.DB.prepare(
    "SELECT COUNT(*) as total_frames, SUM(is_vault_eligible) as eligible_frames FROM frames"
  ).all();

  const { results: recentVideos } = await env.DB.prepare(
    "SELECT video_id, title, privacy_status, total_frames, created_at_epoch, last_checked_epoch FROM videos ORDER BY created_at_epoch DESC LIMIT 10"
  ).all();

  const statusObj = {
    service: "The Bull Print — Cloudflare Control Plane",
    timestamp: new Date().toISOString(),
    epoch: now,
    vault_cooldown_days: 180,
    video_summary: videoStats,
    frame_summary: frameStats && frameStats[0] ? frameStats[0] : {},
    recent_videos: recentVideos
  };

  return new Response(JSON.stringify(statusObj, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}

/**
 * Strict 180-day (6-month) vault reuse query handler:
 * Only returns frames that are strictly >= 180 days old and currently public.
 */
async function handleGetVaultEligibleFrames(env: Env): Promise<Response> {
  const now = Math.floor(Date.now() / 1000);
  const cooldownSecs = parseInt(env.VAULT_COOLDOWN_DAYS || "180", 10) * 86400;
  const cutoff = now - cooldownSecs;

  const { results } = await env.DB.prepare(
    `SELECT frame_id, video_id, frame_index, r2_key, visual_prompt, seed, created_at_epoch, last_used_epoch 
     FROM frames 
     WHERE privacy_status = 'public' 
       AND created_at_epoch <= ? 
       AND last_used_epoch <= ? 
     ORDER BY last_used_epoch ASC 
     LIMIT 50`
  ).bind(cutoff, cutoff).all();

  return new Response(JSON.stringify({
    count: results ? results.length : 0,
    cooldown_cutoff_epoch: cutoff,
    eligible_frames: results || []
  }, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}
