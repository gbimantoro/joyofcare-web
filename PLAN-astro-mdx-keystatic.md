# JoyofCare-Web Astro + MDX + Keystatic Migration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Rebuild `joyofcare-web` as a proper Astro + MDX + Keystatic site (replacing the Odoo-era static HTML hybrid), learning from every mistake found in the 2026-09-06 deep review.

**Architecture:** Astro 7 (SSG, `output: 'static'`) renders pages from an MDX content collection (`src/content/articles/`); Keystatic 6 (GitHub-backed) is the CMS admin at `/keystatic`; the site deploys to Cloudflare Pages custom domain. Content source of truth = **clean MDX files**, not net .txt.

**Canonical domain (DECIDED 2026-09-06): `https://new.joyof.care`** — single SITE_URL everywhere (canonical, OG, sitemap, robots, llms). `joyofcare.net` (Odoo) is NOT canonical for now; migrate/redirect it later.

**Tech Stack:** Astro ^7.3.1, @astrojs/mdx ^8, @keystatic/core ^0.6.9 + @keystatic/astro ^6, @astrojs/cloudflare ^14 (static adapter) OR plain static deploy to Pages, Node 26.

---

## 0. Context — what the deep review found (the "don't repeat" list)

Verified facts (2026-09-06, filesystem+git+curl):

| # | Mistake | Evidence | This plan's guard |
|---|---------|----------|-------------------|
| 1 | Claims ≠ reality ("markdown fixed" 3×, "deployed" while 404) | live `joyofcare.net` still Odoo; `new.joyof.care` 404 on all paths | Every task ends with **real verification**: `curl`, `astro build`, `grep dist output`. |
| 2 | 5 parallel content copies drifted | net 137 txt / content-source 141 / mdx 142 / blog html 168 / sitemap 274 / index.json 37 | One master: MDX. Delete the rest. |
| 3 | Broken YAML everywhere | net txt `---title:` glued line 1 (137/137); mdx double-frontmatter (137/142 polluted) | **Migration script parses + rewrites clean YAML**, validated by `astro build`. |
| 4 | Duplicate content / near-dup slugs | `-41.mdx` vs truncated `...-wajib-.mdx`; `pentingnya-vaksinasi...-12/-28` same base; `panduan-fisioterapi-osteoporosis.mdx` extra | Canonical set defined in Phase 2; dedupe table; archive removed. |
| 5 | 3 stacks in one repo (static pages/, Astro src/, Next cms/) | `astro build` FAILS (YAML @ `3-jenis...-35.mdx:7:8`); `cms/` unused | Delete legacy trees after content port (Phase 9). Single stack. |
| 6 | SEO drift: 2 domains in canonicals/sitemaps, Odoo-era URLs, hub stale (37/168), 2×H1 (164/168), FAQPage schema 0, no ISO dates, WA URL `?phone…?text=` (168/168) | grep + curl + schema scan | Single `SITE_URL` constant; layouts render one H1 + FAQPage + ISO dates; build-time sitemap from collection; verification script. |
| 7 | Dirty repos + PAT in git remote | web 179 M files; net 141 M + 4 ??; `ghp_…` in origin URL | Phase 1 commit/cleanup + scrub remotes before code. |
| 8 | Deploy never verified | Pages configured for `astro build` which fails | Deploy task = curl production + preview domain. |
| 9 | SOP docs stale (4 categories vs 12 real) | publishing-workflow.md | Docs regenerated from schema at end. |

**Canonical target set (Phase 2 decision):** net master `.txt` is the *content source for one-time migration*, but going forward **MDX in `joyofcare-web/src/content/articles/` is the single source of truth** (editable via Keystatic). joyofcare-net becomes archive/research only.

---

## Phase 1 — Repo hygiene & safety baseline (no feature work)

### Task 1.1: Snapshot & commit current state
**Files:** both repos.
**Step 1:** In each repo: `git status --short | wc -l` → record.
**Step 2:** Commit everything as a checkpoint:
```bash
cd /home/gobeam/Projects/joyofcare-web
git add -A && git commit -m "chore: checkpoint pre-Astro-migration (dirty state from enrichment)"
cd /home/gobeam/Projects/joyofcare-net
git add -A && git commit -m "chore: checkpoint pre-migration"
```
**Step 3 (verify):** `git status --short` → empty in both. Push.

