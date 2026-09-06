#!/usr/bin/env python3
"""
Bulk update script for Joy of Care articles:
1. Fix internal links (old paths -> new Astro routes)
2. Randomize dates between Aug 1 - Sep 5, 2026
3. Add featuredImage from thumbnails folder
4. Add infographics from infographics folder
"""

import os
import re
import random
from datetime import datetime, timedelta
from pathlib import Path
import yaml

ARTICLES_DIR = Path("/home/gobeam/Projects/joyofcare-web/src/content/articles")
DIST_THUMBNAILS = Path("/home/gobeam/Projects/joyofcare-web/dist/assets/thumbnails")
DIST_BLOG = Path("/home/gobeam/Projects/joyofcare-web/dist/assets/blog")
DIST_INFOGRAPHICS = Path("/home/gobeam/Projects/joyofcare-web/dist/assets/infographics")

# Mapping of old internal links to new Astro routes
LINK_MAPPING = {
    "/layanan/infus-vitamin-di-rumah": "/infus-suntik-vitamin-di-rumah",
    "/layanan/panggil-dokter": "/panggil-dokter-ke-rumah",
    "/layanan/perawat-homecare": "/layanan-perawat-di-rumah",
    "/layanan/cek-lab-di-rumah": "/homelab",
    "/layanan/fisioterapi": "/layanan-fisioterapi-ke-rumah",
    "/layanan/akupuntur": "/layanan-akupuntur-di-rumah",
    "/layanan/antar-jemput": "/transcare-antar-jemput-ke-rs-jakarta-tangerang",
    "/layanan-kami": "/layanan-lengkap",
    "/artikel": "/blog/",
    "/walk-in-promo": "/layanan-lengkap",  # fallback
}

# Category to thumbnail mapping (using dist/assets/blog SVGs)
CATEGORY_THUMBNAILS = {
    "perawatan-lansia": "perawatan-lansia.svg",
    "fisioterapi-rumah": "fisioterapi-rumah.svg",
    "panggil-dokter": "panggil-dokter.svg",
    "parkinson": "parkinson.svg",
    "studi-luar-negeri": "studi-luar-negeri.svg",
    "osteoporosis": "osteoporosis.svg",
    "antar-jemput-rs": "antar-jemput-rs.svg",
    "vaksinasi-rumah": "vaksinasi-rumah.svg",
    "infus-vitamin": "infus-vitamin.svg",
    "perawat-homecare": "perawat-homecare.svg",
    "kesehatan-umum": "kesehatan-umum.svg",
    "home-lab": "home-lab.svg",
}

# Category to article thumbnail (hero image) mapping
CATEGORY_ARTICLE_IMAGES = {
    "perawatan-lansia": "perawatan-lansia-v1-hero.svg",
    "fisioterapi-rumah": "fisioterapi-rumah-v1-hero.svg",
    "panggil-dokter": "panggil-dokter-v1-hero.svg",
    "parkinson": "parkinson-v1-hero.svg",
    "studi-luar-negeri": "studi-luar-negeri-v1-hero.svg",
    "osteoporosis": "osteoporosis-v1-hero.svg",
    "antar-jemput-rs": "antar-jemput-rs-v1-hero.svg",
    "vaksinasi-rumah": "vaksinasi-rumah-v1-hero.svg",
    "infus-vitamin": "infus-vitamin-v1-hero.svg",
    "perawat-homecare": "perawat-homecare-v1-hero.svg",
    "kesehatan-umum": "kesehatan-umum-v1-hero.svg",
    "home-lab": "home-lab-v1-hero.svg",
}

# Date range: Aug 1 - Sep 5, 2026
START_DATE = datetime(2026, 8, 1)
END_DATE = datetime(2026, 9, 5)

def get_random_date():
    """Get a random date between START_DATE and END_DATE"""
    delta = END_DATE - START_DATE
    random_days = random.randint(0, delta.days)
    return START_DATE + timedelta(days=random_days)

def fix_internal_links(content):
    """Replace old internal links with new Astro routes"""
    # Fix internalLinks array in frontmatter
    for old, new in LINK_MAPPING.items():
        content = content.replace(f'"{old}"', f'"{new}"')
        content = content.replace(f"'{old}'", f"'{new}'")
    
    # Fix markdown links in content body: ](old_path) -> ](new_path)
    for old, new in LINK_MAPPING.items():
        # Match markdown links: [text](old_path)
        pattern = rf'\]\(({re.escape(old)})\)'
        content = re.sub(pattern, f']({new})', content)
        
        # Match malformed links: text](old_path) -> text](new_path)
        # This handles cases like "Layanan Terapi Infus Vitamin di Rumah Joy of Care](/infus-suntik-vitamin-di-rumah)"
        pattern_malformed = rf'(?<!\])\)({re.escape(old)})\)'
        content = re.sub(pattern_malformed, f')({new})', content)
    
    return content

