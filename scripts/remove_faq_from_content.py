#!/usr/bin/env python3
"""
Remove FAQ markdown sections from article content since FAQ is rendered from frontmatter in ArticleLayout.
"""

import re
from pathlib import Path

ARTICLES_DIR = Path("/home/gobeam/Projects/joyofcare-web/src/content/articles")

def remove_faq_section(content):
    """Remove the FAQ markdown section from article content."""
    # Pattern to match "## Pertanyaan yang Sering Diajukan (FAQ...)" with any suffix
    # and everything until the next ## heading or end of content
    pattern = r'\n## Pertanyaan yang Sering Diajukan \(FAQ[^)]*\)\n.*?(?=\n## |\n### |\n---\n|\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    pattern2 = r'\n## Pertanyaan yang Sering Diajukan\n.*?(?=\n## |\n### |\n---\n|\Z)'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip() + '\n'

def main():
    articles = list(ARTICLES_DIR.glob("*.mdx"))
    print(f"Processing {len(articles)} articles...")
    
    updated = 0
    for article_path in articles:
        content = article_path.read_text(encoding='utf-8')
        original = content
        
        content = remove_faq_section(content)
        
        if content != original:
            article_path.write_text(content, encoding='utf-8')
            updated += 1
            print(f"  ✓ {article_path.name}")
        else:
            print(f"  - {article_path.name} (no FAQ section found)")
    
    print(f"\nDone: {updated} articles updated")

if __name__ == "__main__":
    main()