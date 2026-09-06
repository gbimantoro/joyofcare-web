#!/usr/bin/env python3
"""Generate category thumbnails and article infographics for Joy of Care blog."""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# Paths
ASSETS_DIR = Path("/home/gobeam/Projects/joyofcare-web/assets/blog")
THUMBNAILS_DIR = ASSETS_DIR / "thumbnails"
INFOGRAPHICS_DIR = ASSETS_DIR / "infographics"
ARTICLES_DIR = Path("/home/gobeam/Projects/joyofcare-web/src/content/articles")

# Category data
CATEGORIES = {
    "perawatan-lansia": {"label": "Perawatan Lansia", "icon": "👴", "color": "#4CAF50", "desc": "Panduan perawatan kesehatan lansia"},
    "fisioterapi-rumah": {"label": "Fisioterapi Rumah", "icon": "🦴", "color": "#2196F3", "desc": "Fisioterapi profesional di rumah"},
    "panggil-dokter": {"label": "Panggil Dokter", "icon": "🩺", "color": "#E91E63", "desc": "Dokter datang ke rumah Anda"},
    "parkinson": {"label": "Parkinson", "icon": "🧠", "color": "#9C27B0", "desc": "Perawatan pasien Parkinson"},
    "studi-luar-negeri": {"label": "Studi Luar Negeri", "icon": "✈️", "color": "#FF9800", "desc": "Persyaratan kesehatan studi"},
    "osteoporosis": {"label": "Osteoporosis", "icon": "🦴", "color": "#795548", "desc": "Pencegahan osteoporosis"},
    "antar-jemput-rs": {"label": "Antar Jemput RS", "icon": "🚑", "color": "#F44336", "desc": "Transportasi medis"},
    "vaksinasi-rumah": {"label": "Vaksinasi Rumah", "icon": "💉", "color": "#00BCD4", "desc": "Vaksinasi di rumah"},
    "infus-vitamin": {"label": "Infus Vitamin", "icon": "💊", "color": "#FF5722", "desc": "Infus vitamin di rumah"},
    "perawat-homecare": {"label": "Perawat Homecare", "icon": "🏥", "color": "#607D8B", "desc": "Perawat profesional homecare"},
    "kesehatan-umum": {"label": "Kesehatan Umum", "icon": "❤️", "color": "#E91E63", "desc": "Tips kesehatan umum"},
    "home-lab": {"label": "Home Lab", "icon": "🧪", "color": "#3F51B5", "desc": "Cek lab di rumah"},
}


def get_articles_by_category():
    categories = {}
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith('.mdx'):
            with open(ARTICLES_DIR / f, 'r') as file:
                content = file.read()
                cat = title = None
                for line in content.split('\n'):
                    if line.startswith('category:'):
                        cat = line.split(':', 1)[1].strip()
                    elif line.startswith('title:'):
                        title = line.split(':', 1)[1].strip()
                    if cat and title:
                        break
                if cat:
                    categories.setdefault(cat, []).append({'slug': f.replace('.mdx', ''), 'title': title or f})
    return categories


def render_html(html, output, w, h):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.set_content(html)
        page.wait_for_load_state('networkidle')
        page.screenshot(path=str(output))
        browser.close()


