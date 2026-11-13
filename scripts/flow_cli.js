#!/usr/bin/env node
/**
 * Google Flow Standalone CLI Generator
 * Usage:
 *   node scripts/flow_cli.js --prompt "..." --output "output/shorts/short03_cut09.jpg" --ratio "9:16"
 *   node scripts/flow_cli.js --batch output/shorts/shorts_3s_master_spec.json --short short_03
 */

import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const PROFILE_DIR = path.resolve(ROOT_DIR, '.gflow/profiles/default');
const CDP_PORT = 9225;
const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// Dynamically resolve Playwright from tools/google-flow-mcp
let chromium;
try {
  const pw = await import(path.resolve(ROOT_DIR, 'tools/google-flow-mcp/node_modules/playwright/index.mjs'));
  chromium = pw.chromium;
} catch (e) {
  const pw = await import('playwright');
  chromium = pw.chromium;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    prompt: null,
    output: null,
    ratio: '9:16',
    batch: null,
    short: null,
    launchOnly: false,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) options.prompt = args[++i];
    else if (args[i] === '--output' && args[i + 1]) options.output = args[++i];
    else if (args[i] === '--ratio' && args[i + 1]) options.ratio = args[++i];
    else if (args[i] === '--batch' && args[i + 1]) options.batch = args[++i];
    else if (args[i] === '--short' && args[i + 1]) options.short = args[++i];
    else if (args[i] === '--launch-only') options.launchOnly = true;
    else if (args[i] === '--help' || args[i] === '-h') options.help = true;
  }
  return options;
}

