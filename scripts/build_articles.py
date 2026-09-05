#!/usr/bin/env python3
"""Convert JoyofCare article .txt (frontmatter + markdown) to full HTML pages."""
import os, re, glob, html as html_mod

CATEGORIES = {
    "perawatan-lansia": "Perawatan Lansia",
    "fisioterapi-rumah": "Fisioterapi Rumah",
    "panggil-dokter": "Panggil Dokter",
    "parkinson": "Parkinson",
    "studi-luar-negeri": "Studi Luar Negeri",
    "osteoporosis": "Osteoporosis",
    "antar-jemput-rs": "Antar Jemput RS",
    "perawat-homecare": "Perawat Homecare",
    "home-lab": "Home Lab",
    "vaksinasi-rumah": "Vaksinasi Rumah",
    "infus-vitamin": "Infus Vitamin",
    "kesehatan-umum": "Kesehatan Umum",
}

WA_LINK = "https://api.whatsapp.com/send/?phone=628811118911"
WA_CTA = (f'<div class="wa-cta"><p><strong>📲 <a href="{WA_LINK}?text=Hi,%20saya%20tahu%20dari%20web.%20Berapa%20biaya%20layanan%20Joy%20of%20Care?" '
          'class="wa-cta-link">Hubungi WhatsApp Resmi Joy of Care</a></strong></p></div>')

def parse_frontmatter(content):
    """Extract YAML frontmatter fields and body."""
    meta = {}
    body = content
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm = content[3:end].strip()
            body = content[end+3:].strip()
            # Simple YAML parse for our known fields
            lines = fm.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith('faq:') or line.startswith('secondary_keywords:') or line.startswith('internal_links:') or line.startswith('clinical_references:'):
                    i += 1
                    continue
                if ':' in line and not line.startswith('-'):
                    key, _, val = line.partition(':')
                    key = key.strip()
                    val = val.strip().strip('"\'')
                    meta[key] = val
                i += 1
    return meta, body

