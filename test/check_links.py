#!/usr/bin/env python3
"""
Internal Link and Anchor Checker for OpenMandriva Docs.
Scans the generated `_site` directory for broken internal links and assets.
Usage:
    python3 test/check_links.py
"""

import os
import re
import sys
from urllib.parse import urlparse, unquote

def check_site(site_dir='_site'):
    site_dir = os.path.abspath(site_dir)
    if not os.path.isdir(site_dir):
        print(f"Error: Directory '{site_dir}' not found. Run 'bundle exec jekyll build' first.")
        return 1

    broken = []
    total_links = 0

    for root, dirs, files in os.walk(site_dir):
        for f in files:
            if not f.endswith('.html'):
                continue
            html_path = os.path.join(root, f)
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()

            links = re.findall(r'href=[\"\']([^\"\']+)[\"\']', content)
            for link in links:
                if link.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', 'tel:', '//')):
                    continue
                if link in ('/fr/', '/fr', '/'):
                    # Check for index.html in that root
                    target_dir = os.path.join(site_dir, link.strip('/'))
                    if not os.path.isfile(os.path.join(target_dir, 'index.html')) and not os.path.isfile(os.path.join(target_dir, 'index.en.html')):
                        broken.append((html_path, link, target_dir))
                    continue

                total_links += 1
                path = link.split('?')[0].split('#')[0]
                if not path:
                    continue

                if path.startswith('/'):
                    target = os.path.join(site_dir, path.lstrip('/'))
                else:
                    target = os.path.normpath(os.path.join(root, path))

                if os.path.isdir(target):
                    index_target = os.path.join(target, 'index.html')
                    index_en = os.path.join(target, 'index.en.html')
                    if not os.path.isfile(index_target) and not os.path.isfile(index_en):
                        broken.append((html_path, link, target))
                elif not os.path.isfile(target):
                    broken.append((html_path, link, target))

    print(f"Checked {total_links} internal links across '{site_dir}'.")
    if broken:
        print(f"Found {len(broken)} broken link(s):")
        unique_broken = set((os.path.relpath(src, site_dir), l) for src, l, t in broken)
        for src, l in sorted(unique_broken)[:50]:
            print(f"  [{src}] -> {l}")
        if len(unique_broken) > 50:
            print(f"  ... and {len(unique_broken) - 50} more.")
        return 1

    print("All internal links are valid!")
    return 0

if __name__ == '__main__':
    sys.exit(check_site())
