#!/usr/bin/env python3
"""
Remove duplicate FAQ markdown sections from article content and ensure all questions
are preserved in frontmatter `faq` for ArticleLayout accordion and JSON-LD schema.
"""

import os
import re
import sys
from pathlib import Path
import yaml

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "articles"


FAQ_GUIDE_SLUGS = {
    "syarat-kesehatan-studi-luar-negeri-vaksin-mcu-yang-perlu-anda-ketahui",
    "tips-kesehatan-untuk-mahasiswa-kuliah-di-luar-negeri-yang-perlu-anda-ketahui",
    "antar-jemput-rumah-sakit-jakarta-harga-yang-perlu-anda-ketahui",
    "dokter-umum-ke-rumah-tangerang-yang-perlu-anda-ketahui",
    "akupuntur-untuk-nyeri-sendi-lansia-yang-perlu-anda-ketahui",
    "vaksin-di-rumah-jakarta-lansia-yang-perlu-anda-ketahui",
    "kesehatan-lansia-sehat-rutinitas-harian-yang-perlu-anda-ketahui",
    "osteoporosis-pada-lansia-pencegahan-dan-perawatan-yang-perlu-anda-ketahui",
}


def clean_question_text(q_raw: str) -> str:
    """Clean question text: remove leading numbers/bullets and extra whitespace."""
    q = re.sub(r'^\s*\d+[\.\)]\s*', '', q_raw).strip()
    return q


def clean_answer_text(a_raw: str) -> str:
    """Clean answer text: remove **Jawab**: prefix and extra whitespace."""
    a = re.sub(r'^\s*\*\*Jawab\*\*:\s*', '', a_raw, flags=re.I).strip()
    return a


def process_article(fpath: Path) -> tuple[bool, str]:
    if fpath.stem in FAQ_GUIDE_SLUGS:
        return True, "Skipped FAQ-guide article (content is structured Q&A guide)"

    content = fpath.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "Not enough frontmatter delimiters"

    fm_raw = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except Exception as e:
        return False, f"YAML parse error: {e}"

    # 1. Locate the final --- in the body that precedes the CTA section
    all_seps = list(re.finditer(r"\n---\n", body))
    if not all_seps:
        return False, "No '---' separator found in body"

    last_sep = all_seps[-1]
    cta_text = body[last_sep.end():].strip()
    faq_end_pos = last_sep.start()

    # 2. Find all ### headings before the final separator
    before_sep = body[:faq_end_pos]
    h3_matches = list(re.finditer(r"###\s+([^\n]+)", before_sep))
    if not h3_matches:
        return False, "No ### headings before final separator"

    # 3. Walk backwards from the last H3 before separator to collect consecutive question headings
    faq_h3s = []
    for h in reversed(h3_matches):
        text = h.group(1).strip()
        if "?" in text:
            faq_h3s.append(h)
        else:
            break

    if not faq_h3s:
        return True, "Already clean (no FAQ questions before final separator)"

    faq_h3s.reverse()

    # 4. Extract questions and answers from this block
    extracted_faqs = []
    for i, h in enumerate(faq_h3s):
        q_raw = h.group(1).strip()
        q_clean = clean_question_text(q_raw)
        ans_start = h.end()
        ans_end = faq_h3s[i + 1].start() if i + 1 < len(faq_h3s) else faq_end_pos
        ans_raw = before_sep[ans_start:ans_end].strip()
        ans_clean = clean_answer_text(ans_raw)
        if q_clean and ans_clean:
            extracted_faqs.append({"question": q_clean, "answer": ans_clean})

    # 5. Merge with existing frontmatter faqs
    fm_faqs = fm.get("faq") or []
    if not isinstance(fm_faqs, list):
        fm_faqs = []

    merged_faqs = list(fm_faqs)
    for ef in extracted_faqs:
        eq_norm = re.sub(r'[^a-zA-Z0-9]', '', ef["question"].lower())
        exists = any(
            eq_norm in re.sub(r'[^a-zA-Z0-9]', '', f.get("question", "").lower())
            or re.sub(r'[^a-zA-Z0-9]', '', f.get("question", "").lower()) in eq_norm
            for f in merged_faqs if isinstance(f, dict)
        )
        if not exists:
            merged_faqs.append(ef)

    fm["faq"] = merged_faqs

    # 6. Determine the start of the FAQ section in body
    first_q_pos = faq_h3s[0].start()
    preceding_text = body[:first_q_pos]

    h2_match = re.search(r"(\n##\s+[^\n]*(?:Pertanyaan|FAQ|Tanya Jawab)[^\n]*\n\s*)$", preceding_text, re.I)
    if h2_match:
        faq_start_pos = h2_match.start()
        pre_h2 = body[:faq_start_pos]
        sep_pre = re.search(r"(\n---\n\s*)$", pre_h2)
        if sep_pre:
            faq_start_pos = sep_pre.start()
    else:
        sep_match = re.search(r"(\n---\n\s*)$", preceding_text)
        if sep_match:
            faq_start_pos = sep_match.start()
        else:
            faq_start_pos = first_q_pos

    # 7. Construct the new body: content before FAQ, then ---, then CTA
    article_main_content = body[:faq_start_pos].rstrip()
    new_body = f"\n\n{article_main_content}\n\n---\n\n{cta_text}\n"
    new_body = re.sub(r"\n{3,}", "\n\n", new_body)

    # 8. Rebuild frontmatter
    new_fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, width=1000)
    new_content = f"---\n{new_fm_str}---{new_body}"

    fpath.write_text(new_content, encoding="utf-8")
    return True, f"Cleaned {len(extracted_faqs)} Qs, total FM FAQs: {len(merged_faqs)}"


def main():
    articles = sorted(ARTICLES_DIR.glob("*.mdx"))
    print(f"Processing {len(articles)} articles in {ARTICLES_DIR}...")

    success_count = 0
    fail_count = 0

    for article_path in articles:
        ok, msg = process_article(article_path)
        if ok:
            success_count += 1
            print(f"  ✓ {article_path.name}: {msg}")
        else:
            fail_count += 1
            print(f"  ✗ {article_path.name}: {msg}")

    print(f"\nDone: {success_count} succeeded, {fail_count} failed out of {len(articles)} articles.")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())