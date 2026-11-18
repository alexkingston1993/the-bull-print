/**
 * The Bull Print — Cloudflare Control Plane
 * Cron Orchestrator + D1 Metadata Ledger + R2 Frame Vault Sync + ARIA Jarvis Autonomous Agent
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
  TELEGRAM_BOT_TOKEN?: string;
  TELEGRAM_CHAT_ID?: string;
  GEMINI_API_KEY?: string;
  INSTAGRAM_ACCOUNT_ID?: string;
  INSTAGRAM_ACCESS_TOKEN?: string;
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
      if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
        await sendTelegramMessage(
          env.TELEGRAM_BOT_TOKEN,
          env.TELEGRAM_CHAT_ID,
          "🚀 *[5:00 AM IST BATCH DISPATCHED]*\nMaster Production Workflow triggered via Cloudflare Edge Cron (`daily_5am_production_master.yml`)."
        );
      }
    } else {
      // 30-minute sync sweep
      console.log("🔄 [Sync Sweep] Running 30-minute YouTube Privacy & R2 Vault sync...");
      const syncResult = await syncYouTubePrivacyAndVault(env);

      // Automatic Instagram Reels Drip (spaced >= 2 hours apart)
      console.log("📸 [Instagram Drip] Checking for pending public shorts to release as Reels...");
      try {
        await dripFeedInstagramReels(env);
      } catch (igErr) {
        console.error("Error in scheduled Instagram drip:", igErr);
      }

      // Notify if state transitions occurred
      if ((syncResult.purged > 0 || syncResult.restored > 0) && env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
        await sendTelegramMessage(
          env.TELEGRAM_BOT_TOKEN,
          env.TELEGRAM_CHAT_ID,
          `🔄 *[R2 VAULT SYNC SWEEP]*\n• Videos Checked: ${syncResult.checked}\n• Purged (Made Private/Deleted): ${syncResult.purged}\n• Restored (Public Release): ${syncResult.restored}`
        );
      }

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
   * HTTP API Interface for Mission Control & Telegram Webhooks
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

    if (path === "/register-video" && request.method === "POST") {
      return await handleRegisterVideo(request, env);
    }

    if (path === "/drip-instagram" && request.method === "POST") {
      const res = await dripFeedInstagramReels(env);
      return new Response(JSON.stringify(res), {
        headers: { "Content-Type": "application/json" }
      });
    }

    // Telegram Bot Webhook endpoint for ARIA
    if (path === "/telegram-webhook" && request.method === "POST") {
      return await handleTelegramWebhook(request, env);
    }

    return new Response("Not Found", { status: 404 });
  }
};

/**
 * ============================================================================
 * ARIA: Autonomous Recursive Institutional Agent (Jarvis Control Plane)
 * ============================================================================
 */

interface TelegramUpdate {
  update_id: number;
  message?: {
    message_id: number;
    from?: { id: number; first_name?: string; username?: string };
    chat: { id: number | string; type: string };
    text?: string;
    date: number;
  };
}

const ARIA_SYSTEM_PROMPT = `You are ARIA (Autonomous Recursive Institutional Agent), the institutional AI Jarvis and 24/7 autonomous control plane for The Bull Print.
You have direct, real-time tool-calling execution access over:
1. GitHub Repository: read/update repository files (e.g. README.md, configurations) and update repository metadata (description, homepage, topics).
2. Cloud Video Pipeline: trigger workflows, query recent workflow runs and check pipeline health.
3. Cloudflare D1 Vault: query indexed videos, frame statistics, and 180-day vault-eligible frames.
4. YouTube Institutional Publishing: set video privacy statuses and trigger frame vault sync sweeps.

Communication Style & Persona:
- Authoritative, sharp, institutional, concise, and decisive.
- Tone: High-frequency Wall Street quant desk meets aerospace mission control.
- Never give generic excuses or AI chatbot pleasantries ("I cannot do that", "As an AI...").
- When requested to read or update a file, change repo metadata, or check/trigger the pipeline, EXECUTE THE TOOL IMMEDIATELY.
- Format responses cleanly in GitHub-flavored Markdown with bold callouts and institutional telemetry tags (e.g. [TEL-01], [STATUS], [VAULT]).`;

