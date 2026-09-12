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
from datetime import datetime
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
    updated = False

    for slug, data in prompts.items():
        category = data.get("category", "kesehatan-umum")
        track_id, track_info = get_track_for_category(category)

        # Check existing image files on disk
        webp_file = IMAGES_DIR / f"{slug}.webp"
        jpg_file = IMAGES_DIR / f"{slug}.jpg"
        svg_file = IMAGES_DIR / f"{slug}.svg"

        existing_entry = articles_manifest.get(slug)
        current_status = existing_entry.get("status", "pending") if existing_entry else "pending"
        output_image = existing_entry.get("output_image") if existing_entry else None

        if webp_file.exists():
            current_status = "completed"
            output_image = f"/assets/images/articles/{slug}.webp"
        elif jpg_file.exists():
            current_status = "completed"
            output_image = f"/assets/images/articles/{slug}.jpg"
        elif not output_image:
            output_image = f"/assets/images/articles/{slug}.svg" if svg_file.exists() else None

        articles_manifest[slug] = {
            "slug": slug,
            "title": data.get("title", slug),
            "category": category,
            "primaryKeyword": data.get("primaryKeyword", ""),
            "artist_track": track_id,
            "artist_name": track_info["name"],
            "status": current_status,
            "aspectRatio": data.get("aspectRatio", "16:9"),
            "style": data.get("style", "journalistic photography"),
            "imagePrompt": data.get("imagePrompt", ""),
            "featuredImage": output_image or data.get("featuredImage"),
            "has_photo_webp": webp_file.exists(),
            "has_photo_jpg": jpg_file.exists(),
            "has_vector_svg": svg_file.exists(),
            "updated_at": existing_entry.get("updated_at") if existing_entry else datetime.utcnow().isoformat()
        }

    manifest["schema_version"] = "1.0.0"
    manifest["updated_at"] = datetime.utcnow().isoformat()
    manifest["total_articles"] = len(prompts)
    manifest["articles"] = articles_manifest

    save_manifest(manifest)
    return manifest

def save_manifest(manifest):
    # Recalculate summary stats
    articles = manifest.get("articles", {})
    completed = sum(1 for a in articles.values() if a.get("status") == "completed")
    pending = sum(1 for a in articles.values() if a.get("status") == "pending")
    failed = sum(1 for a in articles.values() if a.get("status") == "failed")

    track_stats = {}
    for t_id, t_info in ARTIST_TRACKS.items():
        t_articles = [a for a in articles.values() if a.get("artist_track") == t_id]
        track_stats[t_id] = {
            "name": t_info["name"],
            "total": len(t_articles),
            "completed": sum(1 for a in t_articles if a.get("status") == "completed"),
            "pending": sum(1 for a in t_articles if a.get("status") == "pending"),
            "failed": sum(1 for a in t_articles if a.get("status") == "failed"),
        }

    manifest["summary"] = {
        "total": len(articles),
        "completed": completed,
        "pending": pending,
        "failed": failed,
        "completion_rate": f"{(completed / len(articles) * 100):.1f}%" if articles else "0%",
        "tracks": track_stats
    }

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def print_summary():
    manifest = load_or_init_manifest()
    summary = manifest["summary"]

    print("\n" + "=" * 76)
    print("🎨 JOY OF CARE - VISUAL ARTISTS PRODUCTION DASHBOARD")
    print("=" * 76)
    print(f"Total Articles: {summary['total']} | Completed: {summary['completed']} | Pending: {summary['pending']} | Progress: {summary['completion_rate']}")
    print("-" * 76)

    for t_id, stats in summary["tracks"].items():
        bar_len = 25
        pct = (stats["completed"] / stats["total"]) if stats["total"] > 0 else 0
        filled = int(round(pct * bar_len))
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\n📌 {stats['name']}")
        print(f"   Progress: [{bar}] {stats['completed']}/{stats['total']} ({pct*100:.1f}%)")
        print(f"   Status  : Pending: {stats['pending']} | Completed: {stats['completed']} | Failed: {stats['failed']}")

    print("\n" + "=" * 76)

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

def ingest_image(source_path, slug):
    if not os.path.exists(source_path):
        print(f"Error: Source image {source_path} does not exist.")
        return False

    manifest = load_or_init_manifest()
    if slug not in manifest["articles"]:
        print(f"Warning: Slug '{slug}' not found in prompts manifest, registering anyway.")

    try:
        im = Image.open(source_path)
        # Convert RGBA to RGB if needed
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")

        # Save WebP
        webp_out = IMAGES_DIR / f"{slug}.webp"
        im.save(webp_out, "WEBP", quality=88, method=6)

        # Save JPEG
        jpg_out = IMAGES_DIR / f"{slug}.jpg"
        im.save(jpg_out, "JPEG", quality=90, optimize=True)

        # Update manifest
        if slug in manifest["articles"]:
            manifest["articles"][slug]["status"] = "completed"
            manifest["articles"][slug]["featuredImage"] = f"/assets/images/articles/{slug}.webp"
            manifest["articles"][slug]["has_photo_webp"] = True
            manifest["articles"][slug]["has_photo_jpg"] = True
            manifest["articles"][slug]["completed_at"] = datetime.utcnow().isoformat()
            save_manifest(manifest)

        # Update MDX
        update_single_article_mdx(slug, f"/assets/images/articles/{slug}.webp")
        print(f"✓ Ingested {slug}: WebP ({webp_out.stat().st_size} B), JPG ({jpg_out.stat().st_size} B)")
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
        if entry.get("status") == "completed" and entry.get("has_photo_webp"):
            image_url = f"/assets/images/articles/{slug}.webp"
            if update_single_article_mdx(slug, image_url):
                synced += 1
    print(f"✓ Synced {synced} MDX articles to use photojournalism WebP images.")

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
        # Check if base matches any slug or ends with slug
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
    parser.add_argument("--ingest", help="Ingest a generated image path")
    parser.add_argument("--slug", help="Article slug for the ingested image")
    parser.add_argument("--batch-ingest", help="Batch ingest images from directory")
    parser.add_argument("--sync-mdx", action="store_true", help="Sync completed images to MDX articles")

    args = parser.parse_args()

    if args.export_tracks:
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