async function ensureChrome() {
  // Check if Chrome is already answering on CDP_PORT
  try {
    const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`);
    if (res.ok) {
      console.log(`[Flow CLI] Chrome already running on port ${CDP_PORT}`);
      return;
    }
  } catch (e) {}

  console.log(`[Flow CLI] Launching dedicated Chrome with profile: ${PROFILE_DIR}`);
  fs.mkdirSync(PROFILE_DIR, { recursive: true });

  // Clean stale locks
  const lock = path.join(PROFILE_DIR, 'SingletonLock');
  if (fs.existsSync(lock)) fs.rmSync(lock, { force: true });

  const args = [
    `--remote-debugging-port=${CDP_PORT}`,
    `--user-data-dir=${PROFILE_DIR}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-blink-features=AutomationControlled',
    'https://flow.google.com/'
  ];

  const cp = spawn(CHROME_PATH, args, { detached: true, stdio: 'ignore' });
  cp.unref();

  // Wait for CDP to respond
  let connected = false;
  for (let attempt = 0; attempt < 25; attempt++) {
    await new Promise(r => setTimeout(r, 600));
    try {
      const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`);
      if (res.ok) {
        connected = true;
        break;
      }
    } catch (e) {}
  }

  if (!connected) {
    throw new Error(`[Flow CLI] Timed out waiting for Chrome to start on port ${CDP_PORT}`);
  }
  console.log(`[Flow CLI] Chrome connected on CDP port ${CDP_PORT}`);
}

async function getFlowPage(browser) {
  const context = browser.contexts()[0] || await browser.newContext();
  let pages = context.pages();
  let page = pages.find(p => p.url().includes('flow.google.com') || p.url().includes('labs.google'));

  if (!page) {
    page = await context.newPage();
    console.log('[Flow CLI] Navigating to https://flow.google.com/ ...');
    await page.goto('https://flow.google.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  }

  return page;
}

async function generateSingleImage(page, prompt, outputPath, ratio = '9:16') {
  console.log(`\n[Flow CLI] >>> Generating Image`);
  console.log(`[Flow CLI] Prompt: "${prompt}"`);
  console.log(`[Flow CLI] Target: ${outputPath} (Ratio: ${ratio})`);

  // Ensure on Flow workspace
  const curUrl = page.url();
  if (curUrl.includes('accounts.google.com')) {
    console.log('\n======================================================');
    console.log('⚠️ GOOGLE SIGN-IN REQUIRED:');
    console.log('Please sign in to your Google Account in the open Chrome window.');
    console.log('Once signed in, rerun this command.');
    console.log('======================================================\n');
    return false;
  }

  // Navigate to main workspace if on /about
  if (curUrl.includes('/about')) {
    const createBtn = page.locator('text="Create with Google Flow"').first();
    if (await createBtn.isVisible().catch(() => false)) {
      await createBtn.click();
      await page.waitForTimeout(3000);
    }
  }

  // Find prompt input box
  const inputSelectors = [
    'div[contenteditable="true"]',
    'textarea',
    'input[type="text"]',
    '[role="textbox"]'
  ];

  let promptInput = null;
  for (const sel of inputSelectors) {
    const loc = page.locator(sel).first();
    if (await loc.isVisible().catch(() => false)) {
      promptInput = loc;
      break;
    }
  }

  if (!promptInput) {
    console.log('[Flow CLI] ⚠️ Prompt input not immediately visible. Capturing screenshot...');
    const dbgPath = path.resolve(ROOT_DIR, 'output/flow_debug.png');
    await page.screenshot({ path: dbgPath });
    console.log(`[Flow CLI] Screenshot saved to ${dbgPath}`);
    return false;
  }

  // Capture baseline image URLs
  const baselineSrcs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img')).map(i => i.src).filter(Boolean);
  });

  // Type prompt
  await promptInput.click();
  await page.keyboard.press('Meta+A');
  await page.keyboard.press('Backspace');
  await promptInput.fill(prompt);
  await page.waitForTimeout(400);

  // Trigger submission (Enter or button)
  const submitBtn = page.locator('button:has(:text-is("arrow_forward")), button[type="submit"]').first();
  if (await submitBtn.isVisible().catch(() => false)) {
    await submitBtn.click();
  } else {
    await page.keyboard.press('Enter');
  }

  console.log('[Flow CLI] Prompt submitted. Waiting for generation to complete...');

  // Poll for newly rendered image
  let newImgUrl = null;
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(2000);
    newImgUrl = await page.evaluate((baselines) => {
      const allImgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(Boolean);
      for (const src of allImgs) {
        if (!baselines.includes(src) && (src.includes('/asb/') || src.includes('getMediaUrlRedirect') || src.includes('googleusercontent.com') || src.startsWith('blob:'))) {
          return src;
        }
      }
      return null;
    }, baselineSrcs);

    if (newImgUrl) {
      console.log(`[Flow CLI] Generation completed! Found image: ${newImgUrl.slice(0, 60)}...`);
      break;
    }
    process.stdout.write('.');
  }
  console.log('');

  if (!newImgUrl) {
    console.log('[Flow CLI] Timed out waiting for image element. Check output/flow_debug.png');
    await page.screenshot({ path: path.resolve(ROOT_DIR, 'output/flow_debug.png') });
    return false;
  }

  // Download high-resolution image directly via browser session
  const highResUrl = newImgUrl.replace(/=s\d+(-[a-z]+)?$/, '=s2048-rw');
  const outDir = path.dirname(path.resolve(ROOT_DIR, outputPath));
  fs.mkdirSync(outDir, { recursive: true });

  const base64Data = await page.evaluate(async (url) => {
    const resp = await fetch(url);
    const blob = await resp.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const b64 = (reader.result || '').split(',')[1];
        resolve(b64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }, highResUrl);

  if (!base64Data) {
    console.error('[Flow CLI] Failed to retrieve image base64 data');
    return false;
  }

  fs.writeFileSync(path.resolve(ROOT_DIR, outputPath), Buffer.from(base64Data, 'base64'));
  console.log(`[Flow CLI] ✅ High-Res 2048px Image successfully saved to: ${outputPath}`);
  return true;
}

async function main() {
  const opts = parseArgs();

  if (opts.help) {
    console.log(`
Google Flow Standalone CLI
Commands:
  node scripts/flow_cli.js --launch-only
  node scripts/flow_cli.js --prompt "..." --output "output/shorts/my_plate.jpg" [--ratio 9:16]
  node scripts/flow_cli.js --batch output/shorts/shorts_3s_master_spec.json --short short_03
    `);
    process.exit(0);
  }

  await ensureChrome();

  if (opts.launchOnly) {
    console.log('[Flow CLI] Chrome launched. Log in to Google Flow in the browser.');
    process.exit(0);
  }

  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${CDP_PORT}`);
  const page = await getFlowPage(browser);

  if (opts.prompt && opts.output) {
    const ok = await generateSingleImage(page, opts.prompt, opts.output, opts.ratio);
    process.exit(ok ? 0 : 1);
  } else if (opts.batch && opts.short) {
    const spec = JSON.parse(fs.readFileSync(path.resolve(ROOT_DIR, opts.batch), 'utf8'));
    const shortData = spec[opts.short];
    if (!shortData) {
      console.error(`Short "${opts.short}" not found in ${opts.batch}`);
      process.exit(1);
    }
    console.log(`[Flow CLI] Processing batch for ${opts.short} (${shortData.cuts.length} cuts)...`);
    for (const cut of shortData.cuts) {
      const outPath = `output/shorts/plates/${opts.short}_cut_${String(cut.cut_idx).padStart(2, '0')}.jpg`;
      if (fs.existsSync(path.resolve(ROOT_DIR, outPath))) {
        console.log(`[Flow CLI] Cut ${cut.cut_idx} already exists: ${outPath}. Skipping.`);
        continue;
      }
      const ok = await generateSingleImage(page, cut.prompt, outPath, '9:16');
      if (!ok) {
        console.error(`[Flow CLI] Failed on cut ${cut.cut_idx}.`);
        break;
      }
    }
  } else {
    console.log('No action specified. Run with --help for options.');
  }
}

main().catch(err => {
  console.error('[Flow CLI Error]:', err.message);
  process.exit(1);
});
