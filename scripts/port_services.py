#!/usr/bin/env python3
"""Port enriched static service pages to Astro routes reusing BaseLayout."""
import os, re, json

BASE = "/home/gobeam/Projects/joyofcare-web"
PAGES_DIR = os.path.join(BASE, "pages")
OUT_DIR = os.path.join(BASE, "src", "pages")

# filename -> (route dir, category label) ; None skip
SERVICES = {
    "panggil-dokter-ke-rumah.html": "panggil-dokter-ke-rumah",
    "layanan-fisioterapi-ke-rumah.html": "layanan-fisioterapi-ke-rumah",
    "layanan-perawat-di-rumah.html": "layanan-perawat-di-rumah",
    "layanan-akupuntur-di-rumah.html": "layanan-akupuntur-di-rumah",
    "homelab.html": "homelab",
    "infus-suntik-vitamin-di-rumah.html": "infus-suntik-vitamin-di-rumah",
    "transcare-antar-jemput-ke-rs-jakarta-tangerang.html": "transcare-antar-jemput-ke-rs-jakarta-tangerang",
    "layanan-lengkap.html": "layanan-lengkap",
}


def get_meta(h, key):
    m = re.search(rf'<meta name="{key}" content="([^"]+)"', h)
    return m.group(1) if m else ""


def main():
    for fname, route in SERVICES.items():
        h = open(os.path.join(PAGES_DIR, fname), encoding="utf-8").read()
        title = get_meta(h, "title") or get_meta(h, "og:title")
        title = title or route.replace("-", " ").title()
        desc = get_meta(h, "description")
        # extract main body between </nav> and <footer
        m = re.search(r"</nav>(.*?)<footer", h, re.DOTALL)
        body = m.group(1) if m else ""
        # remove the breadcrumbs nav that links to old relative home? keep as is (uses / and /blog/)
        astro = f"""---
import BaseLayout from '../layouts/BaseLayout.astro';
import {{ SITE_URL }} from '../consts';

export const prerender = true;

const title = {json.dumps(title)};
const description = {json.dumps(desc)};
const canonical = `${{SITE_URL}}/{route}`;
---

<BaseLayout title={{title}} description={{description}} canonicalURL={{canonical}}>
{body}
</BaseLayout>
"""
        out_path = os.path.join(OUT_DIR, route + ".astro")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(astro)
        print(f"Created {route}.astro ({len(body)} chars body)")


if __name__ == "__main__":
    main()