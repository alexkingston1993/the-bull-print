import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const pw = await import(path.resolve(ROOT_DIR, 'tools/google-flow-mcp/node_modules/playwright/index.mjs'));
const { chromium } = pw;

const targetDocId = process.argv[2] || null;

const DOC_CONFIGS = [
  {
    id: 'ai_bubble',
    title: 'Doc 01 - The $2.5 Trillion AI Bubble Panic',
    timingFile: 'output/ai_bubble_documentary/timing_and_timestamps.json',
    framesDir: 'output/ai_bubble_documentary/frames',
    completed: true,
    alreadyStarted: true
  },
  {
    id: 'fii_exodus',
    title: 'Doc 02 - The ₹14,900 Crore FII Capital Exodus',
    timingFile: 'output/fii_exodus_documentary/timing_and_timestamps.json',
    framesDir: 'output/fii_exodus_documentary/frames',
    completed: false,
    alreadyStarted: false
  },
  {
    id: 'nuclear_ai',
    title: "Doc 03 - Big Tech's Nuclear Secret",
    timingFile: 'output/nuclear_ai_documentary/timing_and_timestamps.json',
    framesDir: 'output/nuclear_ai_documentary/frames',
    completed: false,
    alreadyStarted: false
  }
];

function runCommand(cmd, args) {
  return new Promise((resolve, reject) => {
    console.log(`\n🚀 Executing: ${cmd} ${args.join(' ')}`);
    const proc = spawn(cmd, args, { cwd: ROOT_DIR, stdio: 'inherit' });
    proc.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`Command exited with code ${code}`));
    });
  });
}

async function autoStepBatchesUntilComplete(page, targetTotal = 180) {
  console.log(`\n⚡ Monitoring Flow batches until all ${targetTotal} images are rendered...`);
  
  let currentBatch = 1;
  const maxRounds = 300; // ~50 minutes max

  for (let round = 1; round <= maxRounds; round++) {
    await page.waitForTimeout(10000); // 10s polling interval

    const status = await page.evaluate(() => {
      const stopBtn = Array.from(document.querySelectorAll('button')).find(b => {
        const t = (b.innerText || '').toLowerCase();
        return t === 'stop' || t.includes('stop generating');
      });

      const seeAllBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'See all');
      
      const bodyText = document.body.innerText || '';
      const tail = bodyText.slice(-1200);

      const allImgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('/asb/') || s.includes('googleusercontent'));
      const uniqueImgs = Array.from(new Set(allImgs));

      const isAskingNextBatch = tail.includes('Would you like me to generate the next batch') || 
                               tail.includes('Would you like me to proceed with generating the next batch') ||
                               tail.includes('Would you like to proceed with the next batch') ||
                               tail.includes('proceed with generating the next batch');

      const isFinishedAll = uniqueImgs.length >= 180;

      return {
        hasStop: !!stopBtn,
        seeAllCount: seeAllBtns.length,
        totalImgTags: allImgs.length,
        uniqueImgsCount: uniqueImgs.length,
        isAskingNextBatch,
        isFinishedAll,
        lastSnippet: tail.slice(-250).replace(/\n+/g, ' ')
      };
    });

    console.log(`[Round ${round}] Active: ${status.hasStop} | Unique Imgs: ${status.uniqueImgsCount}/${targetTotal} | Asking: ${status.isAskingNextBatch}`);

    if (status.uniqueImgsCount >= targetTotal || status.isFinishedAll) {
      console.log(`🎉 Flow has generated all ${targetTotal} images!`);
      break;
    }

    // If Flow finished a batch and is waiting for confirmation to proceed:
    if (!status.hasStop && status.isAskingNextBatch) {
      console.log(`👉 Flow is asking for next batch confirmation. Sending proceed command...`);
      const textarea = page.locator('textarea, [contenteditable="true"]').first();
      await textarea.click();
      await page.waitForTimeout(300);
      await textarea.fill('Yes, please generate the next batch of 24 images now.');
      await page.waitForTimeout(500);

      const submitBtn = page.locator('button:has(:text-is("arrow_forward")), button[type="submit"]').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        await submitBtn.click();
      } else {
        await page.keyboard.press('Enter');
      }
      console.log(`✅ Sent confirmation for next batch.`);
      await page.waitForTimeout(10000);
    }
  }

  // Click all "See all" buttons to expand any collapsed image lists
  console.log('Expanding all "See all" containers to reveal every frame...');
  await page.evaluate(() => {
    const seeAlls = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'See all');
    seeAlls.forEach(b => b.click());
  });
  await page.waitForTimeout(3000);
}

