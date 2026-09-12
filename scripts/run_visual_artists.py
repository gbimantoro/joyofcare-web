#!/usr/bin/env python3
"""
Joy of Care - Visual Artists Production Runner & Queue Manager
Manages the 4-track Visual Artist Team for 352 article photojournalism prompts.
"""

import os
import sys
import json
import glob
import re
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

WEB_DIR = Path("/home/gobeam/Projects/joyofcare-web")
NET_DIR = Path("/home/gobeam/Projects/joyofcare-net")
ARTICLES_MDX_DIR = WEB_DIR / "src/content/articles"
IMAGES_DIR = WEB_DIR / "assets/images/articles"
PROMPTS_JSON = IMAGES_DIR / "image-prompts-nanobanana.json"
MANIFEST_JSON = IMAGES_DIR / "production_manifest.json"

# 4 Specialized Visual Artist Tracks
ARTIST_TRACKS = {
    "artist-1-geriatric": {
        "name": "Visual Artist 1: Geriatric & Home Nursing",
        "description": "Elderly comfort, compassionate bedside care, gentle nursing, authentic home routines in Jabodetabek",
        "categories": ["perawatan-lansia", "perawat-homecare"],
        "lead": "Sister Winda (Jabodetabek Senior Nurse Persona)"
    },
    "artist-2-doctor": {
        "name": "Visual Artist 2: Doctor Home-Visit & IV Therapy",
        "description": "Physician home consultations, diagnostic equipment, intravenous vitamin therapy, sterile medical procedures",
        "categories": ["panggil-dokter", "infus-vitamin", "vaksinasi-rumah"],
        "lead": "Dr. Rian (Attending Home-Care Physician Persona)"
    },
    "artist-3-rehab": {
        "name": "Visual Artist 3: Neuro-Rehab & Physical Therapy",
        "description": "Gait training, joint mobilization, Parkinson movement support, post-stroke motor rehabilitation",
        "categories": ["fisioterapi-rumah", "parkinson", "osteoporosis"],
        "lead": "Fisioterapis Budi (Clinical Rehab Specialist Persona)"
    },
    "artist-4-escort": {
        "name": "Visual Artist 4: Medical Escort, Lab & Environmental",
        "description": "Ambulance transfers, airport wheelchair escorts, home phlebotomy & lab sampling, N95 respiratory defense",
        "categories": ["antar-jemput-rs", "home-lab", "kesehatan-umum", "studi-luar-negeri", "kesehatan-lingkungan"],
        "lead": "Paramedis Dani (Emergency & Logistics Lead Persona)"
    }
}

def get_track_for_category(category):
    for track_id, info in ARTIST_TRACKS.items():
        if category in info["categories"]:
            return track_id, info
    return "artist-4-escort", ARTIST_TRACKS["artist-4-escort"]

