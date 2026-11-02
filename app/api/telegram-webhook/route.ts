import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const TG_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '';
const AUTH_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '';
const GH_REPO = process.env.GITHUB_REPO || 'alexkingston1993/the-bull-print';
const GH_TOKEN = process.env.GITHUB_PAT_TOKEN || process.env.GITHUB_TOKEN || '';

async function sendTelegram(chatId: number | string, text: string, replyMarkup?: object) {
  if (!TG_TOKEN) return;
  await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      parse_mode: 'Markdown',
      reply_markup: replyMarkup,
      disable_web_page_preview: false,
    }),
  });
}

async function answerCallbackQuery(callbackQueryId: string, text?: string) {
  if (!TG_TOKEN) return;
  await fetch(`https://api.telegram.org/bot${TG_TOKEN}/answerCallbackQuery`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      callback_query_id: callbackQueryId,
      text: text || 'Command received!',
    }),
  });
}

async function dispatchGitHubEvent(eventType: string, clientPayload: object = {}) {
  if (!GH_TOKEN) {
    return { ok: false, status: 401, text: () => Promise.resolve('Missing GITHUB_TOKEN') };
  }
  return fetch(`https://api.github.com/repos/${GH_REPO}/dispatches`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${GH_TOKEN}`,
      Accept: 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'TheBullPrint-Telegram-Webhook',
    },
    body: JSON.stringify({ event_type: eventType, client_payload: clientPayload }),
  });
}

// =====================================================================
// 🧠 AGENT ARIA NATURAL LANGUAGE AI BRAIN (Zero Slash Commands Needed)
// =====================================================================
interface AriaParsedIntent {
  intent: 'create_short' | 'create_video' | 'check_status' | 'check_revenue' | 'check_quota' | 'heal_pipeline' | 'chat';
  topic: string;
  vertical: 'stock_market' | 'crypto' | 'insurance';
  duration: number; // 36|60 for shorts; 3|5|10 for standard videos
  aria_reply: string;
}

const RAW_GEMINI_KEYS = (process.env.GEMINI_API_KEY || process.env.GEMINI_API_KEYS || '')
  .split(',')
  .map((k) => k.trim())
  .filter(Boolean);

const CANDIDATE_GEMINI_MODELS = [
  process.env.GEMINI_MODEL_NAME,
  'gemini-flash-lite-latest',
  'gemini-flash-latest',
  'gemini-2.5-flash',
].filter(Boolean);

async function parseNaturalLanguageWithAriaBrain(userText: string): Promise<AriaParsedIntent> {
  const lower = userText.toLowerCase().trim();

  // Fast heuristic shortcuts for instant response when keywords match unequivocally
  if (['/revenue', '/clicks', 'revenue', 'clicks', 'affiliate', 'how much revenue', 'revenue today'].includes(lower)) {
    return { intent: 'check_revenue', topic: '', vertical: 'stock_market', duration: 0, aria_reply: 'Pulling the live affiliate & revenue ledger now! 💰' };
  }
  if (['/ytquota', '/quota', 'quota', 'yt quota', 'quota slots', 'how many uploads left'].includes(lower)) {
    return { intent: 'check_quota', topic: '', vertical: 'stock_market', duration: 0, aria_reply: 'Auditing YouTube Quota Rotator pool capacity! 🔑' };
  }
  if (['/status', '/diagnose', '/health', 'status', 'diagnose', 'health', 'pipeline status', 'are runners working'].includes(lower)) {
    return { intent: 'check_status', topic: '', vertical: 'stock_market', duration: 0, aria_reply: 'Scanning live GitHub Actions runner telemetry! 🛰️' };
  }
  if (['/heal', '/fix', 'heal', 'fix pipeline', 'unstick pipeline'].includes(lower)) {
    return { intent: 'heal_pipeline', topic: '', vertical: 'stock_market', duration: 0, aria_reply: 'Autonomous doctor dispatched to inspect and heal cloud runners! 🩺' };
  }

  // LLM Intent Prompt
  const prompt = `You are Agent Aria, Chief of Staff and Operations Lead for 'The Bull Print' media company.
Alex (the creator and owner) communicates with you in natural English. No slash commands are ever required from him.

ALEX'S MESSAGE: "${userText}"

Analyze Alex's message and determine his objective. Return STRICT JSON with no markdown wrapping or extra keys:
{
  "intent": "create_short" | "create_video" | "check_status" | "check_revenue" | "check_quota" | "heal_pipeline" | "chat",
  "topic": "<descriptive financial topic if creating video/short, else empty>",
  "vertical": "stock_market" | "crypto" | "insurance",
  "duration": <number: 36 or 60 for shorts, 3 or 5 or 10 for standard videos>,
  "aria_reply": "<Aria's authentic response to Alex. In-character, sharp, witty, adjustments of dark sunglasses, coffee sip, professional. If dispatching video/short, mention that you're running it across our 20-runner parallel cloud matrix on GitHub Actions with zero load on his Mac.>"
}

Rules for Intent & Duration:
- If he mentions "short", "60s", "36s", "reel", or quick video: intent="create_short". Duration=36 or 60 (default 60).
- If he mentions "video", "masterclass", "long video", "deep dive", or minutes (3, 5, 10): intent="create_video". Duration=3, 5, or 10 (default 3).
- If he asks about clicks, earnings, affiliates, revenue: intent="check_revenue".
- If he asks about status, runs, health: intent="check_status".
- If he asks about quotas or YouTube tokens: intent="check_quota".
- If he asks to fix or heal: intent="heal_pipeline".
- Otherwise: intent="chat".`;

  // 1. Try Gemini API
  for (const key of RAW_GEMINI_KEYS) {
    for (const model of CANDIDATE_GEMINI_MODELS) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { responseMimeType: 'application/json' },
          }),
        });
        if (res.ok) {
          const data = await res.json();
          const rawJson = data?.candidates?.[0]?.content?.parts?.[0]?.text;
          if (rawJson) {
            const parsed = JSON.parse(rawJson);
            if (parsed.intent) return parsed;
          }
        }
      } catch {
        // Continue failover
      }
    }
  }

  // 2. Try Pollinations AI Failover
  try {
    const pollRes = await fetch('https://text.pollinations.ai/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: prompt }],
        model: 'openai-fast',
        jsonMode: true,
      }),
    });
    if (pollRes.ok) {
      const text = await pollRes.text();
      const match = text.match(/\{[\s\S]*\}/);
      if (match) {
        const parsed = JSON.parse(match[0]);
        if (parsed.intent) return parsed;
      }
    }
  } catch {
    // Continue fallback
  }

  // 3. Deterministic Heuristic Fallback
  let intent: AriaParsedIntent['intent'] = 'chat';
  let vertical: AriaParsedIntent['vertical'] = 'stock_market';
  let duration = 60;
  let topic = userText;

  if (lower.includes('crypto') || lower.includes('solana') || lower.includes('bitcoin') || lower.includes('btc') || lower.includes('eth')) {
    vertical = 'crypto';
  } else if (lower.includes('insurance') || lower.includes('claim') || lower.includes('health') || lower.includes('irdai')) {
    vertical = 'insurance';
  }

  if (lower.includes('short') || lower.includes('reel') || lower.includes('36s') || lower.includes('60s')) {
    intent = 'create_short';
    duration = lower.includes('36') ? 36 : 60;
    topic = userText.replace(/\b(short|create|make|generate|a|60s|36s|video|please|for me)\b/gi, '').trim();
  } else if (lower.includes('video') || lower.includes('masterclass') || lower.includes('deep dive') || lower.includes('min')) {
    intent = 'create_video';
    const minMatch = lower.match(/\b(3|5|10)\b/);
    duration = minMatch ? parseInt(minMatch[1]) : 3;
    topic = userText.replace(/\b(video|create|make|generate|masterclass|deep dive|min|minute|minutes|please)\b/gi, '').trim();
  }

  return {
    intent,
    topic: topic || (intent === 'create_short' ? 'Bitcoin Perpetual Squeeze' : 'Institutional Order Flow Footprint'),
    vertical,
    duration,
    aria_reply:
      intent === 'chat'
        ? "*Adjusts dark sunglasses and sips double espresso* 🕶️☕ On station, Boss! All cloud systems are green and 100% cloud-hosted. What are we producing or analyzing next?"
        : `Dispatched to cloud matrix! Zero load on your Mac. 🚀`,
  };
}

// =====================================================================
// 💰 AFFILIATE & REVENUE LEDGER HELPERS (Zero-DB GitHub Repo Variables)
// =====================================================================
interface TelemetryShape {
  total_clicks: number;
  brokers: Record<string, number>;
  campaigns: Record<string, number>;
  updated_at: string;
}

function blankTelemetry(): TelemetryShape {
  return { total_clicks: 0, brokers: {}, campaigns: {}, updated_at: '' };
}

async function fetchAffiliateTelemetry(): Promise<TelemetryShape> {
  let data = blankTelemetry();
  if (!GH_TOKEN) return data;
  try {
    const res = await fetch(`https://api.github.com/repos/${GH_REPO}/actions/variables/AFFILIATE_TELEMETRY_JSON`, {
      headers: { Authorization: `Bearer ${GH_TOKEN}`, Accept: 'application/vnd.github+json', 'User-Agent': 'TheBullPrint-Telegram-Webhook' },
    });
    if (res.status === 404) return data; // Ledger not created yet
    if (res.ok) {
      const raw = (await res.json()).value;
      data = { ...blankTelemetry(), ...JSON.parse(raw) };
    }
  } catch {
    // Silent zero ledger on any network failure.
  }
  return data;
}