### Task 1.2: Scrub secrets from remotes
```bash
cd /home/gobeam/Projects/joyofcare-web
git remote set-url origin https://github.com/gbimantoro/joyofcare-web.git
cd /home/gobeam/Projects/joyofcare-net
git remote set-url origin https://github.com/gbimantoro/joyofcare-net.git
```
**Verify:** `git remote -v` shows NO `ghp_`/token. **Then rotate the old PAT in GitHub** (it was exposed in git config history; user action required — flag in final report).

### Task 1.3: Fix .gitignore before anything is added
`joyofcare-web/.gitignore` must contain: `node_modules/`, `dist/`, `.astro/`, `.wrangler/`, `.env*`, `cms/node_modules/`, `.DS_Store`. Remove tracked junk:
```bash
cd /home/gobeam/Projects/joyofcare-web
git rm -r --cached .wrangler 2>/dev/null  # 21 files tracked wrongly
git rm pages/temp_*.md 2>/dev/null        # 7 leftover temp files
git rm -r --cached cms/node_modules 2>/dev/null
git commit -m "chore: fix gitignore, untrack .wrangler, remove temp files"
```
**Verify:** `git ls-files | grep -c wrangler` → 0; `git status` clean.

### Task 1.4: Create migration workspace branch
```bash
cd /home/gobeam/Projects/joyofcare-web
git checkout -b feat/astro-mdx-keystatic
```
**Verify:** `git branch --show-current` → `feat/astro-mdx-keystatic`.

---

## Phase 2 — Canonical content inventory & dedupe decision

### Task 2.1: Parse all 137 net txt into a JSON inventory (read-only analysis)
Create: `joyofcare-net/scripts/migration/inventory.py` (new scripts dir for migration only).

Parse each `articles-final-37/*.txt` + `articles-new-final-100/*.txt` with a **custom tolerant parser** (these files have `---title:` glued and unquoted/multiline YAML — PyYAML will fail; parse fields by line-prefix):
- fields: title (after `---title:`), slug, category, meta_description (folded), primary_keyword, secondary_keywords (list), faq (list q/a, folded), internal_links, clinical_references, body (markdown after first real `\n---`).
- Emit `joyofcare-net/scripts/migration/inventory.json`: slug, source dir, category, word count, md5.
**Verify:** 137 entries, all fields present (report count per field; earlier scan: faq=137, meta_desc=137, internal_links=137, clin_refs=137, prim_kw=137).