def thumb_html(cat, data, count):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:450px;font-family:Inter,sans-serif;background:linear-gradient(135deg,{data["color"]}15,{data["color"]}05);display:flex;align-items:center;justify-content:center}}
.card{{width:760px;height:410px;background:#fff;border-radius:24px;box-shadow:0 20px 60px rgba(0,0,0,.08);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:40px;position:relative;overflow:hidden}}
.card::before{{content:"";position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,{data["color"]},{data["color"]}CC)}}
.icon{{font-size:72px;margin-bottom:20px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.1))}}
.label{{font-size:32px;font-weight:800;color:#1A1A2E;margin-bottom:12px;text-align:center;letter-spacing:-.02em}}
.desc{{font-size:16px;color:#555770;text-align:center;max-width:500px;line-height:1.5;margin-bottom:20px}}
.stats{{display:flex;gap:32px;margin-top:8px}}
.stat{{text-align:center}}
.stat-n{{font-size:28px;font-weight:800;color:{data["color"]}}}
.stat-l{{font-size:12px;color:#8B8DA3;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}}
.brand{{position:absolute;bottom:20px;right:24px;font-size:12px;color:#8B8DA3;font-weight:500}}
</style></head><body><div class="card">
<div class="icon">{data["icon"]}</div>
<div class="label">{data["label"]}</div>
<div class="desc">{data["desc"]}</div>
<div class="stats"><div class="stat"><div class="stat-n">{count}</div><div class="stat-l">Artikel</div></div>
<div class="stat"><div class="stat-n">24/7</div><div class="stat-l">Tersedia</div></div></div>
<div class="brand">Joy of Care</div>
</div></body></html>'''


def info_html(article, cat_data):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:1000px;font-family:Inter,sans-serif;background:linear-gradient(180deg,{cat_data["color"]}08,#fff);display:flex;flex-direction:column;overflow:hidden}}
.hdr{{background:linear-gradient(135deg,{cat_data["color"]},{cat_data["color"]}DD);padding:40px;color:#fff;text-align:center}}
.hdr-icon{{font-size:48px;margin-bottom:16px}}
.hdr h1{{font-size:28px;font-weight:800;line-height:1.3;margin-bottom:12px;letter-spacing:-.02em}}
.hdr p{{font-size:14px;opacity:.9}}
.content{{flex:1;padding:32px 40px;display:flex;flex-direction:column;gap:20px}}
.box{{background:#fff;border-radius:16px;padding:24px;box-shadow:0 4px 20px rgba(0,0,0,.05);border-left:4px solid {cat_data["color"]}}}
.box h3{{font-size:16px;font-weight:700;color:#1A1A2E;margin-bottom:12px}}
.box ul{{list-style:none;padding:0}}
.box li{{font-size:14px;color:#555770;padding:8px 0;border-bottom:1px solid #F0F0F5}}
.box li:last-child{{border-bottom:none}}
.cta{{background:linear-gradient(135deg,#FC9000,#E58200);border-radius:16px;padding:24px;text-align:center;color:#fff;margin-top:auto}}
.cta h3{{font-size:18px;font-weight:700;margin-bottom:8px}}
.cta p{{font-size:14px;opacity:.9;margin-bottom:16px}}
.cta-btn{{display:inline-block;background:#fff;color:#FC9000;padding:12px 24px;border-radius:100px;font-weight:700;font-size:14px}}
.ftr{{background:#1A1A2E;padding:16px 40px;display:flex;justify-content:space-between;color:#fff}}
.ftr-brand{{font-size:14px;font-weight:700}}
.ftr-info{{font-size:12px;opacity:.8}}
</style></head><body>
<div class="hdr"><div class="hdr-icon">{cat_data["icon"]}</div><h1>{article["title"]}</h1><p>{cat_data["label"]} • Joy of Care</p></div>
<div class="content">
<div class="box"><h3>📋 Informasi Penting</h3><ul><li>Layanan profesional di rumah Anda</li><li>Tenaga medis berlisensi</li><li>Harga transparan termasuk transport</li></ul></div>
<div class="box"><h3>✅ Keunggulan</h3><ul><li>Konsultasi gratis via WhatsApp</li><li>Respon cepat 1-2 jam</li><li>Area: Jabodetabek</li></ul></div>
<div class="cta"><h3>Chat WhatsApp Sekarang</h3><p>Konsultasi gratis dengan tim medis</p><div class="cta-btn">08811-118-911</div></div>
</div>
<div class="ftr"><div class="ftr-brand">Joy of Care</div><div class="ftr-info">new.joyof.care</div></div>
</body></html>'''


def main():
    print("🎨 Generating Joy of Care blog assets...")
    arts = get_articles_by_category()
    
    print("\n📸 Category thumbnails...")
    for slug, data in CATEGORIES.items():
        count = len(arts.get(slug, []))
        html = thumb_html(slug, data, count)
        out = THUMBNAILS_DIR / f"{slug}.png"
        render_html(html, out, 800, 450)
        print(f"  ✓ {slug}.png ({count} articles)")
    
    print("\n📊 Infographics (1/3 of articles)...")
    n = 0
    for slug, articles in arts.items():
        cd = CATEGORIES.get(slug, {"label": slug, "icon": "📄", "color": "#666", "desc": ""})
        for i, art in enumerate(articles):
            if i % 3 == 0:
                html = info_html(art, cd)
                out = INFOGRAPHICS_DIR / f"{art['slug'][:60]}.png"
                render_html(html, out, 800, 1000)
                n += 1
                print(f"  ✓ {art['slug'][:50]}...")
    
    print(f"\n✅ Done! {len(CATEGORIES)} thumbnails + {n} infographics = {len(CATEGORIES)+n} assets")


if __name__ == "__main__":
    main()