async function downloadAllFrames(page, beats, framesDir) {
  console.log(`\n📥 Downloading all ${beats.length} high-resolution frames to ${framesDir}...`);
  fs.mkdirSync(framesDir, { recursive: true });

  // Get all unique image URLs from the DOM
  const imageUrls = await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('/asb/') || s.includes('googleusercontent'));
    return Array.from(new Set(imgs));
  });

  console.log(`Found ${imageUrls.length} unique image URLs on Flow.`);

  let downloaded = 0;
  for (let i = 0; i < beats.length; i++) {
    const beat = beats[i];
    const outPath = path.resolve(framesDir, beat.filename);

    if (i >= imageUrls.length) {
      console.warn(`⚠️ Warning: Not enough images found for beat ${i + 1} (${beat.filename})`);
      break;
    }

    const rawUrl = imageUrls[i];
    const highResUrl = rawUrl.replace(/=s\d+(-[a-z]+)?$/, '=s2048-rw');

    const base64 = await page.evaluate(async (url) => {
      const res = await fetch(url);
      const blob = await res.blob();
      return new Promise(resolve => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(blob);
      });
    }, highResUrl);

    if (base64 && base64.includes(',')) {
      const buf = Buffer.from(base64.split(',')[1], 'base64');
      fs.writeFileSync(outPath, buf);
      downloaded++;
      if (downloaded % 10 === 0 || downloaded === beats.length) {
        console.log(`  Downloaded [${downloaded}/${beats.length}] high-res frames...`);
      }
    }
  }

  console.log(`✅ Completed downloading ${downloaded}/${beats.length} plates!`);
  return downloaded;
}

export async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9225');
  const context = browser.contexts()[0];
  let page = context.pages().find(p => p.url().includes('flow.google.com'));

  for (const doc of DOC_CONFIGS) {
    if (targetDocId && doc.id !== targetDocId) continue;
    if (doc.completed) {
      console.log(`⏩ Skipping ${doc.title} (already completed and uploaded)`);
      continue;
    }

    console.log(`\n======================================================`);
    console.log(`🎬 PROCESSING DOCUMENTARY: ${doc.title}`);
    console.log(`======================================================`);

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

    if (!doc.alreadyStarted) {
      // Create new project in Flow
      console.log('Navigating to flow.google.com to create project...');
      await page.goto('https://flow.google.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);

      const newBtn = page.locator('button:has-text("New project"), a:has-text("New project"), [aria-label*="New project"]').first();
      if (await newBtn.isVisible().catch(() => false)) {
        await newBtn.click();
      } else {
        await page.click('text="New project"');
      }
      await page.waitForTimeout(4000);

      // Rename project
      const titleSpan = page.locator('span.header-title').first();
      if (await titleSpan.isVisible().catch(() => false)) {
        await titleSpan.click();
        await page.waitForTimeout(500);
        await page.keyboard.press('Meta+A');
        await page.keyboard.press('Backspace');
        await page.keyboard.type(doc.title);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1000);
      }
      console.log(`Project created: ${page.url()} (${doc.title})`);

      // Construct unified prompt for all 180 bespoke frames
      let unifiedPrompt = `Generate the following ${allBeats.length} cinematic scene images in 16:9 widescreen ratio with clean photographic plates and zero text, completely clean frames with zero typography, numbers, or watermarks.\n\n`;
      unifiedPrompt += `IMPORTANT: Please generate all ${allBeats.length} images in batches of 24 images per batch until all ${allBeats.length} images are complete.\n\n`;
      allBeats.forEach((f, idx) => {
        unifiedPrompt += `Frame ${idx + 1} (${f.filename}): ${f.prompt}\n\n`;
      });
      unifiedPrompt += `Please begin now and render all ${allBeats.length} images in batches of 24 images per batch.`;

      // Submit unified prompt
      const textarea = page.locator('textarea, [contenteditable="true"]').first();
      await textarea.click();
      await page.keyboard.press('Meta+A');
      await page.keyboard.press('Backspace');
      await textarea.fill(unifiedPrompt);
      await page.waitForTimeout(1000);

      const submitBtn = page.locator('button:has(:text-is("arrow_forward")), button[type="submit"]').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        await submitBtn.click();
      } else {
        await page.keyboard.press('Enter');
      }
      console.log(`🚀 All 180 prompts submitted in 1 collection! Flow will now generate them in batches of 24.`);
    } else {
      console.log(`Doc 01 is already running on Flow at: ${page.url()}`);
    }

    // Step through batches until all 180 images are rendered
    await autoStepBatchesUntilComplete(page, allBeats.length);

    // Download high-res plates
    const framesPath = path.resolve(ROOT_DIR, doc.framesDir);
    await downloadAllFrames(page, allBeats, framesPath);

    // Render 12-minute documentary and upload to YouTube
    console.log(`\n🎞 Rendering master 12-minute documentary and uploading to YouTube...`);
    await runCommand('.venv/bin/python', ['scripts/render_and_upload_documentary_from_spec.py', doc.id]);
    console.log(`🏆 Finished documentary: ${doc.title}!`);
  }

  console.log(`\n🎉 ALL 3 MASTER DOCUMENTARIES PRODUCED AND UPLOADED SUCCESSFULLY!`);
  await browser.close();
}

main().catch(console.error);
