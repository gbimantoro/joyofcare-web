# JoyofCare 60-Day Campaign Visual Templates

Reusable SVG visual templates for the 60-day social media campaign. Each template is fully editable, brand-consistent, and optimized for its target platform.

## Brand Standards (Applied Across All Templates)

| Token | Hex | Usage |
|-------|-----|-------|
| Primary Green | `#2D9C4A` | Headers, primary brand color |
| Dark Green | `#1A6B30` | Gradient end, footer, dark sections |
| Accent Orange | `#FC9000` | CTA buttons, accents, click-bait hooks |
| Accent Hover | `#E58200` | CTA hover, gradient end |
| Light Green | `#7ED957` | Highlights, success |
| WhatsApp Green | `#25D366` | WhatsApp icons only |
| YouTube Red | `#FF0000` | YouTube Shorts badge only |

**Typography:** Montserrat (headings, bold/extra-bold) + Inter (body, regular/medium/semi-bold).

**Logo:** Joy wordmark (bold green) + of Care (regular dark/white). Heart icon in green/white circle.

## Template Inventory

### 1. `instagram-post-template.svg` (1080×1080)

**Use:** Single Instagram feed post (square)

**Editable areas:**
- Category badge (top, white pill)
- Hero icon area (large circular icon)
- 2-line headline (Montserrat 48px bold)
- 1-line subtitle
- 6 bullet points (2-column layout)
- CTA heading + subtext + WhatsApp number

**Design notes:** Green gradient background, soft decorative blobs, white content card with subtle shadow, orange CTA card at bottom.

### 2. `instagram-carousel-slide-1.svg` (1080×1350)

**Use:** Cover slide (Slide 1) of Instagram carousel

**Editable areas:**
- Slide number badge (top right)
- Large "1 / N" number badge
- Hero icon
- 2-line headline
- 1-line description
- 3 benefit promise boxes (white-on-green checkmark pills)
- CTA strip with "SWIPE →"

**Design notes:** High-contrast cover that hooks viewers and encourages swiping.

### 3. `instagram-carousel-slide-content.svg` (1080×1350)

**Use:** Content slides (Slides 2-N) of Instagram carousel

**Editable areas:**
- Green header band with slide number + section title
- Icon area (large circular icon)
- Main title + subtitle
- 3 bullet points
- "PRO TIP" highlight box (orange bordered)
- 2 stat callout boxes (green tinted)

**Design notes:** Reusable for any content slide — just swap icons, text, and stats.

### 4. `instagram-reel-cover.svg` (1080×1920)

**Use:** Instagram Reel cover thumbnail (vertical 9:16)

**Editable areas:**
- Reel duration badge (top right)
- 3-line massive headline (120px bold)
- Hook subtitle card (white on green)
- 3-point "what you'll learn" list
- Large WhatsApp CTA card with prominent icon
- Decorative play button hint

**Design notes:** Bold, scroll-stopping design with maximum text size for thumbnail visibility.

### 5. `facebook-post-template.svg` (1200×630)

**Use:** Facebook post / shareable link preview

**Editable areas:**
- Category badge
- 2-line headline (Montserrat 44px)
- 1-line subtitle
- 3 bullet points
- Right-side illustration card with icon + stats
- Bottom WhatsApp CTA pill

**Design notes:** Two-column layout (text left, illustration right), optimized for link share preview.

### 6. `youtube-shorts-thumbnail.svg` (1080×1920)

**Use:** YouTube Shorts thumbnail (vertical 9:16)

**Editable areas:**
- Shorts badge with red play icon
- Massive "WOW!" hook text
- 4-line super-bold headline
- 5 numbered bullet points in white card
- Brand card with WhatsApp CTA

**Design notes:** Click-bait style with maximum contrast. Orange gradient background (stands out in feed), white text with text shadow, big numbered list.

### 7. `twitter-x-image.svg` (1200×675)

**Use:** Twitter/X timeline image (16:9)

**Editable areas:**
- Brand top-left
- X badge top-right
- 3-line headline (Montserrat 64px)
- Right-side icon in circle
- 4 hashtag pills
- Small WhatsApp CTA strip

**Design notes:** Clean, minimal, dark green gradient with subtle grid pattern. Optimized for timeline preview without overpowering tweet text.

## How to Use These Templates

### Option A: Edit SVG Directly

Open the `.svg` file in any vector editor (Figma, Inkscape, Adobe Illustrator) and edit:
- Text elements (look for `font-family="Inter"` or `Montserrat`)
- Replace icon paths
- Adjust colors via `<stop stop-color="..."/>` in gradients

### Option B: Convert to Editable Image

```bash
# Convert to PNG for editing in Canva/Photoshop
rsvg-convert -w 1080 -h 1080 instagram-post-template.svg -o instagram-post.png

# Or use imagemagick
convert -density 150 -background white instagram-post-template.svg instagram-post.png
```

### Option C: Programmatic Generation

Use the templates as base SVGs and modify via Python/Node scripts:

```python
import re

with open('instagram-post-template.svg', 'r') as f:
    svg = f.read()

# Replace headline
svg = svg.replace('Headline Utama', 'Tips Sehat Lansia')
svg = svg.replace('Disini (Maks 2 Baris)', 'yang Wajib Diketahui')

with open('output.svg', 'w') as f:
    f.write(svg)
```

## Customization Checklist Per Post

For each campaign post, edit these fields:

- [ ] **Category badge** — which category (Lansia, Fisioterapi, etc.)
- [ ] **Headline** — 2-line hook (max ~30 chars per line)
- [ ] **Subtitle** — 1-line context
- [ ] **Bullet points** — 3-6 key takeaways
- [ ] **CTA text** — what action to take
- [ ] **WhatsApp number** — already set to 08811-118-911 (do not change)
- [ ] **Hashtags** — at bottom or on card
- [ ] **Icon** — swap to match topic if needed

## Content Calendar Integration

These templates align with the 60-day campaign themes defined by JoC Strategist:

| Week | Theme | Primary Template |
|------|-------|------------------|
| 1-2 | Perawatan Lansia | instagram-post + carousel |
| 3-4 | Fisioterapi Rumah | instagram-post + reel |
| 5-6 | Panggil Dokter | instagram-post + facebook |
| 7-8 | Parkinson awareness | carousel (educational) |
| 9-10 | Studi Luar Negeri | carousel + twitter |
| 11-12 | Osteoporosis | instagram-post + carousel |
| 13-14 | Vaksinasi & Home Lab | carousel + facebook |
| 15-16 | Infus Vitamin | instagram-post |
| 17-18 | Antar Jemput RS | carousel |
| 19-20 | Recap & engagement | youtube + reel |

## File Locations

- **Master:** `/home/gobeam/Projects/joyofcare-net/social-media-campaign/templates/`
- **Web mirror:** `/home/gobeam/Projects/joyofcare-web/assets/social-media-campaign/`

## Asset Stats

- Total templates: 7 (covering 6 platform formats + carousel content variant)
- Total size: ~40 KB (extremely lightweight)
- All scalable to any resolution without quality loss