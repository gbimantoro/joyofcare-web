# JoyofCare Blog Visual Assets

## Overview
Visual assets for the JoyofCare blog and digital products (HR Wellness Toolkit & Caregiver Kit).

## Asset Inventory

### Category Thumbnails (12 files)
**Location:** `thumbnails/`
**Size:** 800×450px
**Format:** PNG with SVG icons

| Category | File | Articles |
|----------|------|----------|
| Perawatan Lansia | perawatan-lansia.png | 38 |
| Fisioterapi Rumah | fisioterapi-rumah.png | 23 |
| Panggil Dokter | panggil-dokter.png | 18 |
| Parkinson | parkinson.png | 11 |
| Studi Luar Negeri | studi-luar-negeri.png | 11 |
| Osteoporosis | osteoporosis.png | 9 |
| Antar Jemput RS | antar-jemput-rs.png | 6 |
| Vaksinasi Rumah | vaksinasi-rumah.png | 5 |
| Infus Vitamin | infus-vitamin.png | 5 |
| Perawat Homecare | perawat-homecare.png | 5 |
| Kesehatan Umum | kesehatan-umum.png | 3 |
| Home Lab | home-lab.png | 3 |

### Article Infographics (123 files)
**Location:** `infographics/`
**Size:** 800×1000px
**Format:** PNG
**Coverage:** Every 3rd article (1/3 of all articles)

Each infographic includes:
- Category-colored header
- Article title
- Numbered key points (3 items)
- CTA section with WhatsApp number
- Joy of Care branding footer

## Design System

### Colors (per category)
- Perawatan Lansia: #4CAF50 (Green)
- Fisioterapi Rumah: #2196F3 (Blue)
- Panggil Dokter: #E91E63 (Pink)
- Parkinson: #9C27B0 (Purple)
- Studi Luar Negeri: #FF9800 (Orange)
- Osteoporosis: #795548 (Brown)
- Antar Jemput RS: #F44336 (Red)
- Vaksinasi Rumah: #00BCD4 (Cyan)
- Infus Vitamin: #FF5722 (Deep Orange)
- Perawat Homecare: #607D8B (Blue Grey)
- Kesehatan Umum: #E91E63 (Pink)
- Home Lab: #3F51B5 (Indigo)

### Typography
- Font: Inter (Google Fonts)
- Weights: 400, 600, 700, 800

### Brand Elements
- Primary: #00bf63 (Joy of Care Green)
- Accent: #FC9000 (Orange)
- WhatsApp: 08811-118-911

## Usage in Astro

### Category Thumbnails
```astro
---
import { CATEGORIES } from '../lib/categories';
---
{CATEGORIES.map(cat => (
  <img src={`/assets/blog/thumbnails/${cat.slug}.png`} alt={cat.label} />
))}
```

### Article Infographics
```astro
---
const infographicPath = `/assets/blog/infographics/${slug}.png`;
---
<img src={infographicPath} alt={title} />
```

## Regenerating Assets

```bash
cd /home/gobeam/Projects/joyofcare-web
source .venv/bin/activate
python3 scripts/gen_fast.py
```

## BIMOS Team Integration

See `BIMOS_TASK_BOARD.md` for:
- Agent pack integration status
- Next phase tasks (HR Toolkit & Caregiver Kit assets)
- Working rules and compliance requirements

## Asset Credits

- **Generated:** 6 September 2026
- **Tool:** Playwright + Chromium headless
- **Design:** BIMOS Visual Designer
- **Approved:** [Pending dr. Bimo review]

---

For questions or updates, contact the BIMOS team lead.
