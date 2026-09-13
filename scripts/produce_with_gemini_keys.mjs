#!/usr/bin/env node
/**
 * Joy of Care - Gemini Multi-Key Image Production Runner
 * 
 * Automatically rotates across 4 Gemini API keys to generate authentic 16:9 photojournalism
 * hero renders for all articles, ingesting them directly into the Joy of Care asset pipeline.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import crypto from 'crypto';
import { execFileSync } from 'child_process';

const WEB_DIR = '/home/gobeam/Projects/joyofcare-web';
const MANIFEST_PATH = path.join(WEB_DIR, 'assets/images/articles/production_manifest.json');
const INGEST_SCRIPT = path.join(WEB_DIR, 'scripts/run_visual_artists.py');
const SCRATCH_DIR = path.join(WEB_DIR, 'assets/images/articles/.scratch');

if (!fs.existsSync(SCRATCH_DIR)) {
  fs.mkdirSync(SCRATCH_DIR, { recursive: true });
}

// 1. Resolve 4 Gemini Keys (Env vars or auto-decrypt from AionUi database via sqlite3 CLI)
function getGeminiKeys() {
  const envKeys = [];
  if (process.env.GEMINI_API_KEYS) {
    envKeys.push(...process.env.GEMINI_API_KEYS.split(',').map(s => s.trim()).filter(Boolean));
  }
  for (let i = 1; i <= 10; i++) {
    const k = process.env[`GEMINI_API_KEY_${i}`];
    if (k) envKeys.push(k.trim());
  }
  if (process.env.GEMINI_API_KEY) {
    envKeys.push(process.env.GEMINI_API_KEY.trim());
  }
  if (envKeys.length > 0) {
    return [...new Set(envKeys)];
  }

  // Fallback: Decrypt from AionUi SQLite backend database
  try {
    const dbPath = '/home/gobeam/.config/AionUi/aionui/aionui-backend.db';
    if (!fs.existsSync(dbPath)) return [];

    const secretStr = execFileSync('sqlite3', [dbPath, "SELECT encryption_secret FROM users WHERE id = 'system_default_user';"], { encoding: 'utf8' }).trim();
    if (!secretStr) return [];

    const derivedKey = crypto.createHash('sha256').update('aionui-encryption-key:' + secretStr).digest();

    const encB64 = execFileSync('sqlite3', [dbPath, "SELECT api_key_encrypted FROM providers WHERE name = 'Gemini';"], { encoding: 'utf8' }).trim();
    if (!encB64) return [];

    const raw = Buffer.from(encB64, 'base64');
    const nonce = raw.subarray(0, 12);
    const tag = raw.subarray(raw.length - 16);
    const ciphertext = raw.subarray(12, raw.length - 16);

    const decipher = crypto.createDecipheriv('aes-256-gcm', derivedKey, nonce);
    decipher.setAuthTag(tag);
    let decrypted = decipher.update(ciphertext, null, 'utf8') + decipher.final('utf8');
    const keys = decrypted.split(/[\s,]+/).map(s => s.trim()).filter(Boolean);
    return [...new Set(keys)];
  } catch (err) {
    console.error('Warning: Failed to decrypt keys from AionUi DB:', err.message);
    return [];
  }
}

// 2. HTTP Request helper with Promise
function requestGoogleAPI(urlStr, options, payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const reqOpts = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: options.method || 'GET',
      headers: options.headers || {}
    };

    const req = https.request(reqOpts, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        let json = null;
        try {
          json = JSON.parse(body);
        } catch (_) {}
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body,
          json
        });
      });
    });

    req.on('error', reject);
    if (payload) {
      req.write(payload);
    }
    req.end();
  });
}

// 3. Test Key and Model Health
async function checkKeyHealth(apiKey, modelName) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
  const payload = JSON.stringify({
    contents: [{ parts: [{ text: 'Ping' }] }]
  });

  const resp = await requestGoogleAPI(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  }, payload);

  if (resp.statusCode === 200) {
    return { ok: true, message: 'Ready' };
  } else if (resp.json && resp.json.error) {
    return { ok: false, code: resp.statusCode, message: resp.json.error.message };
  } else {
    return { ok: false, code: resp.statusCode, message: resp.body.substring(0, 100) };
  }
}

// 4. Generate Image for a Single Prompt
async function generateImageWithKey(apiKey, modelName, promptText) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
  const payload = JSON.stringify({
    contents: [
      {
        parts: [{ text: promptText }]
      }
    ]
  });

  const resp = await requestGoogleAPI(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  }, payload);

  if (resp.statusCode !== 200) {
    const errorMsg = resp.json?.error?.message || resp.body;
    throw new Error(`API Error HTTP ${resp.statusCode}: ${errorMsg}`);
  }

  const candidate = resp.json?.candidates?.[0];
  const parts = candidate?.content?.parts || [];
  for (const part of parts) {
    if (part.inlineData && part.inlineData.data) {
      return Buffer.from(part.inlineData.data, 'base64');
    }
  }

  throw new Error('No image inlineData found in response candidate parts.');
}

// 5. Main Execution
async function main() {
  const args = process.argv.slice(2);
  const isStatus = args.includes('--status');
  const limitArgIdx = args.indexOf('--limit');
  const limit = limitArgIdx !== -1 ? parseInt(args[limitArgIdx + 1], 10) : Infinity;
  const modelArgIdx = args.indexOf('--model');
  const modelName = modelArgIdx !== -1 ? args[modelArgIdx + 1] : 'gemini-3.1-flash-image';

  console.log('='.repeat(78));
  console.log('🖼️  JOY OF CARE - GEMINI MULTI-KEY IMAGE GENERATOR');
  console.log('='.repeat(78));

  const keys = getGeminiKeys();
  console.log(`🔑 Discovered ${keys.length} Gemini API Key(s)`);

  if (keys.length === 0) {
    console.error('❌ Error: No Gemini API keys found in environment or AionUi database.');
    process.exit(1);
  }

  keys.forEach((k, idx) => {
    console.log(`   Key ${idx + 1}: ${k.substring(0, 10)}...${k.substring(k.length - 4)} (len: ${k.length})`);
  });

  if (isStatus) {
    console.log('\n🔍 Checking Health & Billing for model:', modelName);
    for (let i = 0; i < keys.length; i++) {
      const health = await checkKeyHealth(keys[i], modelName);
      const icon = health.ok ? '✅' : '⚠️';
      console.log(`   Key ${i + 1}: ${icon} ${health.ok ? 'HEALTHY' : 'FAILED (' + health.code + ')'} - ${health.message}`);
    }
    console.log('='.repeat(78));
    return;
  }

  // Load production manifest
  if (!fs.existsSync(MANIFEST_PATH)) {
    console.log('Manifest not found, initializing via run_visual_artists.py...');
    execFileSync('python3', [INGEST_SCRIPT, '--summary'], { stdio: 'inherit' });
  }

  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  const articles = manifest.articles || {};

  // Find articles that still need photojournalism
  const pendingSlugs = Object.keys(articles).filter(s => {
    const a = articles[s];
    return a.status !== 'completed' || a.image_type !== 'photojournalism';
  });

  console.log(`\n📊 Queue Status:`);
  console.log(`   Total Articles       : ${Object.keys(articles).length}`);
  console.log(`   Photojournalism Done : ${Object.keys(articles).length - pendingSlugs.length}`);
  console.log(`   Pending Generation   : ${pendingSlugs.length}`);
  console.log(`   Batch Limit Target   : ${limit === Infinity ? 'All Pending' : limit}`);

  if (pendingSlugs.length === 0) {
    console.log('🎉 All 352 articles have completed authentic photojournalism hero renders!');
    return;
  }

  // Start production with key rotation
  let keyIndex = 0;
  let generatedCount = 0;

  for (const slug of pendingSlugs) {
    if (generatedCount >= limit) {
      console.log(`\n🛑 Batch limit of ${limit} reached for this run.`);
      break;
    }

    const item = articles[slug];
    const promptText = item.image_prompt || item.prompt;
    console.log(`\n🚀 [${generatedCount + 1}/${Math.min(limit, pendingSlugs.length)}] Generating: ${slug}`);
    console.log(`   Track: ${item.artist_track} | Category: ${item.category}`);

    let success = false;
    let attempts = 0;

    while (!success && attempts < keys.length) {
      const activeKey = keys[keyIndex];
      const keyNum = keyIndex + 1;

      try {
        console.log(`   Attempting with Key ${keyNum} on ${modelName}...`);
        const imageBuffer = await generateImageWithKey(activeKey, modelName, promptText);

        // Save raw image buffer
        const tempPath = path.join(SCRATCH_DIR, `${slug}.jpg`);
        fs.writeFileSync(tempPath, imageBuffer);
        console.log(`   ✓ Received image buffer (${imageBuffer.length} bytes). Ingesting to 16:9 WebP...`);

        // Ingest into pipeline using run_visual_artists.py
        execFileSync('python3', [INGEST_SCRIPT, '--ingest', tempPath, '--slug', slug], { stdio: 'inherit' });
        fs.unlinkSync(tempPath);

        success = true;
        generatedCount++;
        // Rotate key gently on success to balance quota evenly
        keyIndex = (keyIndex + 1) % keys.length;
      } catch (err) {
        console.warn(`   ⚠️ Key ${keyNum} failed: ${err.message}`);
        attempts++;
        keyIndex = (keyIndex + 1) % keys.length; // rotate to next key
      }
    }

    if (!success) {
      console.error(`\n❌ All ${keys.length} API keys failed for "${slug}".`);
      console.error(`   Please check prepayment credits at https://ai.studio/projects or supply active keys via GEMINI_API_KEYS.`);
      break;
    }
  }

  console.log('\n' + '='.repeat(78));
  console.log(`✨ Batch completed. Generated and ingested ${generatedCount} photojournalism hero assets.`);
  console.log('='.repeat(78));
}

main().catch(err => {
  console.error('Fatal error in runner:', err);
  process.exit(1);
});
