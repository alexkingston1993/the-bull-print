import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const pw = await import(path.resolve(ROOT_DIR, 'tools/google-flow-mcp/node_modules/playwright/index.mjs'));
const { chromium } = pw;

const DOC_CONFIGS = [
  {
    id: 'ai_bubble',
    folder: 'output/ai_bubble_documentary',
    title: 'Doc 01 - The $2.5 Trillion AI Bubble Panic',
    timingFile: 'output/ai_bubble_documentary/timing_and_timestamps.json',
    framesDir: 'output/ai_bubble_documentary/frames'
  },
  {
    id: 'fii_exodus',
    folder: 'output/fii_exodus_documentary',
    title: 'Doc 02 - The ₹14,900 Crore FII Capital Exodus',
    timingFile: 'output/fii_exodus_documentary/timing_and_timestamps.json',
    framesDir: 'output/fii_exodus_documentary/frames'
  },
  {
    id: 'nuclear_ai',
    folder: 'output/nuclear_ai_documentary',
    title: "Doc 03 - Big Tech's Nuclear Secret",
    timingFile: 'output/nuclear_ai_documentary/timing_and_timestamps.json',
    framesDir: 'output/nuclear_ai_documentary/frames'
  }
];

export async function runDocumentaryFlowProduction(targetDocId = null) {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9225');
  const context = browser.contexts()[0];
  let page = context.pages().find(p => p.url().includes('flow.google.com'));

  for (const doc of DOC_CONFIGS) {
    if (targetDocId && doc.id !== targetDocId) continue;

    console.log(`\n======================================================`);
    console.log(`🎬 STARTING FULL 180-FRAME PRODUCTION: ${doc.title}`);
    console.log(`======================================================`);

    const framesPath = path.resolve(ROOT_DIR, doc.framesDir);
    fs.mkdirSync(framesPath, { recursive: true });

    // 1. Navigate to Flow home and create new project
    console.log('Navigating to flow.google.com home...');
    await page.goto('https://flow.google.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    const newBtn = page.locator('button:has-text("New project"), a:has-text("New project"), [aria-label*="New project"]').first();
    if (await newBtn.isVisible().catch(() => false)) {
      await newBtn.click();
    } else {
      await page.click('text="New project"');
    }
    await page.waitForTimeout(4000);

    // 2. Rename project
    const titleSpan = page.locator('span.header-title').first();
    if (await titleSpan.isVisible().catch(() => false)) {
      await titleSpan.click();
      await page.waitForTimeout(800);
      await page.keyboard.press('Meta+A');
      await page.keyboard.press('Backspace');
      await page.keyboard.type(doc.title);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(1000);
    }
    console.log(`Project created: ${page.url()} (${doc.title})`);

    // 3. Load all 180 beats
    const timingData = JSON.parse(fs.readFileSync(path.resolve(ROOT_DIR, doc.timingFile), 'utf8'));
    const allBeats = [];
    for (const [segKey, segVal] of Object.entries(timingData.segments)) {
      const segNum = parseInt(segKey, 10);
      for (const beat of segVal.beats) {
        allBeats.push({
          segNum,
          beatNum: beat.beat_num,
          filename: `seg_${String(segNum).padStart(2, '0')}_beat_${beat.beat_num}.jpg`,
          description: beat.visual_description,
          prompt: beat.prompt
        });
      }
    }

    console.log(`Loaded ${allBeats.length} bespoke frames.`);

    // 4. Construct ONE single unified prompt containing all 180 bespoke frames
    let unifiedPrompt = `Generate the following ${allBeats.length} cinematic scene images in 16:9 widescreen ratio with clean photographic plates and zero text, completely clean frames with zero typography, numbers, or watermarks.\n\n`;
    unifiedPrompt += `IMPORTANT: Please generate all ${allBeats.length} images in batches of 24 images per batch until all ${allBeats.length} images are complete.\n\n`;

    allBeats.forEach((f, idx) => {
      unifiedPrompt += `Frame ${idx + 1} (${f.filename}): ${f.prompt}\n\n`;
    });

    unifiedPrompt += `Please begin now and render all ${allBeats.length} images in batches of 24 images per batch.`;

    console.log(`Unified prompt constructed: ${unifiedPrompt.length} characters.`);

    // 5. Submit unified prompt to Flow
    const textarea = page.locator('textarea, [contenteditable="true"]').first();
    await textarea.click();
    await page.keyboard.press('Meta+A');
    await page.keyboard.press('Backspace');
    await textarea.fill(unifiedPrompt);
    await page.waitForTimeout(1000);

    const submitBtn = page.locator('button:has(:text-is("arrow_forward")), button[type="submit"]').first();
    if (await submitBtn.isVisible().catch(() => false)) {
      await submitBtn.click();
      console.log('Clicked submit button.');
    } else {
      await page.keyboard.press('Enter');
      console.log('Pressed Enter to submit.');
    }

    console.log(`🚀 All 180 frames submitted in one go! Flow is now generating them in batches of 24.`);

    // 6. Monitor and wait for Flow to finish all batches
    console.log('Waiting for Flow AI to execute batches...');
    let lastTileCount = 0;
    let stableCountRounds = 0;

    for (let round = 1; round <= 120; round++) { // up to ~40 minutes
      await page.waitForTimeout(20000); // 20s between checks

      const { isGenerating, tilesCount } = await page.evaluate(() => {
        const stopBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('Stop'));
        const images = document.querySelectorAll('img[src*="/asb/"]');
        return {
          isGenerating: !!stopBtn,
          tilesCount: images.length
        };
      });

      console.log(`[Round ${round}/120] Generating: ${isGenerating} | Images on board: ${tilesCount}/${allBeats.length}`);

      if (tilesCount >= allBeats.length) {
        console.log(`🎉 Target of ${allBeats.length} images reached!`);
        break;
      }

      if (!isGenerating && tilesCount > 0) {
        if (tilesCount === lastTileCount) {
          stableCountRounds++;
          if (stableCountRounds >= 4) { // stable for ~80s after Stop button disappears
            console.log(`Generation completed and stable at ${tilesCount} images.`);
            break;
          }
        } else {
          stableCountRounds = 0;
        }
      } else {
        stableCountRounds = 0;
      }
      lastTileCount = tilesCount;
    }

    // 7. Download all images from board to framesDir
    console.log(`\n📥 Downloading high-res plates to ${doc.framesDir}...`);
    const boardTiles = await page.evaluate(() => {
      const list = [];
      document.querySelectorAll('[aria-label]').forEach(el => {
        const aria = el.getAttribute('aria-label') || '';
        const img = el.querySelector('img');
        if (img && img.src && img.src.includes('/asb/')) {
          list.push({ aria, src: img.src });
        }
      });
      return list;
    });

    console.log(`Found ${boardTiles.length} total tiles with image sources.`);

    // Download each matching beat
    let downloadedCount = 0;
    for (let i = 0; i < allBeats.length; i++) {
      const beat = allBeats[i];
      const outPath = path.resolve(framesPath, beat.filename);

      // Best match from boardTiles:
      // Try matching filename or prompt description keywords
      let matched = boardTiles.find(t => t.aria.toLowerCase().includes(beat.filename.toLowerCase()));
      if (!matched) {
        const kw = beat.description.split(' ').slice(0, 3).join(' ').toLowerCase();
        matched = boardTiles.find(t => t.aria.toLowerCase().includes(kw));
      }
      if (!matched && i < boardTiles.length) {
        // Fallback by sequential index
        matched = boardTiles[i];
      }

      if (matched) {
        const highRes = matched.src.replace(/=s\d+(-[a-z]+)?$/, '=s2048-rw');
        const base64 = await page.evaluate(async (url) => {
          const res = await fetch(url);
          const blob = await res.blob();
          return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
          });
        }, highRes);

        const buf = Buffer.from(base64.split(',')[1], 'base64');
        fs.writeFileSync(outPath, buf);
        downloadedCount++;
        if (downloadedCount % 10 === 0 || downloadedCount === allBeats.length) {
          console.log(`  Downloaded [${downloadedCount}/${allBeats.length}] plates...`);
        }
      }
    }

    console.log(`✅ Saved ${downloadedCount}/${allBeats.length} high-resolution plates for ${doc.title}!`);
  }
}

const targetId = process.argv[2] || null;
runDocumentaryFlowProduction(targetId).catch(console.error);