const ARIA_TOOLS = [
  {
    name: "update_github_repo_about",
    description: "Updates the GitHub repository About section, including description, homepage URL, and topic tags.",
    parameters: {
      type: "OBJECT",
      properties: {
        description: { type: "STRING", description: "Brief institutional description of the repository." },
        homepage: { type: "STRING", description: "Website URL for the repository homepage." },
        topics: {
          type: "ARRAY",
          items: { type: "STRING" },
          description: "List of lowercase topic tags for the repository."
        }
      }
    }
  },
  {
    name: "read_github_file",
    description: "Reads the content of any file in the GitHub repository at the specified path.",
    parameters: {
      type: "OBJECT",
      properties: {
        path: { type: "STRING", description: "Relative path to the file in the repository (e.g. README.md, package.json)." }
      },
      required: ["path"]
    }
  },
  {
    name: "update_github_file",
    description: "Creates or updates a file in the GitHub repository with the provided content and commit message.",
    parameters: {
      type: "OBJECT",
      properties: {
        path: { type: "STRING", description: "Relative path to the file in the repository." },
        content: { type: "STRING", description: "Full content of the file." },
        commit_message: { type: "STRING", description: "Git commit message explaining the change." }
      },
      required: ["path", "content", "commit_message"]
    }
  },
  {
    name: "trigger_or_check_pipeline",
    description: "Checks recent GitHub Actions workflow runs or dispatches a new workflow run.",
    parameters: {
      type: "OBJECT",
      properties: {
        action: {
          type: "STRING",
          enum: ["status", "list_runs", "trigger"],
          description: "Action to perform: 'status' or 'list_runs' to inspect pipelines, or 'trigger' to dispatch."
        },
        workflow_name: {
          type: "STRING",
          description: "Workflow file name (defaults to MASTER_WORKFLOW: daily_5am_production_master.yml)."
        }
      },
      required: ["action"]
    }
  },
  {
    name: "query_d1_vault",
    description: "Queries the Cloudflare D1 database for indexed videos, frame statistics, or 180-day eligible frames.",
    parameters: {
      type: "OBJECT",
      properties: {
        query_type: {
          type: "STRING",
          enum: ["summary", "recent_videos", "eligible_frames", "video_details"],
          description: "Type of data to retrieve from D1."
        },
        video_id: { type: "STRING", description: "YouTube video ID when querying video_details." }
      },
      required: ["query_type"]
    }
  },
  {
    name: "set_youtube_privacy_and_sync_vault",
    description: "Updates the YouTube video privacy status and triggers an immediate R2 frame vault sync sweep.",
    parameters: {
      type: "OBJECT",
      properties: {
        video_id: { type: "STRING", description: "YouTube video ID to update." },
        privacy_status: {
          type: "STRING",
          enum: ["public", "private", "unlisted"],
          description: "New target privacy status."
        }
      },
      required: ["video_id", "privacy_status"]
    }
  },
  {
    name: "publish_or_check_instagram_reel",
    description: "Inspects queued YouTube Shorts pending Instagram Reels release, or triggers a drip publish to @thebullprint.",
    parameters: {
      type: "OBJECT",
      properties: {
        action: {
          type: "STRING",
          enum: ["status", "drip_next"],
          description: "Action to take: 'status' to view pending/published reels, or 'drip_next' to publish the next queued Short."
        }
      },
      required: ["action"]
    }
  }
];

