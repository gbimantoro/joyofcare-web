# JoyofCare Visual Assets Library

Professional SVG visual assets for the JoyofCare blog and social media. All assets are vector-based (SVG), infinitely scalable, and lightweight.

## Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Primary Green | `#2D9C4A` | Main brand, health, growth |
| Dark Green | `#1A6B30` | Headers, footer |
| Accent Orange | `#FC9000` | CTA buttons, energy |
| Accent Orange Hover | `#E58200` | CTA hover states |
| Light Green | `#7ED957` | Highlights, success |
| Cyan | `#0E7490` | Medical/clinical |
| Text Primary | `#1A1A2E` | Headings |
| Text Secondary | `#475569` | Body text |
| Background | `#F8F9FA` | Page background |

## Typography

- **Headings:** Montserrat (Bold/ExtraBold)
- **Body:** Inter (Regular/Medium/SemiBold)

## Asset Inventory

### 1. Category Thumbnails (`/thumbnails/`)

1200×630px — Standard Open Graph / blog category card size. Use as the hero image for each blog category.

| File | Category | Description |
|------|----------|-------------|
| `healthy-aging.svg` | Lansia Sehat | House with heart on roof, green palette, warm caring theme |
| `pengalaman-pasien.svg` | Pengalaman Pasien | Quote marks, 5-star ratings, testimonial theme, warm orange |
| `studi-luar-negeri.svg` | Studi di Luar Negeri | Globe with travel pins, blue/green palette, international theme |
| `vaksinasi.svg` | Vaksinasi di Rumah | Medical shield with cross, syringe, vaccine vial, cyan palette |

### 2. Infographics (`/infographics/`)

1080×1350px — 4:5 portrait ratio. Optimized for Instagram feed, blog hero, and mobile sharing.

| File | Topic | Structure |
|------|-------|-----------|
| `biaya-panggil-dokter.svg` | Cost comparison clinic vs home | Comparison table + 4 benefit cards + 3 pricing tiers |
| `panduan-merawat-orang-tua.svg` | 10-step care guide | Numbered step cards (1-10) with icon and description |
| `fisioterapi-lansia.svg` | 5 physiotherapy exercises | 5 exercise cards with icon + tips box + CTA |
| `persyaratan-kesehatan-studi-luar-negeri.svg` | Study abroad health checklist | 6 checklist items + countries tag + tip box |
| `vaksinasi-untuk-lansia.svg` | 6 essential vaccines for elderly | Stat banner + 6 vaccine cards with schedule tags |

### 3. Social Media Graphics (`/social/`)

| File | Dimensions | Platform |
|------|------------|----------|
| `whatsapp-share-card.svg` | 1200×630 | WhatsApp status / OG share |
| `instagram-post.svg` | 1080×1080 | Instagram feed / square post |
| `facebook-share-card.svg` | 1200×630 | Facebook share with browser mockup |

## Usage Guidelines

### SVG Optimization

The SVG files are clean and ready to use. For production:

```bash
# Optional: Optimize with svgo
npx svgo --multipass thumbnails/healthy-aging.svg
```

### Converting to Other Formats

```bash
# Convert SVG to PNG (e.g., for social media uploads that require raster)
# Requires librsvg or imagemagick
rsvg-convert -w 1200 -h 630 thumbnails/healthy-aging.svg -o thumbnail.png

# Or with imagemagick
convert -density 300 -background white thumbnails/healthy-aging.svg thumbnail.png
```

### HTML / React Usage

```html
<img src="/assets/blog/healthy-aging.svg" alt="Kategori Lansia Sehat" width="1200" height="630" />
```

```jsx
// React
<img src="/assets/blog/healthy-aging.svg" alt="Kategori Lansia Sehat" className="w-full h-auto" />
```

### Next.js Image Optimization

For Next.js, configure `next.config.js`:

```javascript
module.exports = {
  images: {
    dangerouslyAllowSVG: true,
    contentDispositionType: 'attachment',
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;"
  }
}
```

## Design Principles

1. **Professional medical aesthetic** — clean lines, soft shadows, ample whitespace
2. **Trustworthy color palette** — JoyofCare green primary + orange CTA (Notion-inspired)
3. **Real icons (no stock photos)** — Custom SVG illustrations for scalability
4. **Bilingual accessibility** — Bahasa Indonesia primary, English labels where appropriate
5. **Brand consistency** — Every asset includes JoC wordmark + WhatsApp CTA
6. **Mobile-optimized** — Text sizes legible on small screens
7. **AIO/SEO ready** — All SVGs include `<title>` and `<desc>` tags for accessibility

## WhatsApp CTA (Standard)

Every CTA references the official contact:

```
Nomor: 08811-118-911
Link:  https://api.whatsapp.com/send/?phone=628811118911&text=Hi,%20saya%20tahu%20dari%20web.%20Apa%20saja%20layanan%20Joy%20of%20Care?
```

## File Locations

- **Master:** `/home/gobeam/Projects/joyofcare-net/visual-assets/`
- **Web mirror:** `/home/gobeam/Projects/joyofcare-web/assets/`
  - Blog thumbnails: `/assets/blog/`
  - Infographics: `/assets/infographics/`
  - Social graphics: `/assets/social/`

## Maintenance

When updating brand colors or fonts:
1. Update all SVG `<defs>` and gradient stops
2. Replace wordmark text where applicable
3. Re-export or re-sync to both directory locations
4. Update index.json with any new assets