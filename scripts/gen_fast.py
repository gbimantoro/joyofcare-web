#!/usr/bin/env python3
"""Fast asset generator — reuses one browser instance."""
import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS = Path("/home/gobeam/Projects/joyofcare-web/assets/blog")
THUMB = ASSETS / "thumbnails"
INFO = ASSETS / "infographics"
ARTDIR = Path("/home/gobeam/Projects/joyofcare-web/src/content/articles")

CATS = {
    "perawatan-lansia": {"label":"Perawatan Lansia","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',"color":"#4CAF50","desc":"Panduan perawatan kesehatan lansia di rumah"},
    "fisioterapi-rumah": {"label":"Fisioterapi Rumah","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2196F3" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 17.5 3 6V3h3l11.5 11.5"/><path d="m13 19 6-6"/><path d="m16 16 4 4"/><path d="m19 21 2-2"/></svg>',"color":"#2196F3","desc":"Fisioterapi profesional di rumah Anda"},
    "panggil-dokter": {"label":"Panggil Dokter","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',"color":"#E91E63","desc":"Dokter profesional datang ke rumah Anda"},
    "parkinson": {"label":"Parkinson","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#9C27B0" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',"color":"#9C27B0","desc":"Perawatan dan terapi pasien Parkinson"},
    "studi-luar-negeri": {"label":"Studi Luar Negeri","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF9800" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg>',"color":"#FF9800","desc":"Persyaratan kesehatan untuk studi luar negeri"},
    "osteoporosis": {"label":"Osteoporosis","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#795548" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>',"color":"#795548","desc":"Pencegahan dan perawatan osteoporosis"},
    "antar-jemput-rs": {"label":"Antar Jemput RS","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#F44336" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',"color":"#F44336","desc":"Layanan transportasi medis antar jemput"},
    "vaksinasi-rumah": {"label":"Vaksinasi Rumah","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00BCD4" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m18 2 4 4-4 4"/><path d="M14 6H6a4 4 0 0 0-4 4v8"/><path d="M22 14v8M2 14v8"/><path d="M10 2v20"/></svg>',"color":"#00BCD4","desc":"Vaksinasi praktis di rumah Anda"},
    "infus-vitamin": {"label":"Infus Vitamin","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF5722" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v20M2 10h20"/><circle cx="12" cy="12" r="10"/></svg>',"color":"#FF5722","desc":"Layanan infus dan suntik vitamin di rumah"},
    "perawat-homecare": {"label":"Perawat Homecare","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#607D8B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',"color":"#607D8B","desc":"Perawat profesional untuk perawatan di rumah"},
    "kesehatan-umum": {"label":"Kesehatan Umum","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#E91E63" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',"color":"#E91E63","desc":"Tips dan panduan kesehatan umum"},
    "home-lab": {"label":"Home Lab","svg":'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#3F51B5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M12 3v7"/><path d="M5 21h14"/><path d="M7 21l2-9h6l2 9"/></svg>',"color":"#3F51B5","desc":"Cek laboratorium di rumah Anda"},
}

def get_articles():
    cats = {}
    for f in os.listdir(ARTDIR):
        if f.endswith('.mdx'):
            content = (ARTDIR / f).read_text()
            cat = title = None
            for line in content.split('\n'):
                if line.startswith('category:'): cat = line.split(':',1)[1].strip()
                elif line.startswith('title:'): title = line.split(':',1)[1].strip()
                if cat and title: break
            if cat: cats.setdefault(cat, []).append({'slug': f[:-4], 'title': title or f})
    return cats

def thumb_html(d, count):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap");
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:450px;font-family:Inter,sans-serif;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.frame{{width:798px;height:448px;border-radius:20px;position:relative;overflow:hidden;border:2px solid #f0f0f0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:48px;background:linear-gradient(180deg,#fff 0%,{d["color"]}08 100%)}}
.bar{{position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,{d["color"]},{d["color"]}88)}}
.ico{{width:96px;height:96px;border-radius:24px;display:flex;align-items:center;justify-content:center;margin-bottom:24px;background:{d["color"]}10;border:2px solid {d["color"]}25}}
.name{{font-size:30px;font-weight:800;color:#1a1a2e;letter-spacing:-.02em;margin-bottom:6px}}
.sub{{font-size:15px;color:#777;text-align:center;margin-bottom:28px}}
.metrics{{display:flex;gap:48px;align-items:center}}
.m{{text-align:center}}
.mv{{font-size:28px;font-weight:800;color:{d["color"]}}}
.ml{{font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:.1em;margin-top:2px}}
.sep{{width:1px;height:36px;background:#e5e5e5}}
.foot{{position:absolute;bottom:18px;left:0;right:0;text-align:center;font-size:11px;color:#ccc;font-weight:600;letter-spacing:.12em;text-transform:uppercase}}
</style></head><body><div class="frame">
<div class="bar"></div>
<div class="ico">{d["svg"]}</div>
<div class="name">{d["label"]}</div>
<div class="sub">{d["desc"]}</div>
<div class="metrics">
<div class="m"><div class="mv">{count}</div><div class="ml">Artikel</div></div>
<div class="sep"></div>
<div class="m"><div class="mv">7 Hari</div><div class="ml">Per Minggu</div></div>
</div>
<div class="foot">Joy of Care</div>
</div></body></html>'''

def info_html(art, cd):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap");
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:1000px;font-family:Inter,sans-serif;background:#fafbfc;display:flex;flex-direction:column;overflow:hidden}}
.hdr{{background:linear-gradient(135deg,{cd["color"]},{cd["color"]}cc);padding:44px 40px 36px;color:#fff}}
.hdr .tag{{display:inline-block;background:rgba(255,255,255,.18);padding:5px 14px;border-radius:100px;font-size:12px;font-weight:600;margin-bottom:14px;border:1px solid rgba(255,255,255,.25)}}
.hdr h1{{font-size:26px;font-weight:800;line-height:1.3;margin-bottom:8px;letter-spacing:-.02em}}
.hdr p{{font-size:13px;opacity:.85}}
.wrap{{flex:1;padding:28px 32px;display:flex;flex-direction:column;gap:16px}}
.sec{{background:#fff;border-radius:16px;padding:22px 26px;box-shadow:0 2px 16px rgba(0,0,0,.04);border:1px solid #eee}}
.sec h3{{font-size:15px;font-weight:700;color:#1a1a2e;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.sec h3 .dot{{width:8px;height:8px;border-radius:50%;background:{cd["color"]};display:inline-block}}
.sec ul{{list-style:none}}
.sec li{{font-size:13px;color:#555;padding:8px 0;border-bottom:1px solid #f5f5f5;display:flex;align-items:flex-start;gap:10px}}
.sec li:last-child{{border:none}}
.sec li .num{{width:22px;height:22px;border-radius:50%;background:{cd["color"]}15;color:{cd["color"]};font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}}
.cta{{background:linear-gradient(135deg,#FC9000,#E58200);border-radius:16px;padding:26px;text-align:center;color:#fff}}
.cta h3{{font-size:17px;font-weight:700;margin-bottom:6px}}
.cta p{{font-size:13px;opacity:.9;margin-bottom:14px}}
.cta-btn{{display:inline-block;background:#fff;color:#FC9000;padding:11px 28px;border-radius:100px;font-weight:700;font-size:14px}}
.ftr{{background:#1a1a2e;padding:14px 32px;display:flex;justify-content:space-between;color:#fff;font-size:12px}}
.ftr b{{font-weight:700}} .ftr span{{opacity:.6}}
</style></head><body>
<div class="hdr">
<div class="tag">{cd["label"]}</div>
<h1>{art["title"]}</h1>
<p>Joy of Care — Layanan Kesehatan Profesional di Rumah</p>
</div>
<div class="wrap">
<div class="sec"><h3><span class="dot"></span>Informasi Penting</h3><ul>
<li><span class="num">1</span>Layanan profesional langsung ke rumah Anda</li>
<li><span class="num">2</span>Tenaga medis berlisensi dan berpengalaman</li>
<li><span class="num">3</span>Harga transparan sudah termasuk biaya transport</li>
</ul></div>
<div class="sec"><h3><span class="dot"></span>Keunggulan Joy of Care</h3><ul>
<li><span class="num">1</span>Konsultasi gratis via WhatsApp 08811-118-911</li>
<li><span class="num">2</span>Respon cepat dalam 1-2 jam</li>
<li><span class="num">3</span>Area layanan: Jakarta, Tangerang, Depok, Bogor</li>
</ul></div>
<div class="cta"><h3>Hubungi Sekarang</h3><p>Chat WhatsApp untuk konsultasi gratis dengan tim medis kami</p><div class="cta-btn">08811-118-911</div></div>
</div>
<div class="ftr"><b>Joy of Care</b><span>new.joyof.care</span></div>
</body></html>'''

def main():
    arts = get_articles()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width':800,'height':1000})
        
        print("[1/2] Thumbnails...")
        for slug, d in CATS.items():
            count = len(arts.get(slug, []))
            html = thumb_html(d, count)
            out = THUMB / f"{slug}.png"
            if out.exists(): print(f"  SKIP {slug} (exists)"); continue
            page.set_viewport_size({'width':800,'height':450})
            page.set_content(html)
            page.wait_for_timeout(800)
            page.screenshot(path=str(out))
            print(f"  OK {slug}.png")
        
        print("[2/2] Infographics...")
        n = 0
        for slug, articles in arts.items():
            cd = CATS.get(slug, {"label":slug,"svg":"","color":"#666","desc":""})
            for i, art in enumerate(articles):
                if i % 3 != 0: continue
                fn = art['slug'][:60] + '.png'
                out = INFO / fn
                if out.exists(): continue
                html = info_html(art, cd)
                page.set_viewport_size({'width':800,'height':1000})
                page.set_content(html)
                page.wait_for_timeout(800)
                page.screenshot(path=str(out))
                n += 1
                print(f"  OK {fn[:50]}...")
        
        browser.close()
    print(f"\nDone! {n} new infographics + thumbnails generated")

if __name__ == "__main__":
    main()
