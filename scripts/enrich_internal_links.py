#!/usr/bin/env python3
"""
scripts/enrich_internal_links.py
Enriches markdown articles with natural, contextual internal links to key service pages.
Guarantees:
- At most 1 link per service target per article.
- At most 1 link per paragraph.
- Never links inside headings (#), tables (|), code blocks, or existing links [text](url).
- Maintains high editorial quality (Kompas-standard readability).
"""

import glob
import re
import os

KEYWORDS_MAP = [
    (r'\b(panggil dokter ke rumah|dokter visit ke rumah|dokter panggil ke rumah|kunjungan dokter ke rumah|dokter ke rumah)\b', '/panggil-dokter-ke-rumah/'),
    (r'\b(fisioterapi ke rumah|fisioterapi di rumah|fisioterapi stroke di rumah|fisioterapi stroke|sesi fisioterapi)\b', '/layanan-fisioterapi-ke-rumah/'),
    (r'\b(perawat ke rumah|perawat homecare|perawat home care|perawat lansia di rumah|perawat lansia|perawat medis)\b', '/layanan-perawat-di-rumah/'),
    (r'\b(vaksinasi di rumah|vaksin ke rumah|vaksinasi keluarga di rumah|vaksinasi lansia|vaksin di rumah)\b', '/layanan-vaksinasi-di-rumah/'),
    (r'\b(infus vitamin di rumah|suntik vitamin di rumah|terapi infus vitamin|infus vitamin|suntik vitamin)\b', '/infus-suntik-vitamin-di-rumah/'),
    (r'\b(cek darah di rumah|cek lab di rumah|pemeriksaan laboratorium di rumah|home lab|pemeriksaan darah di rumah|cek darah)\b', '/homelab/'),
    (r'\b(layanan akupuntur di rumah|akupuntur medis di rumah|akupuntur medis)\b', '/layanan-akupuntur-di-rumah/'),
    (r'\b(transportasi medis non-darurat|antar jemput pasien ke rumah sakit|layanan TransCare|antar jemput pasien|transportasi medis)\b', '/transcare-antar-jemput-ke-rs-jakarta-tangerang/'),
]

def enrich_article(content: str) -> tuple[str, int]:
    # Separate frontmatter from body
    parts = re.split(r'(^---\n.*?\n---\n)', content, flags=re.DOTALL)
    if len(parts) < 3:
        return content, 0

    header = parts[1]
    body = parts[2]

    # Collect existing targets already linked in the article
    existing_targets = set(re.findall(r'\[.*?\]\((/.*?/|https://(?:www\.)?joyofcare\.net/.*?/)\)', body))
    normalized_existing = set()
    for t in existing_targets:
        m = re.search(r'https?://[^/]+(/.*)', t)
        if m:
            normalized_existing.add(m.group(1))
        else:
            normalized_existing.add(t)

    used_targets = set(normalized_existing)
    added_count = 0

    paragraphs = body.split('\n\n')
    new_paragraphs = []

    for p in paragraphs:
        trimmed = p.strip()
        # Skip headings, tables, blockquotes, code blocks, or HTML tags
        if not trimmed or trimmed.startswith('#') or trimmed.startswith('|') or trimmed.startswith('```') or trimmed.startswith('<'):
            new_paragraphs.append(p)
            continue

        mod_p = p
        for regex_pat, target_url in KEYWORDS_MAP:
            if target_url in used_targets:
                continue

            matches = list(re.finditer(regex_pat, mod_p, flags=re.IGNORECASE))
            if not matches:
                continue

            replaced = False
            for m in matches:
                start, end = m.span()
                matched_phrase = m.group(1)

                prefix = mod_p[:start]
                suffix = mod_p[end:]

                # In markdown: inside link text if open '[' without closing ']' before start
                open_brackets = prefix.count('[') - prefix.count(']')
                open_parens = prefix.count('(') - prefix.count(')')

                if open_brackets > 0 or open_parens > 0:
                    continue

                # Valid match: replace it
                mod_p = prefix + f'[{matched_phrase}]({target_url})' + suffix
                used_targets.add(target_url)
                added_count += 1
                replaced = True
                break

            if replaced:
                # Max 1 link injected per paragraph to preserve reading flow
                break

        new_paragraphs.append(mod_p)

    new_content = header + '\n\n'.join(new_paragraphs)
    return new_content, added_count

def main():
    files = sorted(glob.glob('src/content/articles/*.mdx') + glob.glob('src/content/articles/*.md'))
    total_added = 0
    modified_files = 0

    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            original = fp.read()

        enriched, count = enrich_article(original)
        if count > 0:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(enriched)
            total_added += count
            modified_files += 1

    print(f"Total articles inspected: {len(files)}")
    print(f"Articles enriched with contextual links: {modified_files}")
    print(f"Total contextual links added: {total_added}")
    print(f"Average links added per article: {total_added / len(files):.2f}")

if __name__ == '__main__':
    main()