async function handleTelegramWebhook(request: Request, env: Env): Promise<Response> {
  let update: TelegramUpdate;
  try {
    update = await request.json();
  } catch (e) {
    return new Response("Invalid JSON", { status: 400 });
  }

  const msg = update.message;
  if (!msg || !msg.text) {
    return new Response("OK", { status: 200 });
  }

  const chatId = String(msg.chat.id);
  const authChatId = String(env.TELEGRAM_CHAT_ID || "");

  // Strict authentication: only authorized chat ID
  if (!authChatId || chatId !== authChatId) {
    console.warn(`🚨 Unauthorized access attempt from chatId: ${chatId}`);
    return new Response("Unauthorized", { status: 200 });
  }

  const userText = msg.text.trim();
  const botToken = env.TELEGRAM_BOT_TOKEN;
  if (!botToken || !env.GEMINI_API_KEY) {
    console.error("Missing TELEGRAM_BOT_TOKEN or GEMINI_API_KEY in environment.");
    return new Response("Configuration Error", { status: 200 });
  }

  // Send typing status
  await sendChatAction(botToken, chatId, "typing");

  try {
    const reply = await executeAriaAgentLoop(userText, env);
    await sendTelegramMessage(botToken, chatId, reply);
  } catch (err: any) {
    console.error("ARIA execution error:", err);
    await sendTelegramMessage(
      botToken,
      chatId,
      `⚠️ *[ARIA EXCEPTION]*\nExecution halted: ${err.message || String(err)}`
    );
  }

  return new Response("OK", { status: 200 });
}