async function fetchPostStats(): Promise<{ total: number; last7: number }> {
  const stats = { total: 0, last7: 0 };
  try {
    const res = await fetch('https://the-bull-print.vercel.app/content/posts.json', { cache: 'no-store' });
    if (!res.ok) return stats;
    let posts: any = await res.json();
    if (!Array.isArray(posts)) posts = posts?.posts || [];
    stats.total = posts.length;
    const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    for (const p of posts) {
      const date = Date.parse(p?.date || p?.published || p?.created_at || '');
      if (!Number.isNaN(date) && date >= weekAgo) stats.last7 += 1;
    }
  } catch {
    // Silent zero stats on any fetch failure.
  }
  return stats;
}

function buildRevenueLedgerCard(t: TelemetryShape, content: { total: number; last7: number }): string {
  const brokerOrder: Array<[string, string]> = [
    ['tradingview', 'TradingView'],
    ['gocharting', 'GoCharting'],
    ['zerodha', 'Zerodha'],
    ['delta', 'Delta'],
    ['bybit', 'Bybit'],
  ];
  const total = Number(t.total_clicks || 0);
  const breakdown = brokerOrder.map(([key, label]) => `${label}: \`${t.brokers?.[key] || 0}\``).join(' | ');
  const estReferrals = total * 0.04; // 4% conversion assumption
  const projectedInr = estReferrals * 500; // blended INR kickback/month
  const updatedAt = (t.updated_at || '—').replace('T', ' ').split('.')[0];

  return (
    `💰 *THE BULL PRINT — AFFILIATE & REVENUE LEDGER* 🐂\n` +
    `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
    `🖱️ *Total Affiliate Clicks:* \`${total}\`\n` +
    `📊 *Breakdown by Broker:* ${breakdown}\n` +
    `🎓 *Published Research Dossiers:* \`${content.total}\` (+${content.last7} this week)\n` +
    `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
    `📈 *Est. Active Referrals* (4% CVR): \`${estReferrals.toFixed(1)}\`\n` +
    `₹ *Projected Monthly Recurring RevShare:* \`₹${projectedInr.toLocaleString('en-IN', { maximumFractionDigits: 0 })}\`\n` +
    `🕒 *Ledger Updated:* \`${updatedAt}\`\n` +
    `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
    `💡 *Verdict:* Every YouTube description fires \`/go/{broker}\` — keep publishing articles and the flywheel compounds! ☕🚀`
  );
}

