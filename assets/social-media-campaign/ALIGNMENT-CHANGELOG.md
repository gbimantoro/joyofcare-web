# JoyofCare Visual Templates Alignment Changelog

## What Changed

User feedback: "Learn from instagram and fb pages joyof.care and align with visual templates."

### Direct Page Access Limitation

Instagram and Facebook both completely block automated scraping (even with proper crawler UAs like `facebookexternalhit/1.1`). Direct visual access to the actual `@joyof.care` feed content was not possible in this environment.

### What We Aligned (Verified from Brand Assets)

We aligned templates using **directly sampled colors from the official logo** (`/home/gobeam/Projects/joyofcare-web/pages/images/joc_long.png`) and **the user-confirmed handle `@joyof.care`**.

## Color Updates

### Before (from `joc-branding.json`)
- Primary Green: `#2D9C4A` (muted forest green)
- Dark Green: `#1A6B30` (dark forest)
- Accent Orange: `#FC9000` ✓ (already matched)

### After (sampled from actual `joc_long.png`)
- Primary Green: `#00bf63` (vibrant kelly/medium spring green) — matches logo
- Dark Green: `#007A3D` (deeper kelly for contrast)
- Accent Orange: `#FC9000` ✓ (no change, matches `#fc9001` to within 1-bit)
- Light Green: `#7ED957` ✓ (already matched)

**Files updated (8 SVG files + 2 docs):**
- `instagram-post-template.svg`
- `instagram-carousel-slide-1.svg`
- `instagram-carousel-slide-content.svg`
- `instagram-reel-cover.svg`
- `facebook-post-template.svg`
- `youtube-shorts-thumbnail.svg`
- `twitter-x-image.svg`
- (carousel slides updated as well)
- `README.md` and `index.json` metadata

## Handle Updates

### Inconsistency Discovered

Three sources disagreed on the official handle:

| Source | Instagram |
|--------|-----------|
| `joyofcare-seo-geo-aio-audit.md` | `@joyof.care` (with dot) |
| `joc-branding.json` | `@joyof.care` (with dot) |
| Live `index.html` JSON-LD + footer link | `@joyofcare` (no dot) |

### Resolution

User-confirmed: **`@joyof.care`** (with dot) is correct.

The live website's `index.html` has incorrect schema.org `sameAs` and footer link — these should be fixed by JoC Tech in a separate task.

### Changes Applied

Added `@joyof.care` to the footer hashtag line of every social media template:

```diff
- #JoyOfCare #KesehatanDiRumah #LansiaSehat
+ #JoyOfCare #KesehatanDiRumah @joyof.care #LansiaSehat
```

Affected templates:
- `instagram-post-template.svg`
- `instagram-carousel-slide-1.svg`
- `instagram-carousel-slide-content.svg`
- `instagram-reel-cover.svg`
- `facebook-post-template.svg`
- `youtube-shorts-thumbnail.svg`
- `twitter-x-image.svg`

## Engagement Considerations

The audit reported "Instagram Active but low engagement" and Facebook "2 talking about this (very low)". To help drive engagement on the new `@joyof.care` posts using these templates, we:

1. ✅ Added `@joyof.care` in every footer (handle recognition + word-of-mouth)
2. ✅ Kept bold, scroll-stopping designs (orange CTAs, large typography)
3. ✅ Included "Swipe →" prompts in carousel covers
4. ✅ Made the YouTube Shorts thumbnail orange (different from feed — stands out)

## Known Limitations

1. **Cannot directly access actual `@joyof.care` posts** to see exact real-world font choices, photo styles, filter usage, etc. Instagram and Facebook fully block scraping.
2. **Cannot verify** whether they use specific photo filters, brand watermarks, or recurring graphic elements beyond the logo and verified colors.
3. **Should re-verify** after JoC Strategist completes the 60-day content calendar — campaign-specific variations may need additional tweaks.

## Recommended Next Steps

1. **JoC Tech** — Fix the live `index.html` line 94 + 490 to use `@joyof.care` (with dot) in JSON-LD `sameAs` and footer link.
2. **JoC Strategist** — When building the 60-day calendar, use these templates as starting point. Pull 3-5 most-engaging posts from `@joyof.care` directly via browser) to confirm any visual patterns we couldn't programmatically detect.
3. **JoC Visual** — Can produce additional templates (Stories, Highlight covers, Profile banner) on request, using these updated brand specs.

## Files Modified

- All 7 SVG templates in `/home/gobeam/Projects/joyofcare-net/social-media-campaign/templates/`
- Mirrored to `/home/gobeam/Projects/joyofcare-web/assets/social-media-campaign/`
- `README.md` and `index.json` updated with new color metadata