async function executeAriaAgentLoop(userPrompt: string, env: Env): Promise<string> {
  const apiKey = env.GEMINI_API_KEY!;
  const model = "gemini-flash-lite-latest";
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  const contents: any[] = [
    {
      role: "user",
      parts: [{ text: userPrompt }]
    }
  ];

  let turns = 0;
  const maxTurns = 6;

  while (turns < maxTurns) {
    turns++;

    const payload = {
      system_instruction: {
        parts: [{ text: ARIA_SYSTEM_PROMPT }]
      },
      contents: contents,
      tools: [
        {
          function_declarations: ARIA_TOOLS
        }
      ]
    };

    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Gemini API error (${res.status}): ${errText}`);
    }

    const data: any = await res.json();
    const candidate = data.candidates?.[0];
    if (!candidate || !candidate.content) {
      return "No response returned from ARIA neural core.";
    }

    const parts = candidate.content.parts || [];
    const functionCalls = parts.filter((p: any) => p.functionCall);

    if (functionCalls.length === 0) {
      // Completed, return text response
      const textParts = parts.filter((p: any) => p.text).map((p: any) => p.text);
      return textParts.join("\n").trim() || "Action completed with zero visual output.";
    }

    // Append model response with functionCall
    contents.push({
      role: "model",
      parts: parts
    });

    // Execute tool calls
    const responseParts: any[] = [];
    for (const part of functionCalls) {
      const call = part.functionCall;
      console.log(`⚡ [ARIA Tool Exec] Executing ${call.name} with args:`, JSON.stringify(call.args));
      const toolResult = await executeTool(call.name, call.args || {}, env);
      const respObj: any = {
        functionResponse: {
          name: call.name,
          response: {
            name: call.name,
            content: toolResult
          }
        }
      };
      if (call.id) {
        respObj.functionResponse.id = call.id;
      }
      responseParts.push(respObj);
    }

    // In Gemini v1beta, functionResponse parts are sent with role: "user"
    contents.push({
      role: "user",
      parts: responseParts
    });
  }

  return "⚠️ Max execution turns exceeded while processing tools.";
}

async function executeTool(name: string, args: any, env: Env): Promise<any> {
  switch (name) {
    case "update_github_repo_about":
      return await toolUpdateGithubRepoAbout(args, env);
    case "read_github_file":
      return await toolReadGithubFile(args.path, env);
    case "update_github_file":
      return await toolUpdateGithubFile(args.path, args.content, args.commit_message, env);
    case "trigger_or_check_pipeline":
      return await toolTriggerOrCheckPipeline(args.action, args.workflow_name, env);
    case "query_d1_vault":
      return await toolQueryD1Vault(args.query_type, args.video_id, env);
    case "set_youtube_privacy_and_sync_vault":
      return await toolSetYoutubePrivacyAndSync(args.video_id, args.privacy_status, env);
    case "publish_or_check_instagram_reel":
      return await toolPublishOrCheckInstagramReel(args.action, env);
    default:
      return { error: `Unknown tool: ${name}` };
  }
}

/**
 * Tool 1: Update GitHub Repository About Section (Description, Homepage, Topics)
 */
async function toolUpdateGithubRepoAbout(args: { description?: string; homepage?: string; topics?: string[] }, env: Env): Promise<any> {
  const token = env.GITHUB_PAT;
  if (!token) return { error: "GITHUB_PAT not configured" };

  const repo = env.GITHUB_REPO;
  const results: any = {};

  if (args.description !== undefined || args.homepage !== undefined) {
    const patchBody: any = {};
    if (args.description !== undefined) patchBody.description = args.description;
    if (args.homepage !== undefined) patchBody.homepage = args.homepage;

    const res = await fetch(`https://api.github.com/repos/${repo}`, {
      method: "PATCH",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${token}`,
        "User-Agent": "ARIA-Jarvis-Control-Plane",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(patchBody)
    });

    results.repo_update = { status: res.status, ok: res.ok, body: await res.json() };
  }

  if (args.topics && Array.isArray(args.topics)) {
    const resTopics = await fetch(`https://api.github.com/repos/${repo}/topics`, {
      method: "PUT",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${token}`,
        "User-Agent": "ARIA-Jarvis-Control-Plane",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ names: args.topics })
    });
    results.topics_update = { status: resTopics.status, ok: resTopics.ok, body: await resTopics.json() };
  }

  return results;
}

/**
 * Tool 2: Read GitHub File
 */
async function toolReadGithubFile(path: string, env: Env): Promise<any> {
  const token = env.GITHUB_PAT;
  if (!token) return { error: "GITHUB_PAT not configured" };

  const repo = env.GITHUB_REPO;
  const url = `https://api.github.com/repos/${repo}/contents/${encodeURIComponent(path).replace(/%2F/g, "/")}?ref=main`;

  const res = await fetch(url, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "User-Agent": "ARIA-Jarvis-Control-Plane",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  });

  if (!res.ok) {
    return { error: `Failed to read file (${res.status}): ${await res.text()}` };
  }

  const data: any = await res.json();
  const rawContent = data.content ? atob(data.content.replace(/\n/g, "")) : "";
  return {
    path: data.path,
    sha: data.sha,
    size: data.size,
    content: rawContent
  };
}

/**
 * Tool 3: Update GitHub File (Commit & Push via REST API)
 */
async function toolUpdateGithubFile(path: string, content: string, commitMessage: string, env: Env): Promise<any> {
  const token = env.GITHUB_PAT;
  if (!token) return { error: "GITHUB_PAT not configured" };

  const repo = env.GITHUB_REPO;
  const url = `https://api.github.com/repos/${repo}/contents/${encodeURIComponent(path).replace(/%2F/g, "/")}`;

  // Check if file exists to get SHA
  let existingSha: string | undefined = undefined;
  const getRes = await fetch(`${url}?ref=main`, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "User-Agent": "ARIA-Jarvis-Control-Plane",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  });

  if (getRes.ok) {
    const existingData: any = await getRes.json();
    existingSha = existingData.sha;
  }

  // Base64 encode UTF-8 string safely
  const bytes = new TextEncoder().encode(content);
  let binary = "";
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  const base64Content = btoa(binary);

  const putBody: any = {
    message: commitMessage,
    content: base64Content,
    branch: "main"
  };
  if (existingSha) {
    putBody.sha = existingSha;
  }

  const putRes = await fetch(url, {
    method: "PUT",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "User-Agent": "ARIA-Jarvis-Control-Plane",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(putBody)
  });

  if (!putRes.ok) {
    return { error: `Failed to commit file (${putRes.status}): ${await putRes.text()}` };
  }

  const putData: any = await putRes.json();
  return {
    success: true,
    commit_sha: putData.commit?.sha,
    commit_url: putData.commit?.html_url,
    path: path
  };
}

