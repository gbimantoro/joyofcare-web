#!/usr/bin/env python3
"""
Joy of Care Sitemap & RSS Generator
Scans blog articles and categories to produce valid sitemap XML and RSS feeds.
"""

import os
import json
from datetime import datetime
from xml.sax.saxutils import escape

BASE_URL = "https://www.joyofcare.net"
PAGES_DIR = "/home/gobeam/Projects/joyofcare-web/pages"
BLOG_DIR = os.path.join(PAGES_DIR, "blog")
INDEX_JSON = os.path.join(BLOG_DIR, "index.json")
OUTPUT_SITEMAP_ARTICLES = os.path.join(PAGES_DIR, "sitemap-articles.xml")
OUTPUT_RSS = os.path.join(BLOG_DIR, "feed.xml")

CATEGORY_MAP = {
    "healthy-aging-3": ("healthy-aging", "Lansia Sehat & Geriatri"),
    "healthy-aging": ("healthy-aging", "Lansia Sehat & Geriatri"),
    "pengalaman-1": ("pengalaman", "Pengalaman Pasien"),
    "pengalaman": ("pengalaman", "Pengalaman Pasien"),
    "studi-luar-negeri-4": ("studi-luar-negeri", "Studi di Luar Negeri"),
    "studi-luar-negeri": ("studi-luar-negeri", "Studi di Luar Negeri"),
    "vaksinasi-di-rumah-2": ("vaksinasi", "Vaksinasi di Rumah"),
    "vaksinasi": ("vaksinasi", "Vaksinasi di Rumah")
}

def generate_sitemap(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        '',
        '  <!-- Blog Hub & Category Listing Pages -->',
        '  <url>',
        f'    <loc>{BASE_URL}/blog/</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.85</priority>',
        '  </url>'
    ]
    
    unique_cats = set()
    for art in articles:
        cat_key = art.get("category", "healthy-aging")
        cat_slug, _ = CATEGORY_MAP.get(cat_key, (cat_key, cat_key))
        unique_cats.add(cat_slug)
        
    for cat in sorted(unique_cats):
        lines.extend([
            '  <url>',
            f'    <loc>{BASE_URL}/blog/{cat}/</loc>',
            f'    <lastmod>{today}</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.80</priority>',
            '  </url>'
        ])
        
    lines.append('\n  <!-- Blog Articles -->')
    for art in articles:
        cat_key = art.get("category", "healthy-aging")
        cat_slug, _ = CATEGORY_MAP.get(cat_key, (cat_key, cat_key))
        slug = art.get("slug", "")
        url = f"{BASE_URL}/blog/{cat_slug}/{slug}"
        
        # Determine priority based on length/pillar status
        wc = art.get("word_count", 600)
        priority = "0.8" if wc > 1000 else "0.7"
        
        lines.extend([
            '  <url>',
            f'    <loc>{escape(url)}</loc>',
            f'    <lastmod>{today}</lastmod>',
            '    <changefreq>monthly</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>'
        ])
        
    lines.append('</urlset>\n')
    return '\n'.join(lines)

def generate_rss(articles):
    now_rfc822 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")
    
    items_xml = []
    for art in articles[:20]: # Latest 20 articles in RSS feed
        title = escape(art.get("title", "Artikel Joy of Care"))
        cat_key = art.get("category", "healthy-aging")
        cat_slug, cat_name = CATEGORY_MAP.get(cat_key, (cat_key, "Kesehatan"))
        slug = art.get("slug", "")
        url = f"{BASE_URL}/blog/{cat_slug}/{slug}"
        desc = escape(f"Panduan kesehatan dan tips perawatan terpercaya dari Joy of Care: {title}")
        
        items_xml.append(f"""    <item>
      <title>{title}</title>
      <link>{escape(url)}</link>
      <guid isPermaLink="true">{escape(url)}</guid>
      <description>{desc}</description>
      <category>{escape(cat_name)}</category>
      <dc:creator>Tim Medis Joy of Care</dc:creator>
      <pubDate>{now_rfc822}</pubDate>
    </item>""")
        
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Joy of Care — Blog Kesehatan &amp; Homecare Lansia</title>
    <link>{BASE_URL}/blog/</link>
    <description>Edukasi kesehatan keluarga, fisioterapi, geriatri lansia sehat, dan homecare profesional Jabodetabek.</description>
    <language>id-ID</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{BASE_URL}/blog/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    return rss_content

def main():
    if not os.path.exists(INDEX_JSON):
        print(f"Error: index.json not found at {INDEX_JSON}")
        return
        
    with open(INDEX_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)
        
    print(f"Loaded {len(articles)} articles from {INDEX_JSON}")
    
    # 1. Generate Sitemap XML
    sitemap_xml = generate_sitemap(articles)
    with open(OUTPUT_SITEMAP_ARTICLES, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"Generated sitemap at: {OUTPUT_SITEMAP_ARTICLES}")
    
    # 2. Generate RSS Feed XML
    rss_xml = generate_rss(articles)
    with open(OUTPUT_RSS, "w", encoding="utf-8") as f:
        f.write(rss_xml)
    print(f"Generated RSS feed at: {OUTPUT_RSS}")

if __name__ == "__main__":
    main()
