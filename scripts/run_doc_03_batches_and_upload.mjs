import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const pw = await import(path.resolve(ROOT_DIR, 'tools/google-flow-mcp/node_modules/playwright/index.mjs'));
const { chromium } = pw;

const BATCHES = [
  { start: 1, end: 24, prompt: 'Generate frames 1 through 24' },
  { start: 25, end: 48, prompt: 'Generate frames 25 through 48' },
  { start: 49, end: 72, prompt: 'Generate frames 49 through 72' },
  { start: 73, end: 96, prompt: 'Generate frames 73 through 96' },
  { start: 97, end: 120, prompt: 'Generate frames 97 through 120' },
  { start: 121, end: 144, prompt: 'Generate frames 121 through 144' },
  { start: 145, end: 168, prompt: 'Generate frames 145 through 168' },
  { start: 169, end: 180, prompt: 'Generate frames 169 through 180' },
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

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9225');
  const context = browser.contexts()[0];
  const flowPage = context.pages().find(p => p.url().includes('flow.google.com/project/1918faa1-3bfd-48c1-9a10-09441828bc49'));

  if (!flowPage) {
    console.error('Doc 03 project page not found!');
    process.exit(1);
  }

  console.log('Connected to Doc 03 Flow project:', flowPage.url());

  // Check how many images exist and what batch we are on
  for (let batchIdx = 0; batchIdx < BATCHES.length; batchIdx++) {
    const batch = BATCHES[batchIdx];
    console.log(`\n--- Checking Batch ${batchIdx + 1}/${BATCHES.length} (Frames ${batch.start}–${batch.end}) ---`);

    // Wait until Flow is idle (hasStop is false)
    let isGenerating = true;
    while (isGenerating) {
      await flowPage.waitForTimeout(10000); // check every 10s
      isGenerating = await flowPage.evaluate(() => {
        const stopBtn = Array.from(document.querySelectorAll('button')).find(b => {
          const t = (b.innerText || '').toLowerCase();
          return t === 'stop' || t.includes('stop generating');
        });
        return !!stopBtn;
      });

      const imgCount = await flowPage.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('/asb/') || s.includes('googleusercontent'));
        return Array.from(new Set(imgs)).length;
      });

      console.log(`[Batch ${batchIdx + 1}] Active: ${isGenerating} | Images on board: ~${imgCount}`);

      if (!isGenerating) {
        break;
      }
    }

    // Check if the next batch needs to be triggered
    if (batchIdx > 0 || (batchIdx === 0 && false)) {
      console.log(`👉 Sending prompt for Batch ${batchIdx + 1}: "${batch.prompt}"...`);
      const textarea = flowPage.locator('textarea, [contenteditable="true"]').first();
      await textarea.click();
      await flowPage.waitForTimeout(400);
      await textarea.fill(batch.prompt);
      await flowPage.waitForTimeout(500);

      const submitBtn = flowPage.locator('button:has(:text-is("arrow_forward")), button[type="submit"]').first();
      if (await submitBtn.isVisible().catch(() => false)) {
        await submitBtn.click();
      } else {
        await flowPage.keyboard.press('Enter');
      }

      console.log(`✅ Triggered Batch ${batchIdx + 1}. Waiting 15s for generation to spin up...`);
      await flowPage.waitForTimeout(15000);
    } else {
      console.log(`Batch 1 was already triggered and is finishing.`);
    }
  }

  console.log('\n🎉 ALL 8 BATCHES PROCESSED! Expanding all images...');
  await flowPage.evaluate(() => {
    const seeAlls = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'See all');
    seeAlls.forEach(b => b.click());
  });
  await flowPage.waitForTimeout(4000);

  // Download all 180 images
  const timingData = JSON.parse(fs.readFileSync(path.resolve(ROOT_DIR, 'output/nuclear_ai_documentary/timing_and_timestamps.json'), 'utf8'));
  const allBeats = [];
  for (const [segKey, segVal] of Object.entries(timingData.segments)) {
    const segNum = parseInt(segKey, 10);
    for (const beat of segVal.beats) {
      allBeats.push({
        segNum,
        beatNum: beat.beat_num,
        filename: `seg_${String(segNum).padStart(2, '0')}_beat_${beat.beat_num}.jpg`
      });
    }
  }

  const framesDir = path.resolve(ROOT_DIR, 'output/nuclear_ai_documentary/frames');
  fs.mkdirSync(framesDir, { recursive: true });

  const imageUrls = await flowPage.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s.includes('/asb/') || s.includes('googleusercontent'));
    return Array.from(new Set(imgs));
  });

  console.log(`\n📥 Downloading all ${imageUrls.length} frames to ${framesDir}...`);
  for (let i = 0; i < allBeats.length; i++) {
    if (i >= imageUrls.length) break;
    const beat = allBeats[i];
    const outPath = path.resolve(framesDir, beat.filename);
    const highResUrl = imageUrls[i].replace(/=s\d+(-[a-z]+)?$/, '=s2048-rw');

    const base64 = await flowPage.evaluate(async (url) => {
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
      if ((i + 1) % 15 === 0 || i + 1 === allBeats.length) {
        console.log(`  Downloaded [${i + 1}/${allBeats.length}] plates...`);
      }
    }
  }

  console.log('✅ Download complete! Rendering and uploading Doc 03...');
  await runCommand('.venv/bin/python', ['scripts/render_and_upload_documentary_from_spec.py', 'nuclear_ai']);
  console.log('🏆 DOC 03 COMPLETE AND UPLOADED TO YOUTUBE!');
}

main().catch(console.error);