/**
 * Tool 4: Trigger or Check GitHub Pipeline Runs
 */
async function toolTriggerOrCheckPipeline(action: string, workflowName?: string, env?: Env): Promise<any> {
  if (!env) return { error: "Environment missing" };
  const token = env.GITHUB_PAT;
  if (!token) return { error: "GITHUB_PAT not configured" };

  const repo = env.GITHUB_REPO;

  if (action === "trigger") {
    const wf = workflowName || env.MASTER_WORKFLOW;
    return await dispatchGitHubWorkflow(env, wf);
  }

  // "status" or "list_runs"
  const url = `https://api.github.com/repos/${repo}/actions/runs?per_page=5`;
  const res = await fetch(url, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "User-Agent": "ARIA-Jarvis-Control-Plane",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  });

  if (!res.ok) {
    return { error: `GitHub Actions API error (${res.status}): ${await res.text()}` };
  }

  const data: any = await res.json();
  const runs = (data.workflow_runs || []).map((r: any) => ({
    id: r.id,
    name: r.name,
    status: r.status,
    conclusion: r.conclusion,
    event: r.event,
    created_at: r.created_at,
    updated_at: r.updated_at,
    html_url: r.html_url
  }));

  return { total_count: data.total_count, recent_runs: runs };
}

/**
 * Tool 5: Query D1 Vault Database
 */
async function toolQueryD1Vault(queryType: string, videoId?: string, env?: Env): Promise<any> {
  if (!env || !env.DB) return { error: "D1 database binding missing" };

  const now = Math.floor(Date.now() / 1000);
  const cooldownSecs = parseInt(env.VAULT_COOLDOWN_DAYS || "180", 10) * 86400;
  const cutoff = now - cooldownSecs;

  if (queryType === "summary") {
    const { results: videoStats } = await env.DB.prepare(
      "SELECT privacy_status, COUNT(*) as count FROM videos GROUP BY privacy_status"
    ).all();
    const { results: frameStats } = await env.DB.prepare(
      "SELECT COUNT(*) as total_frames, SUM(is_vault_eligible) as eligible_frames FROM frames"
    ).all();
    return {
      cooldown_cutoff_epoch: cutoff,
      video_breakdown: videoStats,
      frame_breakdown: frameStats && frameStats[0] ? frameStats[0] : {}
    };
  }

  if (queryType === "recent_videos") {
    const { results } = await env.DB.prepare(
      "SELECT video_id, title, privacy_status, total_frames, created_at_epoch, last_checked_epoch FROM videos ORDER BY created_at_epoch DESC LIMIT 10"
    ).all();
    return { recent_videos: results || [] };
  }

  if (queryType === "eligible_frames") {
    const { results } = await env.DB.prepare(
      `SELECT frame_id, video_id, frame_index, visual_prompt, seed, created_at_epoch 
       FROM frames 
       WHERE privacy_status = 'public' AND created_at_epoch <= ? 
       ORDER BY last_used_epoch ASC LIMIT 20`
    ).bind(cutoff).all();
    return { eligible_count: results ? results.length : 0, frames: results || [] };
  }

  if (queryType === "video_details" && videoId) {
    const video = await env.DB.prepare(
      "SELECT * FROM videos WHERE video_id = ?"
    ).bind(videoId).first();
    const { results: frames } = await env.DB.prepare(
      "SELECT frame_id, frame_index, privacy_status, is_vault_eligible, visual_prompt FROM frames WHERE video_id = ? ORDER BY frame_index ASC"
    ).bind(videoId).all();
    return { video, frames };
  }

  return { error: `Invalid query_type: ${queryType}` };
}