def md_to_html(text):
    """Convert markdown body to clean HTML with proper structure."""
    # Strip raw WhatsApp URL lines and double CTA wording from body first
    text = re.sub(r'Hubungi WhatsApp kami di https?://\S+ sekarang juga!?', '', text)
    text = re.sub(r'📲 \*\*Hubungi WhatsApp Resmi Joy of Care\*\*: <a href=[^>]+>[^<]+</a>', '', text)
    text = re.sub(r'^📲 Hubungi WhatsApp Resmi Joy of Care.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Hubungi WhatsApp JoC untuk informasi harga: https?://\S+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'https?://(api\.whatsapp\.com|wa\.me)/\S+', '', text)
    text = re.sub(r'\[Konsultasi Dokter Gratis via WhatsApp\]\(https?://[^)]+\)', '', text)
    text = re.sub(r'^Hubungi WhatsApp Resmi Joy of Care:.*$', '', text, flags=re.MULTILINE)
    # Remove orphaned markdown link brackets left by stripping (e.g. "[ sekarang juga!")
    text = re.sub(r'\[\s*sekarang juga!?\s*\](?:\(|\))??', '', text)
    text = re.sub(r'\[\s*\]|\[\s*', '', text)
    # Collapse blank runs introduced by stripping
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.split('\n')
    out = []
    i = 0

    # Block state
    stack = []  # track open block tags: 'ul', 'ol', 'quote', 'info'

    def close(level=1):
        for _ in range(level):
            if not stack:
                return
            tag = stack.pop()
            if tag == 'ul':
                out.append('</ul>')
            elif tag == 'ol':
                out.append('</ol>')
            elif tag == 'quote':
                out.append('</blockquote>')
            elif tag == 'info':
                out.append('</div>')

    def close_lists():
        while stack and stack[-1] in ('ul', 'ol'):
            tag = stack.pop()
            out.append('</ul>' if tag == 'ul' else '</ol>')

    # Table state
    in_table = False
    table_rows = []

    def close_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            out.append('<table>')
            for ridx, row in enumerate(table_rows):
                cells = [inline(c.strip()) for c in row.strip().strip('|').split('|')]
                tag = 'th' if ridx == 0 else 'td'
                out.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
            out.append('</table>')
        in_table = False
        table_rows = []

    for line in lines:
        s = line.strip()

        # Skip YAML frontmatter remnants
        if s == '---' or (s.startswith('---') and s.endswith('---')):
            close_table()
            close()
            continue

        # Empty line -> close lists and quotes (keep info-box open)
        if not s:
            close_lists()
            if stack and stack[-1] == 'quote':
                close()
            continue

        # Table detection
        if s.startswith('|') and '|' in s[1:]:
            if not in_table:
                close_lists()
                close()
                in_table = True
                table_rows = []
            if not re.match(r'^[\s|:-]+$', s):
                table_rows.append(s)
            continue
        elif in_table:
            close_table()

        # Headers
        h = re.match(r'^(#{1,4})\s+(.*)$', s)
        if h:
            close_table()
            close_lists()
            close()  # close quote/info before new block
            level = len(h.group(1))
            htext = inline(h.group(2))
            if 'Highlights' in htext:
                out.append(f'<div class="info-box"><h{level}>Highlights</h{level}>')
                stack.append('info')
            elif 'Penting dipahami' in htext:
                out.append(f'<div class="info-box"><h{level}>Penting dipahami</h{level}>')
                stack.append('info')
            else:
                out.append(f'<h{level}>{htext}</h{level}>')
            continue

        # HR
        if re.match(r'^-{3,}$', s) or re.match(r'^\*{3,}$', s):
            close_table()
            close()
            out.append('<hr>')
            continue

        # Blockquote (either quotes an info-box or normal quote)
        if s.startswith('>'):
            qtext = s.lstrip('> ').strip()
            hq = re.match(r'^(#{1,4})\s+(.*)$', qtext)
            if hq:
                htext = inline(hq.group(2))
                if 'Highlights' in htext or 'Penting dipahami' in htext:
                    close_table()
                    close_lists()
                    close()
                    out.append(f'<div class="info-box"><h{len(hq.group(1))}>{htext}</h{len(hq.group(1))}>')
                    stack.append('info')
                else:
                    if stack and stack[-1] in ('quote', 'info'):
                        # content inside an opened block; treat as plain heading
                        out.append(f'<h{len(hq.group(1))}>{htext}</h{len(hq.group(1))}>')
                    else:
                        out.append(f'<h{len(hq.group(1))}>{htext}</h{len(hq.group(1))}>')
                continue
            bq = re.match(r'^[-*]\s+(.*)$', qtext)
            if bq:
                # Bullet inside quote/info
                if not stack or stack[-1] not in ('quote', 'info', 'ul'):
                    out.append('<blockquote><ul>')
                    stack.append('quote')
                    stack.append('ul')
                elif stack[-1] == 'info':
                    out.append('<ul>')
                    stack.append('ul')
                out.append(f'<li>{inline(bq.group(1))}</li>')
                continue
            # Plain quoted text
            if not stack or stack[-1] not in ('quote', 'info'):
                out.append('<blockquote>')
                stack.append('quote')
            out.append(inline(qtext))
            continue

        # Bullet list
        bm = re.match(r'^[-*]\s+(.*)$', s)
        if bm:
            close_table()
            if stack and stack[-1] != 'ul':
                close()
            if not stack or stack[-1] != 'ul':
                out.append('<ul>')
                stack.append('ul')
            out.append(f'<li>{inline(bm.group(1))}</li>')
            continue

        # Numbered list
        nm = re.match(r'^(\d+)\.\s+(.*)$', s)
        if nm:
            close_table()
            if stack and stack[-1] != 'ol':
                close()
            if not stack or stack[-1] != 'ol':
                out.append('<ol>')
                stack.append('ol')
            out.append(f'<li>{inline(nm.group(2))}</li>')
            continue

        # Regular paragraph
        close_table()
        close_lists()
        if stack and stack[-1] == 'quote':
            close()
        out.append(f'<p>{inline(s)}</p>')

    close_table()
    close()
    return '\n'.join(out)

def inline(text):
    """Inline markdown conversions."""
    t = text
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    return t

def build_html(title, meta_desc, cat_dir, cat_name, slug, body):
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_mod.escape(title)} | Joy of Care</title>
  <meta name="description" content="{html_mod.escape(meta_desc)}">
  <link rel="canonical" href="https://new.joyof.care/blog/{cat_dir}/{slug}">
  <link rel="icon" href="/images/joc_icon.png" type="image/png">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../../css/blog.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":"{html_mod.escape(title)}","description":"{html_mod.escape(meta_desc)}","url":"https://new.joyof.care/blog/{cat_dir}/{slug}","publisher":{{"@type":"Organization","name":"Joy of Care","logo":"/images/joc_logo.png"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://new.joyof.care/blog/{cat_dir}/{slug}"}}}}
  </script>
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <a href="/" class="nav-logo"><img src="/images/joc_long.png" alt="Joy of Care" width="120" height="40"><span class="logo-text-mobile">Joy of Care</span></a>
    <div class="nav-links"><a href="/">Beranda</a><a href="/layanan-lengkap">Layanan</a><a href="/blog/">Artikel</a><a href="{WA_LINK}&text=Hi,%20saya%20tahu%20dari%20web.%20Mau%20tanya%20layanan%20Joy%20of%20Care" class="nav-cta">Chat WhatsApp</a></div>
    <button class="nav-mobile" aria-label="Buka menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div></nav>
  <article class="article-content" style="padding-top:calc(var(--nav-height)+40px);max-width:800px;margin:0 auto;">
    <nav class="breadcrumbs" style="margin-bottom:20px;font-size:0.9rem;color:var(--color-text-muted);"><a href="/" style="color:var(--color-primary);">Beranda</a> › <a href="/blog/" style="color:var(--color-primary);">Artikel</a> › <a href="/blog/{cat_dir}/" style="color:var(--color-primary);">{cat_name}</a> › {html_mod.escape(title)}</nav>
    <span class="category-badge" style="margin-bottom:16px;display:inline-block;">{cat_name}</span>
    <h1 style="font-size:2rem;margin-bottom:16px;line-height:1.3;">{html_mod.escape(title)}</h1>
    <p style="color:var(--color-text-muted);font-size:0.9rem;margin-bottom:32px;">Oleh Tim Joy of Care | Konsultasi Gratis via <a href="{WA_LINK}" style="color:var(--color-primary);">WhatsApp 08811-118-911</a></p>
    <div class="article-body">
{body}
{WA_CTA}
    </div>
    <div class="cta-box">
      <h3 style="color:white;margin-top:0;">Konsultasi Gratis dengan Dokter</h3>
      <p style="margin-bottom:16px;">Chat WhatsApp kami untuk konsultasi gratis tanpa komitmen.</p>
      <a href="{WA_LINK}&text=Hi,%20saya%20tahu%20dari%20web.%20Mau%20konsultasi%20gratis" class="cta-box-btn">Chat WhatsApp Sekarang</a>
    </div>
  </article>
  <script>var menuBtn=document.querySelector(".nav-mobile");var navLinks=document.querySelector(".nav-links");if(menuBtn&&navLinks){{menuBtn.addEventListener("click",function(e){{e.preventDefault();navLinks.classList.toggle("nav-open")}})}};</script>
</body></html>"""

def main():
    base = '/home/gobeam/Projects/joyofcare-web/pages/blog'
    src = '/home/gobeam/Projects/joyofcare-web/content-source/articles'
    total = 0
    for cat_dir, cat_name in CATEGORIES.items():
        cat_path = os.path.join(src, cat_dir)
        if not os.path.isdir(cat_path):
            continue
        for f in glob.glob(os.path.join(cat_path, '*.txt')):
            slug = os.path.splitext(os.path.basename(f))[0]
            with open(f) as fh:
                content = fh.read()
            meta, body_md = parse_frontmatter(content)
            title = meta.get('title', slug.replace('-', ' ').title())
            meta_desc = meta.get('meta_description', title)
            body_html = md_to_html(body_md)
            page = build_html(title, meta_desc, cat_dir, cat_name, slug, body_html)
            html_path = os.path.join(base, cat_dir, slug + '.html')
            with open(html_path, 'w') as fh:
                fh.write(page)
            total += 1
    print(f"Generated {total} HTML articles")

if __name__ == '__main__':
    main()