def load_prompts():
    if not PROMPTS_JSON.exists():
        raise FileNotFoundError(f"Prompts file not found at {PROMPTS_JSON}")
    with open(PROMPTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def load_or_init_manifest():
    prompts = load_prompts()
    manifest = {}

    if MANIFEST_JSON.exists():
        try:
            with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load existing manifest: {e}. Reinitializing.")

    articles_manifest = manifest.get("articles", {})
    now_iso = datetime.now(timezone.utc).isoformat()

    for slug, data in prompts.items():
        category = data.get("category", "kesehatan-umum")
        track_id, track_info = get_track_for_category(category)

        webp_file = IMAGES_DIR / f"{slug}.webp"
        jpg_file = IMAGES_DIR / f"{slug}.jpg"
        svg_file = IMAGES_DIR / f"{slug}.svg"

        existing_entry = articles_manifest.get(slug, {})
        existing_type = existing_entry.get("image_type")

        # Distinguish between real photojournalism vs baseline card
        if existing_type == "photojournalism" or (webp_file.exists() and webp_file.stat().st_size > 100000):
            image_type = "photojournalism"
            status = "completed"
            output_image = f"/assets/images/articles/{slug}.webp"
        elif webp_file.exists():
            image_type = "baseline_card"
            status = "baseline_ready"
            output_image = f"/assets/images/articles/{slug}.webp"
        elif svg_file.exists():
            image_type = "vector_svg"
            status = "pending_render"
            output_image = f"/assets/images/articles/{slug}.svg"
        else:
            image_type = "none"
            status = "pending"
            output_image = None

        articles_manifest[slug] = {
            "slug": slug,
            "title": data.get("title", slug),
            "category": category,
            "primaryKeyword": data.get("primaryKeyword", ""),
            "artist_track": track_id,
            "artist_name": track_info["name"],
            "status": status,
            "image_type": image_type,
            "aspectRatio": data.get("aspectRatio", "16:9"),
            "style": data.get("style", "journalistic photography"),
            "imagePrompt": data.get("imagePrompt", ""),
            "featuredImage": output_image or data.get("featuredImage"),
            "has_photo_webp": webp_file.exists(),
            "has_photo_jpg": jpg_file.exists(),
            "has_vector_svg": svg_file.exists(),
            "updated_at": existing_entry.get("updated_at", now_iso)
        }

    manifest["schema_version"] = "1.1.0"
    manifest["updated_at"] = now_iso
    manifest["total_articles"] = len(prompts)
    manifest["articles"] = articles_manifest

    save_manifest(manifest)
    return manifest

def save_manifest(manifest):
    articles = manifest.get("articles", {})
    photo_completed = sum(1 for a in articles.values() if a.get("image_type") == "photojournalism")
    baseline_ready = sum(1 for a in articles.values() if a.get("image_type") == "baseline_card")
    pending = sum(1 for a in articles.values() if a.get("image_type") not in ("photojournalism", "baseline_card"))

    track_stats = {}
    for t_id, t_info in ARTIST_TRACKS.items():
        t_articles = [a for a in articles.values() if a.get("artist_track") == t_id]
        track_stats[t_id] = {
            "name": t_info["name"],
            "total": len(t_articles),
            "photojournalism": sum(1 for a in t_articles if a.get("image_type") == "photojournalism"),
            "baseline_ready": sum(1 for a in t_articles if a.get("image_type") == "baseline_card"),
            "pending": sum(1 for a in t_articles if a.get("image_type") not in ("photojournalism", "baseline_card")),
        }

    manifest["summary"] = {
        "total": len(articles),
        "photojournalism_completed": photo_completed,
        "baseline_ready": baseline_ready,
        "pending": pending,
        "coverage_rate": f"{((photo_completed + baseline_ready) / len(articles) * 100):.1f}%" if articles else "0%",
        "photojournalism_rate": f"{(photo_completed / len(articles) * 100):.1f}%" if articles else "0%",
        "tracks": track_stats
    }

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def print_summary():
    manifest = load_or_init_manifest()
    summary = manifest["summary"]

    print("\n" + "=" * 78)
    print("🎨 JOY OF CARE - VISUAL ARTISTS PRODUCTION DASHBOARD")
    print("=" * 78)
    print(f"Total Articles       : {summary['total']}")
    print(f"Photojournalism Done : {summary['photojournalism_completed']} ({summary['photojournalism_rate']})")
    print(f"16:9 WebP Baselines  : {summary['baseline_ready']}")
    print(f"Total 16:9 Coverage  : {summary['coverage_rate']}")
    print("-" * 78)

    for t_id, stats in summary["tracks"].items():
        bar_len = 25
        total = stats["total"]
        photo_pct = (stats["photojournalism"] / total) if total > 0 else 0
        base_pct = (stats["baseline_ready"] / total) if total > 0 else 0

        p_filled = int(round(photo_pct * bar_len))
        b_filled = int(round(base_pct * bar_len))
        remain = max(0, bar_len - p_filled - b_filled)
        bar = "█" * p_filled + "▒" * b_filled + "░" * remain

        print(f"\n📌 {stats['name']}")
        print(f"   Visual Meter: [{bar}] Total: {total}")
        print(f"   Photos: {stats['photojournalism']} | Baselines: {stats['baseline_ready']} | Pending: {stats['pending']}")

    print("\n" + "=" * 78)

def export_tracks():
    manifest = load_or_init_manifest()
    articles = manifest["articles"]

    tracks_dir = IMAGES_DIR / "tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)

    for t_id, t_info in ARTIST_TRACKS.items():
        track_articles = {
            slug: data for slug, data in articles.items() if data.get("artist_track") == t_id
        }
        track_file = tracks_dir / f"{t_id}.json"
        with open(track_file, "w", encoding="utf-8") as f:
            json.dump({
                "artist_track": t_id,
                "artist_name": t_info["name"],
                "description": t_info["description"],
                "lead_persona": t_info["lead"],
                "total_articles": len(track_articles),
                "articles": track_articles
            }, f, indent=2, ensure_ascii=False)
        print(f"✓ Exported {len(track_articles)} prompts for {t_info['name']} -> {track_file}")

def render_baselines():
    print("🎨 Rendering high-resolution 16:9 WebP baseline cards using Sharp...")
    node_script = """
    const sharp = require('/home/gobeam/Projects/joyofcare-web/node_modules/sharp');
    const fs = require('fs');
    const path = require('path');

    const manifestPath = '/home/gobeam/Projects/joyofcare-web/assets/images/articles/production_manifest.json';
    const imagesDir = '/home/gobeam/Projects/joyofcare-web/assets/images/articles';
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

    async function run() {
      let count = 0;
      for (const [slug, item] of Object.entries(manifest.articles)) {
        if (item.image_type === 'photojournalism') {
          continue; // Preserve actual photojournalism
        }
        const svgPath = path.join(imagesDir, `${slug}.svg`);
        const webpPath = path.join(imagesDir, `${slug}.webp`);
        if (fs.existsSync(svgPath)) {
          const svgBuf = fs.readFileSync(svgPath);
          await sharp(svgBuf)
            .resize(1280, 720)
            .webp({ quality: 90 })
            .toFile(webpPath);
          count++;
          if (count % 50 === 0) {
            console.log(`  Processed ${count} WebP cards...`);
          }
        }
      }
      console.log(`✅ Finished rendering ${count} baseline WebP cards (1280x720 16:9).`);
    }
    run().catch(console.error);
    """
    res = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)
    load_or_init_manifest()

