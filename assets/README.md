# Joy of Care Visual Assets Library (v2.0 Upgraded)

Human-centric, professional SVG visual assets for the Joy of Care blog, website, and social media. All assets are self-contained vector-based SVGs with embedded high-resolution photography and official Joy of Care brand marks (`joc_icon.png` and `joc_long.png`).

---

## 1. Brand Guidelines & Aesthetics

| Design Token | Value | Description |
|---|---|---|
| **Primary Emerald** | `#00bf63` | Joy of Care signature vitality & health green |
| **Deep Forest Green** | `#007A3D` | High-contrast headings, authority, trust |
| **Accent Warm Orange** | `#FC9000` | CTA buttons, phone icons, key action items |
| **Clinical Teal** | `#0E7490` | Diagnostic, medical rigor, and milestone markers |
| **Calming Background** | `#EFFBF4` / `#F8FCF9` | Anxiety-reducing soft medical green gradient |
| **Primary Text (Dark)** | `#0F172A` / `#1A1A2E` | Deep slate near-black for maximum readability |
| **Muted Text** | `#475569` | Secondary descriptions and clinical labels |

### Typography & 8px Grid
- **Headings:** Montserrat (800 Bold / ExtraBold) with -1px tracking
- **Body & Captions:** Inter (Medium 500, SemiBold 600, Bold 700)
- **Grid:** All cards, margins, paddings, and line-heights are aligned to an 8px grid system.

### The 3C Rule & Human-Centric Imagery
1. **Clarity:** Reduced visual clutter; 3-5 word high-contrast titles.
2. **Contrast:** Strong typographic hierarchy against a calming, clean background.
3. **Curiosity & Empathy:** Abstract shapes replaced with empathetic real photography (therapists guiding patients, smiling seniors, registered nurses, doctors visiting home).
4. **Official Logo Integration:** Each visual asset embeds the official `joc_long.png` brand logo and `joc_icon.png` badge for verified clinical authenticity.

---

## 2. Asset Inventory

### A. Category Thumbnails (`/assets/thumbnails/` & `/assets/blog/`)
- **Dimensions:** 1200 × 630 px (1.91:1 ratio, Open Graph and Twitter Card standard)
- **Structure:** 12 Categories × 3 Variants = **36 SVGs** + 12 Category Primary Banners + 6 Legacy Upgrades = **54 Assets**
- **Variants:**
  - **Variant 1 (Brand Hero):** Punchy service promise, official STR/SIP verification pills, warm photography card, CTA.
  - **Variant 2 (Benefit Scene):** Reassurance, patient outcome, and family peace-of-mind focus.
  - **Variant 3 (Process Steps):** 4-step structured clinical protocol timeline overlay.

| Category | Primary Slug | Photo Subject | Key Benefit Focus |
|---|---|---|---|
| Fisioterapi di Rumah | `fisioterapi-rumah.svg` | Terapis membimbing pasien stroke | Pemulihan stroke & gerak sendi mandiri |
| Perawatan Lansia | `perawatan-lansia.svg` | Perawat mendampingi oma lansia | Pendampingan geriatri penuh kasih di rumah |
| Panggil Dokter ke Rumah | `panggil-dokter.svg` | Dokter visit memeriksa pasien | Respon cepat 1-2 jam & resep digital |
| Penyakit Parkinson | `parkinson.svg` | Pendampingan gerak pasien Parkinson | Protokol saraf EPDA & cegah risiko jatuh |
| Studi Luar Negeri | `studi-luar-negeri.svg` | Konsultasi MCU mahasiswa & dokter | Form universitas & vaksinasi internasional |
| Osteoporosis | `osteoporosis.svg` | Lansia aktif latihan beban & tulang | Skrining FRAX & infus kalsium di rumah |
| Antar Jemput RS (TransCare) | `antar-jemput-rs.svg` | Armada ambulans & perawat jaga | Transportasi medis aman dengan monitor vital |
| Perawat Homecare | `perawat-homecare.svg` | Perawat medis STR merawat luka | Asuhan keperawatan 24 jam & steril |
| Home Lab & Cek Darah | `home-lab.svg` | Pengambilan darah flebotomi di rumah | Hasil uji lab akreditasi 24 jam digital |
| Vaksinasi di Rumah | `vaksinasi-rumah.svg` | Vaksinasi lansia & keluarga | Jaminan cold-chain BPOM & tenaga medis |
| Infus Vitamin & Imun | `infus-vitamin.svg` | Infus vitamin booster stamina | Penyerapan seluler 100% aman terdaftar |
| Kesehatan Umum & Akupuntur | `kesehatan-umum.svg` | Tindakan akupuntur medis titik sendi | Redakan nyeri kronis alami jarum steril |

### B. Infografis Edukatif (`/assets/infographics/`)
- **Dimensions:** 1080 × 1350 px (4:5 vertical portrait, Instagram & mobile article embed standard)
- **Coverage:** Generated for **1 out of 3 articles** across the entire blog (48 articles × 2 naming aliases + 5 category pillars = **101 files**)
- **Content Flow:**
  1. Top Header with `joc_long` official logo and 24/7 WhatsApp Hotline (`08811-118-911`)
  2. Category Badge with `joc_icon` and punchy topic title
  3. Hero Clinical Stat card (98% kepuasan pasien & bimbingan dokter berizin)
  4. 4-Langkah Timeline connected step cards (Evaluasi, Rencana, Sesi Terapi, Monitoring)
  5. Rekomendasi Tim Medis (Clinical advice & family warning signs)
  6. Footer Hotline CTA Banner with `joc_icon`

---

## 3. Web & Build Integration

All assets are located in `/home/gobeam/Projects/joyofcare-web/assets/` and symlinked to `/home/gobeam/Projects/joyofcare-web/public/assets`.
- During `npm run build`, Astro automatically bundles them into `dist/assets/`.
- During `python3 scripts/build_articles.py`, infographics are automatically identified and embedded into article HTML bodies.
