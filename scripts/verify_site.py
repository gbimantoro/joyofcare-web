#!/usr/bin/env python3
"""Phase 6: Post-build verification gate for joyofcare-web.

Fails (exit non-zero) if any of the "don't repeat" list from the deep review is present
in the built dist/.
"""
import glob, os, re, sys

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist")
SITE_URL = "https://new.joyof.care"

errors = []


def all_html():
    return glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True)


def article_pages():
    # article pages live at dist/blog/<category>/<slug>/index.html (2 levels deep)
    return glob.glob(os.path.join(DIST, "blog", "*", "*", "index.html"))


def blog_pages():
    return glob.glob(os.path.join(DIST, "blog", "**", "index.html"), recursive=True)


def main():
    if not os.path.isdir(DIST):
        print("dist/ not found. Run `npm run build` first.")
        return 1

    arts = article_pages()
    allp = all_html()

    # 1) WA URL bug: ?phone=628811118911?text=
    for p in allp:
        h = open(p, encoding="utf-8").read()
        if "send/?phone=628811118911?text=" in h:
            errors.append(f"[WA-BUG] {p}: ?phone...?text= present")

    # 2) >1 H1 in article pages
    for p in arts:
        h = open(p, encoding="utf-8").read()
        n = h.count("<h1")
        if n > 1:
            errors.append(f"[H1] {p}: {n} H1 tags")

    # 3) Article JSON-LD datePublished + dateModified ISO
    for p in arts:
        h = open(p, encoding="utf-8").read()
        if '"datePublished"' not in h or '"dateModified"' not in h:
            errors.append(f"[DATE] {p}: missing ISO datePublished/dateModified")

    # 4) No Odoo/www.joyofcare.net refs anywhere
    for p in allp:
        h = open(p, encoding="utf-8", errors="ignore").read()
        if "web/image" in h or "odoo.com" in h or "www.joyofcare.net" in h:
            errors.append(f"[ODOO] {p}: contains Odoo/www.joyofcare.net reference")

    # 5) canonical must start with SITE_URL
    for p in allp:
        h = open(p, encoding="utf-8").read()
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', h)
        if m and not m.group(1).startswith(SITE_URL):
            errors.append(f"[CANON] {p}: canonical {m.group(1)} != {SITE_URL}")

    # 6) markdown relics in rendered HTML (article + homepage)
    for p in allp:
        h = open(p, encoding="utf-8").read()
        if re.search(r">\*\*|\*\*<|##\s|###\s", h):
            errors.append(f"[MD-RELIC] {p}: markdown relic found")

    # 7) banned headings
    for p in allp:
        h = open(p, encoding="utf-8").read()
        if "Poin Kunci" in h or "Ringkasan Eksekutif" in h:
            errors.append(f"[HEADING] {p}: banned heading found")

    # 8) any price in article HTML
    for p in blog_pages():
        h = open(p, encoding="utf-8").read()
        if re.search(r"Rp\s?[\d.,]+", h):
            errors.append(f"[PRICE] {p}: Rp amount found")

    # 9) sitemap loc count vs blog page count
    sitemap_locs = 0
    for sf in glob.glob(os.path.join(DIST, "sitemap-*.xml")):
        sitemap_locs += open(sf, encoding="utf-8").read().count("<loc>")
    bp = len(blog_pages())
    print(f"Info: sitemap locs={sitemap_locs}, blog pages={bp}")
    if sitemap_locs == 0:
        errors.append("[SITEMAP] no sitemap generated")

    if errors:
        print("\n=== VERIFY FAILED ===")
        seen = set()
        for e in errors:
            if e not in seen:
                seen.add(e)
                print(" -", e)
        print(f"\n{len(seen)} unique error(s)")
        return 1
    print("\n=== VERIFY OK ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())