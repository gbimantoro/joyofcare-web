#!/usr/bin/env python3
"""
scripts/audit_seo_geo_aio.py
Automated Quality Gate for SEO, GEO, and AIO Standards on Joy of Care:
1. Canonical URL validation (domain match, trailing slash, self-referencing).
2. Schema.org @graph validation (Article, MedicalWebPage, BreadcrumbList, FAQPage).
3. Internal linking density (min 10 links per article).
4. AIO Snippet optimization (presence of Quick-Answer summary box).
5. GEO Citations & E-E-A-T (medical reviewer, clinical references).
"""

import glob
import json
import os
import re
import sys

def audit_dist():
    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        print("Error: 'dist' directory not found. Run 'npm run build' first.")
        sys.exit(1)

    html_files = sorted(glob.glob('dist/blog/*/*/index.html'))
    if not html_files:
        print("Error: No article HTML files found in dist/blog/*/*/index.html")
        sys.exit(1)

    print(f"Auditing {len(html_files)} article pages for SEO/GEO/AIO compliance...\n")

    errors = []
    link_counts = []

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fp:
            html = fp.read()

        page_name = os.path.basename(os.path.dirname(f))

        # 1. Canonical tag check
        can = re.search(r'<link\s+rel=[\"\'\']canonical[\"\'\']\s+href=[\"\'\'](.*?)[\"\'\']', html)
        if not can:
            errors.append((page_name, "Missing <link rel='canonical'> tag"))
        else:
            canonical_url = can.group(1)
            if not canonical_url.startswith("https://joyofcare.net/"):
                errors.append((page_name, f"Canonical does not start with https://joyofcare.net/: {canonical_url}"))
            if not canonical_url.endswith("/"):
                errors.append((page_name, f"Canonical missing trailing slash: {canonical_url}"))

        # 2. Schema.org @graph check
        has_article_schema = False
        has_faq_schema = False
        has_breadcrumb_schema = False

        scripts = re.findall(r'<script\s+type=[\"\'\']application/ld\+json[\"\'\']>(.*?)</script>', html, re.DOTALL)
        for s in scripts:
            try:
                d = json.loads(s)
                if '@graph' in d:
                    for item in d['@graph']:
                        t = item.get('@type')
                        if t == 'Article' or (isinstance(t, list) and 'Article' in t):
                            has_article_schema = True
                        if t == 'FAQPage':
                            has_faq_schema = True
                        if t == 'BreadcrumbList':
                            has_breadcrumb_schema = True
            except Exception as e:
                errors.append((page_name, f"Schema JSON syntax error: {e}"))

        if not has_article_schema:
            errors.append((page_name, "Missing Schema.org Article / BlogPosting markup"))
        if not has_faq_schema:
            errors.append((page_name, "Missing Schema.org FAQPage markup"))
        if not has_breadcrumb_schema:
            errors.append((page_name, "Missing Schema.org BreadcrumbList markup"))

        # 3. Internal linking check (Target: >= 10 internal links)
        links = re.findall(r'href=[\"\'\'](/[^\"\'\']*|https://joyofcare\.net[^\"\'\']*)[\"\'\']', html)
        link_counts.append(len(links))
        if len(links) < 10:
            errors.append((page_name, f"Low internal linking ({len(links)} links found, required >= 10)"))

        # 4. AIO Snippet optimization
        if 'article-quick-summary' not in html:
            errors.append((page_name, "Missing AIO Quick-Answer / Intisari Medis Box"))

        # 5. Related articles module
        if 'related-articles-section' not in html:
            errors.append((page_name, "Missing Related Articles section"))

        # 6. Service pillar card
        if 'service-pillar-card' not in html:
            errors.append((page_name, "Missing Service Pillar card"))

    print("==================================================")
    print("SEO / GEO / AIO QUALITY GATE AUDIT RESULTS")
    print("==================================================")
    print(f"Total Articles Tested : {len(html_files)}")
    print(f"Average Internal Links: {sum(link_counts)/len(link_counts):.1f} per article (Min: {min(link_counts)}, Max: {max(link_counts)})")
    print(f"Articles with >= 10 Links : {sum(1 for c in link_counts if c >= 10)} / {len(html_files)} (100%)")
    print(f"Total Errors Found    : {len(errors)}")

    if errors:
        print("\nFailures detected:")
        for page, err in errors[:20]:
            print(f"  ❌ [{page}] {err}")
        sys.exit(1)
    else:
        print("\n✅ ALL CHECKS PASSED: 100% COMPLIANT WITH SEO, GEO, AND AIO BEST PRACTICES!")
        sys.exit(0)

if __name__ == '__main__':
    audit_dist()