async function handleRevenueCommand(chatId: number | string) {
  const [t, content] = await Promise.all([fetchAffiliateTelemetry(), fetchPostStats()]);
  await sendTelegram(chatId, buildRevenueLedgerCard(t, content));
}

function buildYtQuotaCard(): string {
  // The only slot Vercel reliably holds is YT_OAUTH_POOL_JSON (provisioned via
  // scripts/provision_yt_pool_cli.py). Everything else is cloud-managed.
  let slots: any[] = [];
  let poolSources: string[] = [];
  try {
    const raw = process.env.YT_OAUTH_POOL_JSON || '';
    if (raw) {
      const parsed = JSON.parse(raw);
      slots = Array.isArray(parsed) ? parsed : [parsed];
      poolSources = slots.map(
        (s: any) => `▫️ \`pool.json (ends …${String(s.client_id || '').slice(-14)})\``
      );
    }
  } catch {
    /* malformed pool json — report empty */
  }
  for (let i = 1; i <= 6; i++) {
    if (process.env[`YT_CLIENT_ID_${i}`] && process.env[`YT_REFRESH_TOKEN_${i}`]) {
      const cid = process.env[`YT_CLIENT_ID_${i}`]!;
      poolSources.push(`▫️ \`env YT_CLIENT_ID_${i} (ends …${cid.slice(-14)})\``);
    }
  }

  const n = poolSources.length;
  const capacity = n * 6; // 10,000 units/day ÷ 1,650 units per upload ≈ 6 videos/day/slot
  const dailyTarget = 16; // 6 Long-Form + 10 Shorts across stock×2 / crypto×2 / insurance×2
  const neededSlots = Math.ceil(dailyTarget / 6); // 3 slots minimum for the full cadence
  const lines = [
    '🔑 *AGENT ARIA: YT QUOTA ROTATOR STATUS* ⛽⚡',
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    `🧩 *Active OAuth Slots:* \`${n}\` project slot(s)`,
    ...poolSources,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    `📊 *Daily Upload Capacity:* \`≈ ${capacity}/16 videos\` (${n} × 6 → target ${dailyTarget}: 6 Long + 10 Shorts)`,
    'ℹ️ *Math:* 10,000 quota units/day/project ÷ 1,650 units per upload',
  ];
  if (n === 0) {
    lines.push('⚠️ *No pool detected on Vercel* (run scripts/provision_yt_pool_cli.py --sync)');
  } else if (n < neededSlots) {
    lines.push(
      `🚨 *DEFICIT:* the 16-video/day cadence needs \`3\` slots (16 × 1,650 = 26,400 units) but only \`${n}\` armed — run scripts/provision_yt_pool_cli.py --bootstrap ta to add projects`
    );
  } else {
    lines.push('🚀 *Rotation:* quotaExceeded on Slot #N auto-fails over to Slot #N+1 mid-upload');
  }
  lines.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  lines.push('🛡️ *Verdict:* ' + (n >= neededSlots ? 'duplicate-proof & quota-rotated 🐂' : `\`${n}/3 slots\` — self-rotates, cadence ceiling ≈ ${capacity}`));
  return lines.join('\n');
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // 1. HANDLE INLINE BUTTON CALLBACKS (One-Tap Self-Healing, Rerun, Slot Dispatch)
    if (body.callback_query) {
      const cb = body.callback_query;
      const chatId = cb.message?.chat?.id;
      const data: string = cb.data || '';

      if (AUTH_CHAT_ID && String(chatId) !== String(AUTH_CHAT_ID)) {
        await answerCallbackQuery(cb.id, 'Unauthorized');
        return NextResponse.json({ ok: true, status: 'unauthorized_ignored' });
      }

      if (data === 'view_revenue') {
        await answerCallbackQuery(cb.id, 'Pulling the Revenue Ledger... 💰');
        await handleRevenueCommand(chatId);
        return NextResponse.json({ ok: true, handler: 'view_revenue' });
      }

      if (data === 'view_yt_quota') {
        await answerCallbackQuery(cb.id, 'Auditing YouTube Quota Slots... 🔑');
        await sendTelegram(chatId, buildYtQuotaCard());
        return NextResponse.json({ ok: true, handler: 'view_yt_quota' });
      }

      await answerCallbackQuery(cb.id, 'Engaging Agent Aria...');

      if (data.startsWith('rerun_failed:')) {
        const runId = data.split(':')[1];
        const rerunRes = await fetch(`https://api.github.com/repos/${GH_REPO}/actions/runs/${runId}/rerun-failed-jobs`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${GH_TOKEN}`,
            Accept: 'application/vnd.github.v3+json',
          },
        });
        if (rerunRes.ok) {
          await sendTelegram(chatId, `🔄 *Agent Aria:* Successfully re-dispatched failed jobs for Workflow Run \`#${runId}\`! Telemetry monitoring active. ☕🚀`);
        } else {
          await sendTelegram(chatId, `⚠️ *Agent Aria:* GitHub Actions re-run notice (HTTP ${rerunRes.status}).`);
        }
      } else if (data.startsWith('run_slot:')) {
        const slot = data.split(':')[1];
        const ghRes = await dispatchGitHubEvent('trigger_media_engine', { topic: slot, mode: 'slot_override' });
        if (ghRes.ok) {
          await sendTelegram(chatId, `🚀 *Agent Aria:* Dispatched market cycle for \`${slot}\` to GitHub Actions cloud runner!`);
        } else {
          await sendTelegram(chatId, `⚠️ *Agent Aria:* Failed to dispatch workflow (HTTP ${ghRes.status}).`);
        }
      }

      return NextResponse.json({ ok: true });
    }

    // 2. HANDLE SLASH COMMANDS SERVERLESSLY ON VERCEL
    const msg = body?.message;
    const text: string = (msg?.text || '').trim();
    const chatId = msg?.chat?.id;

    if (!chatId || (AUTH_CHAT_ID && String(chatId) !== String(AUTH_CHAT_ID))) {
      return NextResponse.json({ ok: true, status: 'unauthorized_ignored' });
    }

    const lower = text.toLowerCase();

    // Command: /status, /diagnose, or /health
    if (['/status', '/diagnose', '/health', 'status', 'diagnose'].includes(lower)) {
      if (!GH_TOKEN) {
        await sendTelegram(chatId, '⚠️ *Agent Aria:* `GITHUB_PAT_TOKEN` is not configured on Vercel.');
        return NextResponse.json({ ok: true });
      }

      const runsRes = await fetch(`https://api.github.com/repos/${GH_REPO}/actions/runs?per_page=3`, {
        headers: {
          Authorization: `Bearer ${GH_TOKEN}`,
          Accept: 'application/vnd.github.v3+json',
        },
      });

      if (!runsRes.ok) {
        await sendTelegram(chatId, `⚠️ *Agent Aria:* Could not reach GitHub API (HTTP ${runsRes.status}).`);
        return NextResponse.json({ ok: true });
      }

      const runsData = await runsRes.json();
      const latest = runsData.workflow_runs?.[0];

      if (!latest) {
        await sendTelegram(chatId, '🔍 *Agent Aria:* No recent workflow runs found in repository.');
        return NextResponse.json({ ok: true });
      }

      const statusEmoji = latest.conclusion === 'success' ? '✅' : latest.conclusion === 'failure' ? '💥' : '⏳';
      const conclusionText = latest.conclusion || latest.status || 'in_progress';
      
      const report =
        `🛰️ *AGENT ARIA — LIVE CLOUD TELEMETRY* 🕶️☕\n` +
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
        `${statusEmoji} *Latest Workflow:* \`${latest.name}\`\n` +
        `⚡ *Run ID:* \`#${latest.id}\` (\`${conclusionText.toUpperCase()}\`)\n` +
        `📅 *Triggered Via:* \`${latest.event}\` at \`${latest.updated_at.replace('T', ' ').replace('Z', ' UTC')}\`\n` +
        `🌐 *Web Portal:* \`https://the-bull-print.vercel.app\`\n` +
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;

      const inlineKeyboard =
        latest.conclusion === 'failure'
          ? {
              inline_keyboard: [
                [{ text: '🔄 Re-Run Failed Jobs', callback_data: `rerun_failed:${latest.id}` },
                  { text: '🩹 Force Clean Rebuild', callback_data: 'run_slot:Institutional Order Flow & Macro Liquidity' },
                ],
                [{ text: '💰 Revenue & Clicks', callback_data: 'view_revenue' },
                  { text: '🔑 YT Quota', callback_data: 'view_yt_quota' }],
              ],
            }
          : {
              inline_keyboard: [
                [
                  { text: '🌅 Pre-Market Brief', callback_data: 'run_slot:Pre-Market Morning Brief & Global Liquidity' },
                  { text: '🔔 Closing Bell', callback_data: 'run_slot:Closing Bell Institutional Absorption' },
                ],
                [
                  { text: '🎓 Weekend Masterclass', callback_data: 'run_slot:Weekend Wealth & Market Structure Masterclass' },
                  { text: '💰 Revenue & Clicks', callback_data: 'view_revenue' },
                ],
                [{ text: '🔑 YT Quota Slot Capacity', callback_data: 'view_yt_quota' }],
              ],
            };

      await sendTelegram(chatId, report, inlineKeyboard);
    // 3. NATURAL LANGUAGE AI BRAIN & AUTOMATED INTENT DISPATCH
    // Alex speaks exclusively in natural English. Aria detects intent, extracts parameters,
    // triggers parallel cloud matrix pipelines (zero local Mac compute), and replies conversationally.
    const parsed = await parseNaturalLanguageWithAriaBrain(text);

    if (parsed.intent === 'create_short') {
      const topic = parsed.topic || 'Solana Memecoin Siphon & MEV Arbitrage Squeeze';
      const duration = parsed.duration || 60;
      const vertical = parsed.vertical || 'crypto';

      const ghRes = await dispatchGitHubEvent('trigger_parallel_video', {
        topic,
        shorts_only: 'true',
        shorts_count: '1',
        duration_sec: String(duration),
        vertical,
        parallel_matrix: 'true',
        max_parallel_runners: '20',
        mode: 'aria_natural_language_dispatch',
      });

      // Also trigger legacy event name as backup
      await dispatchGitHubEvent('trigger_media_engine', {
        topic,
        shorts_only: 'true',
        shorts_count: '1',
        duration_sec: String(duration),
        vertical,
        parallel_matrix: 'true',
        max_parallel_runners: '20',
        mode: 'aria_natural_language_dispatch',
      });

      const confirmation = parsed.aria_reply ||
        `🕶️☕ *Agent Aria on Station:*\n\n` +
        `Dispatched **${duration}s 9:16 Short** to our **20-Runner Parallel Cloud Matrix** on GitHub Actions!\n` +
        `📌 *Topic:* \`${topic}\`\n` +
        `🏛️ *Vertical:* \`${vertical}\`\n` +
        `⚡ *Parallel Execution:* All 6-second segments rendering simultaneously across parallel Ubuntu cloud runners (+ Kaggle GPU overflow).\n` +
        `🛡️ *Local Host:* Your Mac is 100% untouchable and untouched. All execution is cloud-native.\n\n` +
        `I'll notify you the moment the assembled video, ducked audio bed, and web article go live! 🚀`;

      await sendTelegram(chatId, confirmation);
      return NextResponse.json({ ok: true, intent: 'create_short', topic, duration, vertical, dispatched: ghRes.ok });
    }

    if (parsed.intent === 'create_video') {
      const topic = parsed.topic || 'Institutional Order Flow Absorption & Macro Liquidity';
      const duration = parsed.duration || 3;
      const vertical = parsed.vertical || 'stock_market';

      const ghRes = await dispatchGitHubEvent('trigger_parallel_video', {
        topic,
        vertical,
        duration_min: String(duration),
        shorts_only: 'false',
        parallel_matrix: 'true',
        max_parallel_runners: '20',
        mode: 'aria_natural_language_dispatch',
      });

      // Also trigger legacy event name as backup
      await dispatchGitHubEvent('trigger_media_engine', {
        topic,
        vertical,
        duration_min: String(duration),
        shorts_only: 'false',
        parallel_matrix: 'true',
        max_parallel_runners: '20',
        mode: 'aria_natural_language_dispatch',
      });

      const confirmation = parsed.aria_reply ||
        `🕶️☕ *Agent Aria on Station:*\n\n` +
        `Dispatched **${duration}-Minute 2K Masterclass** to our **20-Runner Parallel Cloud Matrix** on GitHub Actions!\n` +
        `📌 *Topic:* \`${topic}\`\n` +
        `🏛️ *Vertical:* \`${vertical}\`\n` +
        `🎨 *Specs:* High-CTR Flow AI thumbnail frames, Method C Glass HUD callouts, and 2,500+ word WebP companion article.\n` +
        `⚡ *Parallel Concurrency:* Segments rendered concurrently across up to 20 Ubuntu runners + Kaggle GPU.\n` +
        `🛡️ *Local Host:* Zero load on your Mac; 100% cloud execution.\n\n` +
        `Monitoring telemetry now, Captain! 🚀`;

      await sendTelegram(chatId, confirmation);
      return NextResponse.json({ ok: true, intent: 'create_video', topic, duration, vertical, dispatched: ghRes.ok });
    }

    if (parsed.intent === 'check_revenue') {
      await handleRevenueCommand(chatId);
      return NextResponse.json({ ok: true, intent: 'check_revenue' });
    }

    if (parsed.intent === 'check_quota') {
      await sendTelegram(chatId, buildYtQuotaCard());
      return NextResponse.json({ ok: true, intent: 'check_quota' });
    }

    if (parsed.intent === 'check_status') {
      const runsRes = await fetch(`https://api.github.com/repos/${GH_REPO}/actions/runs?per_page=3`, {
        headers: { Authorization: `Bearer ${GH_TOKEN}`, Accept: 'application/vnd.github.v3+json' },
      });
      if (runsRes.ok) {
        const runsData = await runsRes.json();
        const latest = runsData.workflow_runs?.[0];
        const statusEmoji = latest?.conclusion === 'success' ? '✅' : latest?.conclusion === 'failure' ? '💥' : '⏳';
        const report =
          `🛰️ *AGENT ARIA — LIVE CLOUD TELEMETRY* 🕶️☕\n` +
          `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n` +
          `${statusEmoji} *Latest Workflow:* \`${latest?.name || 'Cloud Media Engine'}\`\n` +
          `⚡ *Run ID:* \`#${latest?.id || 'N/A'}\` (\`${(latest?.conclusion || latest?.status || 'RUNNING').toUpperCase()}\`)\n` +
          `📅 *Triggered:* \`${(latest?.updated_at || '').replace('T', ' ').replace('Z', ' UTC')}\`\n` +
          `🌐 *Web Portal:* \`https://the-bull-print.vercel.app\`\n` +
          `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n` +
          (parsed.aria_reply || 'All cloud runners active and standing by.');
        await sendTelegram(chatId, report);
      } else {
        await sendTelegram(chatId, parsed.aria_reply || 'Checking telemetry... all cloud runners standing by.');
      }
      return NextResponse.json({ ok: true, intent: 'check_status' });
    }

    if (parsed.intent === 'heal_pipeline') {
      const ghRes = await dispatchGitHubEvent('heal_pipeline', { mode: 'watchdog_heal' });
      await sendTelegram(
        chatId,
        parsed.aria_reply ||
          `🩺 *Agent Aria:* Dispatched Autonomous Pipeline Healer to cloud runners! Diagnosing failed runs and clearing state. ☕🚀`
      );
      return NextResponse.json({ ok: true, intent: 'heal_pipeline' });
    }

    // Default: Conversational chat with Aria's persona
    await sendTelegram(chatId, parsed.aria_reply);
    return NextResponse.json({ ok: true, intent: 'chat' });
  } catch (err: any) {
    return NextResponse.json({ ok: false, error: err?.message || 'Unknown error' }, { status: 500 });
  }
}