def update_frontmatter_field(content, field_name, new_value):
    """Update a specific frontmatter field"""
    pattern = rf'^(\s*{field_name}:\s*).*$'
    replacement = rf'\1{new_value}'
    return re.sub(pattern, replacement, content, flags=re.MULTILINE)

def add_frontmatter_field(content, field_name, new_value, after_field=None):
    """Add a new frontmatter field if it doesn't exist"""
    # Check if field already exists
    if re.search(rf'^\s*{field_name}:', content, re.MULTILINE):
        return content
    
    if after_field and re.search(rf'^\s*{after_field}:', content, re.MULTILINE):
        # Insert after the specified field
        pattern = rf'^(?P<indent>\s*{after_field}:.*$)(?P<nl>\n)'
        replacement = rf'\g<indent>\g<nl>{field_name}: {new_value}\g<nl>'
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Insert after title if no after_field specified or not found
    pattern = rf'^(?P<indent>\s*title:.*$)(?P<nl>\n)'
    replacement = rf'\g<indent>\g<nl>{field_name}: {new_value}\g<nl>'
    return re.sub(pattern, replacement, content, flags=re.MULTILINE)

def parse_frontmatter(content):
    """Parse frontmatter from MDX content"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        try:
            return yaml.safe_load(fm_text), match.end()
        except:
            return {}, 0
    return {}, 0

def get_slug_from_filename(filename):
    """Extract slug from filename"""
    return filename.replace('.mdx', '')

def find_infographic(slug):
    """Find infographic for an article slug"""
    # Look for exact match first
    for ext in ['-infografis.svg', '.svg']:
        infographic_name = f"{slug}{ext}"
        if (DIST_INFOGRAPHICS / infographic_name).exists():
            return infographic_name
    return None

def process_article(filepath):
    """Process a single article file"""
    content = filepath.read_text(encoding='utf-8')
    original_content = content
    
    # Parse frontmatter
    frontmatter, fm_end = parse_frontmatter(content)
    if not frontmatter:
        return False, "No frontmatter found"
    
    category = frontmatter.get('category', '')
    slug = frontmatter.get('slug', get_slug_from_filename(filepath.name))
    
    # 1. Fix internal links
    content = fix_internal_links(content)
    
    # 2. Randomize date
    random_date = get_random_date()
    date_str = random_date.strftime('%Y-%m-%d')
    content = update_frontmatter_field(content, 'date', f"'{date_str}'")
    
    # 3. Add featuredImage if not present
    if 'featuredImage' not in frontmatter or not frontmatter['featuredImage']:
        article_image = CATEGORY_ARTICLE_IMAGES.get(category)
        if article_image:
            content = add_frontmatter_field(content, 'featuredImage', f'"/assets/thumbnails/{article_image}"', after_field='slug')
    
    # 4. Add infographic if found
    infographic = find_infographic(slug)
    if infographic:
        # Check if infographic field exists
        if 'infographic' not in frontmatter:
            content = add_frontmatter_field(content, 'infographic', f'"/assets/infographics/{infographic}"', after_field='featuredImage')
    
    # Only write if changed
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        return True, f"Updated: date={date_str}, featuredImage={category}, infographic={infographic}"
    
    return False, "No changes needed"

def main():
    print(f"Processing articles in {ARTICLES_DIR}")
    articles = list(ARTICLES_DIR.glob("*.mdx"))
    print(f"Found {len(articles)} articles")
    
    updated = 0
    errors = 0
    
    for article_path in articles:
        try:
            changed, msg = process_article(article_path)
            if changed:
                updated += 1
                print(f"  ✓ {article_path.name}: {msg}")
            else:
                print(f"  - {article_path.name}: {msg}")
        except Exception as e:
            errors += 1
            print(f"  ✗ {article_path.name}: ERROR - {e}")
    
    print(f"\nSummary: {updated} updated, {errors} errors, {len(articles)} total")

if __name__ == "__main__":
    # Set seed for reproducibility
    random.seed(42)
    main()