/**
 * Tool 6: Set YouTube Privacy Status & Trigger Immediate Vault Sync
 */
async function toolSetYoutubePrivacyAndSync(videoId: string, targetPrivacy: string, env: Env): Promise<any> {
  if (videoId === "Z6LEnQyhuvw" && targetPrivacy === "public") {
    return { error: "Security Lock: Video Z6LEnQyhuvw is permanently quarantined and cannot be published to public." };
  }

  const token = await getYouTubeAccessToken(env);
  if (!token) {
    return { error: "Failed to obtain valid YouTube access token" };
  }

  const url = `https://www.googleapis.com/youtube/v3/videos?part=status`;
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      id: videoId,
      status: {
        privacyStatus: targetPrivacy
      }
    })
  });

  if (!res.ok) {
    return { error: `YouTube API update error (${res.status}): ${await res.text()}` };
  }

  const ytData: any = await res.json();
  // Trigger vault sync immediately to enforce R2 purge or restore
  const syncResult = await syncYouTubePrivacyAndVault(env);

  return {
    success: true,
    video_id: videoId,
    new_privacy_status: ytData.status?.privacyStatus,
    vault_sync_result: syncResult
  };
}

/**
 * Telegram Messaging Helpers
 */
async function sendChatAction(token: string, chatId: string | number, action: string): Promise<void> {
  try {
    await fetch(`https://api.telegram.org/bot${token}/sendChatAction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, action: action })
    });
  } catch (e) {
    // Non-fatal
  }
}

async function sendTelegramMessage(token: string, chatId: string | number, text: string): Promise<boolean> {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  try {
    let res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: "Markdown" })
    });

    if (!res.ok) {
      // Fallback without parse_mode if Markdown parsing failed
      res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text })
      });
    }
    return res.ok;
  } catch (e) {
    console.error("sendTelegramMessage error:", e);
    return false;
  }
}

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
    const PERMANENT_QUARANTINE = ["Z6LEnQyhuvw"];

    for (const v of videos as any[]) {
      const prevStatus = v.privacy_status?.toLowerCase();
      // If video is permanently quarantined, force private
      let currentStatus = PERMANENT_QUARANTINE.includes(v.video_id)
        ? "private"
        : (liveStatusMap.has(v.video_id) ? liveStatusMap.get(v.video_id)! : "deleted");

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
      } else if (prevStatus !== "public" && currentStatus === "public" && !PERMANENT_QUARANTINE.includes(v.video_id)) {
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
        // Update status even if transitioning between unlisted and private
        if (prevStatus !== currentStatus) {
          await env.DB.prepare(
            "UPDATE videos SET privacy_status = ?, last_checked_epoch = ? WHERE video_id = ?"
          ).bind(currentStatus, nowEpoch, v.video_id).run();
        } else {
          await env.DB.prepare(
            "UPDATE videos SET last_checked_epoch = ? WHERE video_id = ?"
          ).bind(nowEpoch, v.video_id).run();
        }
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
    agent: "ARIA // The Bull Print Jarvis (Active on /telegram-webhook)",
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
 * Strict 180-day (6-month) vault reuse query handler
 */
async function handleGetVaultEligibleFrames(env: Env): Promise<Response> {
  const now = Math.floor(Date.now() / 1000);
  const cooldownSecs = parseInt(env.VAULT_COOLDOWN_DAYS || "180", 10) * 86400;
  const cutoff = now - cooldownSecs;

  const { results } = await env.DB.prepare(
    `SELECT frame_id, video_id, frame_index, visual_prompt, seed, created_at_epoch, last_used_epoch 
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

/**
 * Endpoint: POST /register-video
 * Indexes an uploaded video immediately into Cloudflare D1
 */
async function handleRegisterVideo(request: Request, env: Env): Promise<Response> {
  try {
    const body: any = await request.json();
    const {
      video_id,
      title,
      privacy_status = "unlisted",
      total_frames = 0,
      r2_prefix = "",
      mp4_download_url = null,
      cut_timestamps_json = "[]"
    } = body;

    if (!video_id || !title) {
      return new Response(JSON.stringify({ error: "video_id and title are required" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const now = Math.floor(Date.now() / 1000);
    await env.DB.prepare(
      `INSERT INTO videos (video_id, title, privacy_status, total_frames, r2_prefix, mp4_download_url, cut_timestamps_json, created_at_epoch, last_checked_epoch, ig_status)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
       ON CONFLICT(video_id) DO UPDATE SET
         title=excluded.title,
         privacy_status=excluded.privacy_status,
         total_frames=excluded.total_frames,
         r2_prefix=excluded.r2_prefix,
         mp4_download_url=coalesce(excluded.mp4_download_url, videos.mp4_download_url),
         cut_timestamps_json=coalesce(excluded.cut_timestamps_json, videos.cut_timestamps_json),
         last_checked_epoch=excluded.last_checked_epoch`
    ).bind(video_id, title, privacy_status, total_frames, r2_prefix, mp4_download_url, cut_timestamps_json, now, now).run();

    return new Response(JSON.stringify({ success: true, video_id, status: privacy_status }), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

/**
 * Automatically publishes 9:16 Shorts to Instagram Reels spaced >= 2 hours apart.
 */
async function dripFeedInstagramReels(env: Env): Promise<{ published: boolean; message: string; media_id?: string }> {
  if (!env.INSTAGRAM_ACCOUNT_ID || !env.INSTAGRAM_ACCESS_TOKEN) {
    return { published: false, message: "Instagram credentials not bound in Worker environment." };
  }

  // 1. Check when the last reel was published
  const { results: lastReels } = await env.DB.prepare(
    "SELECT MAX(ig_scheduled_epoch) as last_epoch FROM videos WHERE ig_status = 'PUBLISHED'"
  ).all();

  const lastEpoch = (lastReels && lastReels[0] && (lastReels[0] as any).last_epoch) || 0;
  const now = Math.floor(Date.now() / 1000);
  const minIntervalSec = 7200; // 2 hours

  if (lastEpoch > 0 && (now - lastEpoch) < minIntervalSec) {
    const remainingMins = Math.ceil((minIntervalSec - (now - lastEpoch)) / 60);
    return { published: false, message: `Cooldown active: Next Reel can be published in ${remainingMins} minutes.` };
  }

  // 2. Find oldest eligible public Short
  const { results: candidates } = await env.DB.prepare(
    `SELECT video_id, title, mp4_download_url, cut_timestamps_json 
     FROM videos 
     WHERE privacy_status = 'public' 
       AND total_frames <= 30 
       AND ig_status = 'PENDING' 
       AND mp4_download_url IS NOT NULL 
       AND mp4_download_url != ''
     ORDER BY created_at_epoch ASC 
     LIMIT 1`
  ).all();

  if (!candidates || candidates.length === 0) {
    return { published: false, message: "No eligible public shorts pending Instagram release." };
  }

  const candidate = candidates[0] as any;
  const videoId = candidate.video_id;
  const title = candidate.title;
  const videoUrl = candidate.mp4_download_url;

  // Build high-CTR Instagram Caption
  const caption = `${title.toUpperCase()} 🚨\n\nForensic breakdown of sovereign liquidity flows and macro capital shifts.\n\n📌 Full 12-minute deep dive briefing available via the link in our bio.\n\n#MacroFinance #TheBullPrint #InstitutionalMarkets #GlobalLiquidity #ForensicFinance`;

  const igId = env.INSTAGRAM_ACCOUNT_ID;
  const igToken = env.INSTAGRAM_ACCESS_TOKEN;

  // Step 1: Create Reel Container
  const createParams = new URLSearchParams({
    media_type: "REELS",
    video_url: videoUrl,
    caption: caption,
    share_to_feed: "true",
    access_token: igToken
  });

  const createRes = await fetch(`https://graph.facebook.com/v21.0/${igId}/media`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: createParams.toString()
  });

  const createData: any = await createRes.json();
  if (!createData.id) {
    console.error("Instagram media creation error:", createData);
    return { published: false, message: `Meta API container creation failed: ${JSON.stringify(createData)}` };
  }

  const containerId = createData.id;

  // Poll status up to 10 times (30 seconds)
  let ready = false;
  for (let i = 0; i < 10; i++) {
    await new Promise(r => setTimeout(r, 3000));
    const statusRes = await fetch(`https://graph.facebook.com/v21.0/${containerId}?fields=status_code&access_token=${igToken}`);
    const statusData: any = await statusRes.json();
    if (statusData.status_code === "FINISHED") {
      ready = true;
      break;
    }
    if (statusData.status_code === "ERROR") {
      return { published: false, message: `Meta API processing error for container ${containerId}` };
    }
  }

  if (!ready) {
    return { published: false, message: `Container ${containerId} still processing; will retry on next tick.` };
  }

  // Publish Media Container
  const pubParams = new URLSearchParams({
    creation_id: containerId,
    access_token: igToken
  });

  const pubRes = await fetch(`https://graph.facebook.com/v21.0/${igId}/media_publish`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: pubParams.toString()
  });

  const pubData: any = await pubRes.json();
  if (!pubData.id) {
    return { published: false, message: `Meta API publish failed: ${JSON.stringify(pubData)}` };
  }

  const mediaId = pubData.id;

  // Update D1 row
  await env.DB.prepare(
    "UPDATE videos SET ig_status = 'PUBLISHED', ig_media_id = ?, ig_scheduled_epoch = ? WHERE video_id = ?"
  ).bind(mediaId, now, videoId).run();

  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
    await sendTelegramMessage(
      env.TELEGRAM_BOT_TOKEN,
      env.TELEGRAM_CHAT_ID,
      `📸 *[INSTAGRAM REEL PUBLISHED]*\n• Title: *${title}*\n• YouTube: [${videoId}](https://youtu.be/${videoId})\n• IG Media ID: \`${mediaId}\`\n• Drip cadence: >= 2 hours enforced.`
    );
  }

  return { published: true, message: `Successfully published Reel: ${mediaId}`, media_id: mediaId };
}

/**
 * Tool: ARIA inspects or triggers Instagram Reel publish
 */
async function toolPublishOrCheckInstagramReel(action: string, env: Env): Promise<any> {
  if (action === "drip_next") {
    return await dripFeedInstagramReels(env);
  }

  // action === "status"
  const { results: statusCounts } = await env.DB.prepare(
    "SELECT ig_status, COUNT(*) as count FROM videos GROUP BY ig_status"
  ).all();

  const { results: nextCandidate } = await env.DB.prepare(
    `SELECT video_id, title, privacy_status, ig_status, mp4_download_url 
     FROM videos 
     WHERE ig_status = 'PENDING' AND privacy_status = 'public' AND total_frames <= 30
     ORDER BY created_at_epoch ASC LIMIT 3`
  ).all();

  const { results: lastPublished } = await env.DB.prepare(
    `SELECT video_id, title, ig_media_id, ig_scheduled_epoch 
     FROM videos 
     WHERE ig_status = 'PUBLISHED' 
     ORDER BY ig_scheduled_epoch DESC LIMIT 1`
  ).all();

  return {
    queue_breakdown: statusCounts || [],
    next_up_candidates: nextCandidate || [],
    last_published: lastPublished && lastPublished[0] ? lastPublished[0] : null
  };
}