### Task 2.2: Build dedupe & canonical map
Analyze against the 142 existing `src/content/articles/*.mdx` and 141 blog html slugs. Rules:
- Canonical slug = net txt slug (has `-NN` suffixes, e.g. `-41`, `-43`).
- Old truncated mdx (`...-wajib-.mdx`, `...-hin.mdx`, `...-ho.mdx`, `...-mengu.mdx`) = **pre-rewrite duplicates → archive, never migrate**.
- `panduan-fisioterapi-osteoporosis.mdx` (clean FM, standalone) → decide: migrate content if unique else archive (it's the pre-rewrite version of `-43` family — likely dup; verify by title/body overlap).
- `pentingnya-vaksinasi...-12` vs `-28` (same base, both in net) → **keep both** (different body? verify overlap <60% → distinct articles with same base name; if near-identical, keep one + canonical redirect).
- Output: `canonical-map.json` {old_slug → final_slug_or_DELETE, final set list}.
**Verify:** final set count documented (target ≈ 137, exact after dedupe). No two final slugs equal. All DELETE decisions have a reason + archive location.

### Task 2.3: Category normalization map
Category list in net txt (12, verified): perawatan-lansia 38, fisioterapi-rumah 23, panggil-dokter 18, parkinson 11, studi-luar-negeri 11, osteoporosis 9, antar-jemput-rs 6, vaksinasi-rumah 5, perawat-homecare 5, infus-vitamin 5, kesehatan-umum 3, home-lab 3.
Note: category display labels must match `CATEGORIES` used by build script + Keystatic options (existing keystatic.config.ts already has 12 with `Vaksinasi` label for `vaksinasi-rumah` — verify).
Create `src/lib/categories.ts` exporting slug→label (single source, imported by layouts, sitemap, blog hub, category pages).
**Verify:** every inventory category exists in the map; Keystatic select options identical.

---

## Phase 3 — Clean migration: net txt → valid MDX

### Task 3.1: Write migration script `joyofcare-net/scripts/migration/txt_to_mdx.py`
For each canonical entry:
1. Read txt; parse (reuse Task 2.1 parser).
2. Emit MDX:
   ```
   ---
   title: "<clean human title>"
   metaTitle: "<title> | Joy of Care"   # ≤60 chars
   metaDescription: "<from FM, one line>"
   category: <cat>
   author: "Tim Medis Joy of Care"
   reviewer: "dr. Sarah Wijaya, Sp.FR"
   date: 2026-09-05          # from git/log provenance; ISO date only
   slug: <slug>
   primaryKeyword: <pk>
   secondaryKeywords: [...]  # array form
   internalLinks: [...]      # from FM internal_links parsed to slugs
   faq:
     - question: "..."
       answer: "..."
   clinicalReferences: [...] # optional keep
   ---
   # <Title>      ← ONLY ONE H1, from title, NOT duplicated in layout
   <body cleaned>
   ```
3. **Body cleaning rules (apply all):**
   - Fix WhatsApp URLs: `send/?phone=628811118911?text=` → `send/?phone=628811118911&text=` (the 168/168 bug).
   - Strip raw `https://api.whatsapp.com…`/`wa.me` bare lines (layout renders CTA once).
   - Strip duplicate CTA wording blocks (`📲 **Hubungi WhatsApp…**: <a>` leftovers), keep no more than needed.
   - Remove any `[Konsultasi…](…)` markdown link relics.
   - Keep info boxes but ensure heading text uses **"Penting dipahami"** (not Poin Kunci / Ringkasan Eksekutif — user standard).
   - Ensure H1 appears once in body OR once in layout (decide: layout shows H1 from FM; **strip leading `# Title` in body if it equals FM title**; else keep body H1 and layout renders no duplicate — pick rule in code: body H1 wins if body starts with `# `; layout omits H1 then).
   - No prices (client rule), no fake case studies.
4. Output to `joyofcare-web/src/content/articles/<slug>.mdx` (flat dir; category is FM field, Keystatic path matches `src/content/articles/*`).

**Verify (this is the critical gate):**
```bash
cd /home/gobeam/Projects/joyofcare-web
python3 /home/gobeam/Projects/joyofcare-net/scripts/migration/txt_to_mdx.py --dry-run   # report only
# after real run:
python3 -c "import glob,yaml; [yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('src/content/articles/*.mdx')]"  # must not raise
npx astro check   # content collection validates
```
Every generated mdx must parse; `astro build` must pass (may still fail on old duplicates — Phase 4 removes them).

### Task 3.2: Remove obsolete mdx duplicates
Archive (move to `joyofcare-net/scripts/migration/archive-md/`) the old truncated + standalone dup mdx identified in Task 2.2. Never `git rm` without archive.
**Verify:** count matches canonical-map DELETE list; `astro build` passes.

### Task 3.3: Parity check content-source + blog html cleanup
Delete stale `joyofcare-web/content-source/` after migration (it was a txt mirror). Delete `pages/blog/` static HTML **only after Phase 8 port is verified** (kept until Astro pages cover all routes — see Phase 9 for final removal). Mark as deprecated in README now.

---

## Phase 4 — Astro framework hardening (src/)

### Task 4.1: Fix `src/content.config.ts`
Schema (must match Keystatic config exactly): `slug` (string), `title`, `metaTitle?`, `metaDescription`, `category` (enum 12), `author` default, `reviewer` default, `date: z.coerce.date()`, `featuredImage?`, `primaryKeyword?`, `secondaryKeywords?` array, `internalLinks?` array, `faq?` array of {question, answer}, `clinicalReferences?`.
**Verify:** `npx astro check` passes on migrated content.

### Task 4.2: Single `SITE_URL` constant + layout fixes
Create `src/consts.ts`: `SITE_URL = 'https://new.joyof.care'` (**DECIDED canonical — do NOT change to www.joyofcare.net**).
- `BaseLayout.astro`: canonical/OG URLs absolute via SITE_URL; fix favicon/og-image to local assets; JSON-LD MedicalBusiness uses SITE_URL; add FAQPage injection hook; keep lang="id".
- `ArticleLayout.astro`: single H1 rule (from Task 3.1); inject `FAQPage` JSON-LD from FM faq (current layout has MedicalWebPage + BreadcrumbList but no FAQPage and no ISO dateModified — add `dateModified` same as date, ISO); schema adds `datePublished`/`dateModified` ISO 8601; render FAQ section from FM (semantic `<details>`), CTA sidebar once with correct `&text=` URL; author/reviewer block (E-E-A-T); medical disclaimer line (required, currently 1/168).
**Verify:** render one sample article page; grep output: exactly 1 `<h1`, contains `FAQPage`, `"datePublished": "2026-…T…`, CTA URL has `&text=`, no `?text=`.

### Task 4.3: Port 11 static pages → Astro routes
Existing static content lives in `pages/*.html` (homepage index, 8 service pages + homelab, layanan-lengkap, 404, artikel). Port each to `src/pages/…` using the SAME design tokens (copy styles into global CSS once):
- `index.astro` (exists — verify content parity with static index.html, fix Odoo image URLs `/web/image/…` → local `/images/…`)
- `panggil-dokter-ke-rumah.astro`, `layanan-fisioterapi-ke-rumah.astro`, `layanan-perawat-di-rumah.astro`, `layanan-akupuntur-di-rumah.astro`, `homelab.astro`, `infus-suntik-vitamin-di-rumah.astro`, `transcare-antar-jemput-ke-rs-jakarta-tangerang.astro`, `layanan-lengkap.astro`, `404.astro`.
- Each service page: schema (MedicalProcedure/MedicalTherapy/…), H1 unique, WA CTA correct, OG absolute, local images.
**Verify:** `astro build` emits each route; visual spot-check in `astro preview`; no `/web/image/` or odoo.com references anywhere in src (`grep -r "web/image\|odoo.com" src/ public/` → 0).

### Task 4.4: Global CSS & assets to `public/`
- Create `public/`; move images from `pages/images/`, `pages/assets/`, css (style.css + blog.css → merge into `src/styles/global.css` imported by layouts; keep fonts), js (main.js → Astro `<script>` or public js), robots.txt, llms.txt (update SITE_URL), favicon.
- astro.config: static output; remove `output:'server'` + cloudflare adapter unless Keystatic prod needs server (see Phase 7 decision); `trailingSlash: 'ignore'` or keep 'always' consistently with links.
**Verify:** build output includes assets; `curl`-equivalent local check via `astro preview` returns 200 for /css/…, /images/….

### Task 4.5: Blog hub + category pages (from collection, not stale JSON)
- `src/pages/blog/index.astro`: list from `getCollection('articles')`, real counts, links `/blog/<category>/<slug>/`, categories from `categories.ts`.
- `src/pages/blog/[category]/index.astro`: card grid per category (exists — verify it reads new FM category values).
- `src/pages/blog/[category]/[slug].astro` (exists — verify props match schema, add FAQ render + disclaimer).
**Verify:** build lists N articles == canonical count; category pages non-empty for all 12 (counts match inventory; empty cats dropped).

---

## Phase 5 — Sitemap, RSS, index.json, redirects (from collection)

### Task 5.1: `@astrojs/sitemap` integration
Add `@astrojs/sitemap` to astro.config with `site: SITE_URL` + custom filter so only real pages are listed (kills the 274-loc phantom sitemap). Include service pages + all article URLs.
**Verify:** build → `dist/sitemap-index.xml`; count locs == canonical pages (not 274).

### Task 5.2: RSS feed + blog index.json endpoints
`src/pages/blog/feed.xml.ts` (or @astrojs/rss) — regenerate feed from collection (static feed.xml in pages/blog is stale). `src/pages/blog/index.json.ts` — serve JSON index generated from collection (fixes 37-vs-168 staleness).
**Verify:** `/blog/feed.xml` valid XML with N items; `/blog/index.json` N entries.

### Task 5.3: `_redirects` for Odoo-era URLs (Cloudflare Pages)
Create `public/_redirects` mapping legacy patterns → new Astro routes, incl.:
- `/artikel/*` → `/blog/…` (user asked earlier; map by slug when known, else `/blog/`)
- `/blog/healthy-aging-3/*`, `/artikel/healthy-aging-3`, `/blog/vaksinasi-di-rumah-2/*` → category pages
- old truncated slugs → canonical `-NN` slugs (from canonical-map)
- `/layanan-kami`, `/walk-in-promo`, `/tindakan-perawat-di-rumah`, `/web/*` → 404 or relevant page
**Verify:** `wrangler pages deploy --dry-run` or local preview honors redirects (spot check 3 entries with curl on preview).

---

## Phase 6 — Verification script & local CI gate

### Task 6.1: `scripts/verify_site.py` (web repo)
Runs after every build and FAILS on: any `?phone=628811118911?text=`, `>1 <h1` in article pages, missing `FAQPage`/`datePublished` ISO in article JSON-LD, `web/image|odoo.com` refs, count mismatch between sitemap locs and article files, canonical not SITE_URL, markdown relics (`**`, `## `) in rendered HTML, "Poin Kunci"/"Ringkasan Eksekutif" headings, any price `Rp` in article HTML.
**Verify:** script exits 0 on clean build; deliberately break one file → exits non-zero with message (prove it catches).

### Task 6.2: Wire as `npm run verify` (+ optional pre-push git hook)
**Verify:** `npm run build && npm run verify` = green end-to-end.

---

## Phase 7 — Keystatic CMS (single instance)

### Task 7.1: Consolidate to root keystatic.config.ts
Delete `cms/` (Next.js duplicate) after confirming nothing references it; root `keystatic.config.ts` already exists (GitHub storage, repo gbimantoro/joyofcare-web, collection `articles` at `src/content/articles/*`). Align schema fields with content.config.ts (add faq, secondaryKeywords, primaryKeyword, internalLinks, clinicalReferences; body = mdx).
**Verify:** `npx keystatic` type-checks config (dry local start).

### Task 7.2: Keystatic dev mode
`npm run dev` → admin at `/keystatic` edits local MDX.
**Verify:** edit a test article in browser admin → file changes on disk → build still passes.

### Task 7.3: Keystatic production mode decision
**Decision point:** Keystatic GitHub storage on Cloudflare Pages needs server-side GitHub API calls → requires either (a) `output:'server'` with @astrojs/cloudflare + GitHub OAuth env, or (b) static deploy where content edits happen via Keystatic locally / GitHub UI, or (c) deploy admin as separate small worker. Research current @keystatic/astro + CF Pages guidance at implementation time (docs change). Default recommendation: **static site + GitHub-storage Keystatic run locally** for content ops (lowest risk, keeps site pure static/fast), revisit if client wants in-browser editing in prod.
**Verify:** documented decision + working local admin; env vars never committed.

---

## Phase 8 — Cloudflare Pages deploy (the part that was always broken)

### Task 8.1: Create Pages project config
`wrangler.toml` (or dashboard): project `new-joy-of-care`, build command `npm run build`, output `dist/`, node 26. Custom domain `new.joyof.care` already attached (verified: Cloudflare responds on it, currently 404 = no successful deployment). Deploy preview first.
**Verify:** `wrangler pages deploy dist/ --project-name new-joy-of-care --branch preview` succeeds; preview URL returns 200.

### Task 8.2: Verify production domain (new.joyof.care) — THE go-live gate
After first successful deploy, curl every critical path:
```bash
for p in / /blog/ /blog/perawatan-lansia/ /blog/fisioterapi-rumah/ /panggil-dokter-ke-rumah /robots.txt /llms.txt /sitemap-index.xml; do
  echo -n "$p -> "; curl -s -o /dev/null -w "%{http_code}\n" "https://new.joyof.care$p"
done
```
**Verify:** all 200 (this kills the current 404-everywhere state); article URL 200; random slug → 404 page.
### Task 8.3: joyofcare.net DNS (do NOT cut over until new.joyof.care is 200)
Canonical is new.joyof.care, so joyofcare.net must NOT serve duplicate canonical content. Chosen option (confirm w/ user): leave Odoo live at joyofcare.net for now, OR set Cloudflare **Redirect Rule** on the joyofcare.net zone: hostname `joyofcare.net` + `www.joyofcare.net` → 301 `https://new.joyof.care` (preserve path). No DNS record change needed if using a redirect rule (zone is already on Cloudflare). **Requires Cloudflare dashboard/API access — user action.**
**Verify:** `curl -I https://www.joyofcare.net/` → 301 to new.joyof.care (if redirect chosen) OR unchanged Odoo (if keep-live chosen). Never both domains 200 with the same content.

---

## Phase 9 — Legacy cleanup (only after parity verified)

### Task 9.1: Delete legacy static tree
After all routes verified on Astro: remove `pages/` static HTML (keep only what's referenced: none), `content-source/`, `cms/`, old `.wrangler`, `dist/` (gitignored anyway). Keep `pages/blog` content only if needed as redirect source → prefer `_redirects`.
**Verify:** `git status` clean; `astro build` green; preview parity: homepage + services + every article renders.

### Task 9.2: Repo docs update
- README: single-stack architecture, how to add article (Keystatic / drop MDX + `npm run build && verify`), SITE_URL, deploy steps.
- Update `joyofcare-net/publishing-workflow.md` → point to new repo reality or archive; regenerate category docs from `categories.ts`.
- Update skill `joc-web` (patch: architecture now Astro+MDX, content master = MDX, old txt archive-only, verification script path).
**Verify:** docs contain no 4-category/Odoo-era instructions.

### Task 9.3: Final commit + tag
Commit all, push, tag `v2-astro`. `git status` clean both repos.
**Verify:** fresh clone → `npm ci && npm run build && npm run verify` passes.

---

## Files likely to change (map)

| Area | Files |
|---|---|
| Config | `astro.config.mjs`, `src/content.config.ts`, `keystatic.config.ts`, `wrangler.toml`, `.gitignore`, `package.json` |
| Content | `src/content/articles/*.mdx` (137 regenerated, dupes archived) |
| Layouts | `src/layouts/BaseLayout.astro`, `ArticleLayout.astro` |
| Pages | `src/pages/index.astro`, `blog/index.astro`, `blog/[category]/index.astro`, `blog/[category]/[slug].astro`, + 10 ported .astro, `404.astro` |
| Lib | `src/consts.ts`, `src/lib/categories.ts`, `src/styles/global.css` |
| Public | `public/images/*`, `robots.txt`, `llms.txt`, `_redirects`, favicon |
| Endpoints | `src/pages/blog/feed.xml.ts`, `blog/index.json.ts` |
| Scripts | `joyofcare-net/scripts/migration/*.py`, `joyofcare-web/scripts/verify_site.py` |
| Deleted | `cms/`, `content-source/`, `pages/` (legacy html+blog), `.wrangler/` (untrack), `pages/temp_*.md` |

## Tests / validation summary
1. `python3 txt_to_mdx.py --dry-run` → 137 candidates, all parse.
2. `npx astro check` → 0 errors (content schema).
3. `npm run build` → green; emits N article pages + 11 static pages.
4. `npm run verify` → green (single H1, FAQPage, ISO dates, clean WA URL, no markdown/price/odoo refs, counts equal).
5. `astro preview` spot-check: homepage, 1 service page, hub, category, article, 404.
6. Preview deploy → 200s; production domain → 200s; www after DNS → 200s, no Odoo cookies.
7. Both repos `git status` clean; remotes token-free.

## Risks, tradeoffs, open questions
1. **Final canonical domain** — **DECIDED: `https://new.joyof.care`** (SITE_URL everywhere). Do not reintroduce www.joyofcare.net in canonicals.
2. **Keystatic prod mode on CF Pages** (local-admin vs server output): research at implementation; static+local recommended; in-browser prod editing may require server output + OAuth app + secrets.
3. **Some net articles <800 words or near-dup pairs** (vaksinasi -12/-28): dedupe decisions recorded in canonical-map; content quality pass optional follow-up.
4. **date provenance**: use repo/git dates (all ~2026-09-05) — acceptable; refine later.
5. **Astro 7 vs @keystatic/astro 6 compatibility**: pin versions; `npx astro check` gate will catch.
6. **User-assisted steps**: PAT rotation (DONE 2026-09-06 by user), Cloudflare DNS decision for joyofcare.net (Task 8.3: keep Odoo live OR 301 redirect — user action).
7. **Old SEO equity**: Odoo URLs 301-redirect via `_redirects`; keep sitemap clean; submit new sitemap in Search Console after go-live.
8. **PAT already revoked** — verify no token remains in any git remote/config before pushing.

## Definition of done
- Astro+MDX site on Cloudflare Pages serving homepage, 11 service/utility pages, 12-category blog hub, ~137 clean articles at canonical URLs — all verified 200 by curl.
- Keystatic admin functional (at least locally).
- Zero legacy stacks/content copies; one MDX source of truth; verification script part of workflow.
- Both repos clean & pushed; no secrets in remotes; skill `joc-web` updated.