def ingest_image(source_path, slug):
    if not os.path.exists(source_path):
        print(f"Error: Source image {source_path} does not exist.")
        return False

    manifest = load_or_init_manifest()
    try:
        im = Image.open(source_path)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")

        webp_out = IMAGES_DIR / f"{slug}.webp"
        im.save(webp_out, "WEBP", quality=88, method=6)

        jpg_out = IMAGES_DIR / f"{slug}.jpg"
        im.save(jpg_out, "JPEG", quality=90, optimize=True)

        now_iso = datetime.now(timezone.utc).isoformat()
        if slug in manifest["articles"]:
            manifest["articles"][slug]["status"] = "completed"
            manifest["articles"][slug]["image_type"] = "photojournalism"
            manifest["articles"][slug]["featuredImage"] = f"/assets/images/articles/{slug}.webp"
            manifest["articles"][slug]["has_photo_webp"] = True
            manifest["articles"][slug]["has_photo_jpg"] = True
            manifest["articles"][slug]["updated_at"] = now_iso
            save_manifest(manifest)

        update_single_article_mdx(slug, f"/assets/images/articles/{slug}.webp")
        print(f"✓ Ingested photojournalism {slug}: WebP ({webp_out.stat().st_size} B), JPG ({jpg_out.stat().st_size} B)")
        return True
    except Exception as e:
        print(f"Error ingesting image for {slug}: {e}")
        return False

def update_single_article_mdx(slug, image_url):
    mdx_file = ARTICLES_MDX_DIR / f"{slug}.mdx"
    if not mdx_file.exists():
        return False

    with open(mdx_file, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    fm = parts[1]
    body = parts[2]

    if re.search(r"^featuredImage:", fm, re.MULTILINE):
        fm = re.sub(r"^featuredImage:.*$", f"featuredImage: {image_url}", fm, flags=re.MULTILINE)
    else:
        fm += f"\nfeaturedImage: {image_url}"

    with open(mdx_file, "w", encoding="utf-8") as f:
        f.write(f"---{fm}---{body}")
    return True

def sync_all_mdx():
    manifest = load_or_init_manifest()
    synced = 0
    for slug, entry in manifest["articles"].items():
        if entry.get("has_photo_webp"):
            image_url = f"/assets/images/articles/{slug}.webp"
            if update_single_article_mdx(slug, image_url):
                synced += 1
    print(f"✓ Synced {synced} MDX articles to use 16:9 WebP images.")

def batch_ingest_dir(dir_path):
    p = Path(dir_path)
    if not p.exists():
        print(f"Directory {dir_path} does not exist.")
        return

    images = list(p.glob("*.jpg")) + list(p.glob("*.jpeg")) + list(p.glob("*.png")) + list(p.glob("*.webp"))
    manifest = load_or_init_manifest()
    matched = 0

    for img in images:
        base = img.stem
        for slug in manifest["articles"].keys():
            if base == slug or base.startswith(slug) or slug in base:
                if ingest_image(str(img), slug):
                    matched += 1
                break
    print(f"✓ Batch ingested {matched} images from {dir_path}")

def main():
    parser = argparse.ArgumentParser(description="Joy of Care Visual Artists Runner")
    parser.add_argument("--status", "--summary", action="store_true", help="Print production dashboard")
    parser.add_argument("--export-tracks", action="store_true", help="Export individual artist prompt files")
    parser.add_argument("--render-baselines", action="store_true", help="Render high-res 16:9 WebP baselines for all articles")
    parser.add_argument("--ingest", help="Ingest a generated image path")
    parser.add_argument("--slug", help="Article slug for the ingested image")
    parser.add_argument("--batch-ingest", help="Batch ingest images from directory")
    parser.add_argument("--sync-mdx", action="store_true", help="Sync completed images to MDX articles")

    args = parser.parse_args()

    if args.render_baselines:
        render_baselines()
        sync_all_mdx()
        print_summary()
    elif args.export_tracks:
        export_tracks()
    elif args.ingest and args.slug:
        ingest_image(args.ingest, args.slug)
    elif args.batch_ingest:
        batch_ingest_dir(args.batch_ingest)
    elif args.sync_mdx:
        sync_all_mdx()
    else:
        print_summary()

if __name__ == "__main__":
    main()
