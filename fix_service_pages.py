#!/usr/bin/env python3
"""Fix service pages: replace nav, fix WA links, ensure SEO schema."""
import re, sys, os

BASE = "/home/gobeam/Projects/joyofcare-web/pages"

# Standard modern nav (single Layanan link)
NAV = '''  <nav class="nav" role="navigation" aria-label="Navigasi utama">
    <div class="nav-inner">
      <a href="/" class="nav-logo" aria-label="Joy of Care - Beranda">
        <img src="/images/joc_long.png" alt="Joy of Care" width="160" height="40">
      </a>
      <div class="nav-links">
        <a href="/">Beranda</a>
        <a href="/layanan-lengkap">Layanan</a>
        <a href="/blog/">Artikel</a>
        <a href="/#faq">FAQ</a>
        <a href="https://wa.me/628811118911?text=Hi,%20saya%20tahu%20dari%20web.%20Mau%20tanya%20layanan%20Joy%20of%20Care" class="nav-cta">Chat WhatsApp</a>
      </div>
      <button class="nav-mobile" aria-label="Buka menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    </div>
  </nav>'''

def fix_nav(html):
    # Replace whole nav element (first <nav ...> ... </nav>)
    return re.sub(r'<nav[^>]*>.*?</nav>', NAV, html, count=1, flags=re.DOTALL)

def fix_links(html):
    # api.whatsapp.com/send/?phone=628811118911 -> wa.me
    html = html.replace(
        'https://api.whatsapp.com/send/?phone=628811118911',
        'https://wa.me/628811118911'
    )
    return html

def strip_prices(html):
    # Remove price tables
    html = re.sub(r'<table[^>]*class="price-table".*?</table>', '', html, flags=re.DOTALL)
    # Remove Rp amounts
    html = re.sub(r'(Mulai\s*)?Rp\s*[\d.,]+', '', html)
    # Remove price footnotes
    html = re.sub(r'<p class="text-muted"[^>]*>\*?[Hh]arga[^<]*</p>', '', html)
    # Replace 'Harga all-in'/'harga all-in' text
    html = html.replace('Harga all-in termasuk transport', 'sudah termasuk transport')
    html = html.replace('Harga all-in, sudah termasuk transportasi', 'sudah termasuk transportasi')
    html = re.sub(r'[Hh]arga all-in[^.<]*', 'harga kompetitif', html)
    return html

def fix_cta(html):
    # Ensure footer date text removed
    html = html.replace('Terakhir diperbarui: 5 September 2026', '')
    html = re.sub(r'<p class="text-muted">\s*</p>', '', html)
    return html

def add_homepage_stat(filepath):
    pass

for fname in ["layanan-fisioterapi-ke-rumah.html", "homelab.html",
              "layanan-perawat-di-rumah.html", "infus-suntik-vitamin-di-rumah.html"]:
    path = os.path.join(BASE, fname)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    html = fix_nav(html)
    html = fix_links(html)
    html = strip_prices(html)
    html = fix_cta(html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed: {fname} ({html.count('wa.me')} wa.me links, nav replaced={NAV.splitlines()[0] in html})")
