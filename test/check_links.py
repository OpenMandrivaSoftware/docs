#!/usr/bin/env python3
"""
Internal Link and Asset Validator for OpenMandriva Docs.

Scans the compiled Jekyll site directory to verify:
- Internal links (href) and assets (src) exist on disk.
- Page anchors (#id or <a name>) exist in current and target documents.
- Relative and absolute paths resolve correctly.
- Same-origin URLs matching site_url are validated as internal paths.
- URL-encoded characters and query parameters are properly handled.
- Directory links require a valid index.html.

Usage:
    python3 test/check_links.py [--site-dir DIR] [--site-url URL] [--baseurl URL]
"""

import argparse
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote


class HTMLResourceParser(HTMLParser):
    """Extracts internal links, asset sources, and anchor identifiers from HTML."""

    def __init__(self):
        super().__init__()
        self.links = []       # list of (tag, attr, url, line)
        self.anchors = set()  # set of anchor names / element ids

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Collect element IDs as anchor targets
        element_id = attrs_dict.get("id")
        if element_id:
            self.anchors.add(element_id)

        # Collect named anchors (<a name="...">)
        if tag == "a" and "name" in attrs_dict:
            self.anchors.add(attrs_dict["name"])

        line, _ = self.getpos()

        # Check href attributes
        if tag in ("a", "link", "area"):
            href = attrs_dict.get("href")
            if href:
                self.links.append((tag, "href", href, line))

        # Check src attributes
        if tag in ("img", "script", "iframe", "source", "video", "audio", "input"):
            src = attrs_dict.get("src")
            if src:
                self.links.append((tag, "src", src, line))


class LinkChecker:
    def __init__(self, site_dir="_site", site_url="https://docs.openmandriva.org", baseurl=""):
        self.site_dir = os.path.abspath(site_dir)
        self.site_url = site_url.rstrip("/") if site_url else ""
        self.baseurl = ("/" + baseurl.strip("/")) if baseurl and baseurl.strip("/") else ""
        self.parsed_site_url = urlparse(self.site_url) if self.site_url else None

        self.file_anchors = {}  # {abs_html_path: set(anchors)}
        self.file_links = {}    # {abs_html_path: list((tag, attr, url, line))}
        self.errors = []        # list of dict(source, link, reason, line)
        self.checked_count = 0

    def is_same_origin(self, parsed_url, raw_url):
        """Determine if a URL belongs to the site origin."""
        if not self.parsed_site_url or not self.parsed_site_url.netloc:
            return False

        if raw_url.startswith("//"):
            netloc = raw_url[2:].split("/")[0]
            return netloc == self.parsed_site_url.netloc

        if parsed_url.scheme in ("http", "https"):
            return parsed_url.netloc == self.parsed_site_url.netloc

        return False

    def scan(self):
        """Pass 1: Traverse the site directory and parse all HTML files."""
        if not os.path.isdir(self.site_dir):
            raise FileNotFoundError(f"Site directory '{self.site_dir}' does not exist.")

        for root, _, files in os.walk(self.site_dir):
            for file_name in files:
                if file_name.endswith(".html"):
                    file_path = os.path.join(root, file_name)
                    parser = HTMLResourceParser()
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                        parser.feed(fp.read())
                    self.file_anchors[file_path] = parser.anchors
                    self.file_links[file_path] = parser.links

    def validate(self):
        """Pass 2: Validate all links and anchors."""
        self.errors = []
        self.checked_count = 0

        for src_path, links in self.file_links.items():
            for tag, attr, raw_link, line in links:
                link = raw_link.strip()
                if not link:
                    continue

                # Skip non-HTTP schemes
                if link.startswith(("mailto:", "tel:", "javascript:", "data:", "irc:", "magnet:", "news:")):
                    continue

                parsed = urlparse(link)

                # Skip external links
                if parsed.scheme in ("http", "https") or link.startswith("//"):
                    if not self.is_same_origin(parsed, link):
                        continue

                self.checked_count += 1

                path_part = unquote(parsed.path)
                fragment = unquote(parsed.fragment)

                # Strip baseurl prefix if configured
                if self.baseurl and path_part.startswith(self.baseurl):
                    path_part = path_part[len(self.baseurl):]
                    if not path_part.startswith("/"):
                        path_part = "/" + path_part

                # Resolve filesystem target
                if not path_part:
                    # Same-page link (e.g. href="#anchor")
                    target_file = src_path
                elif path_part.startswith("/"):
                    # Site-root relative link
                    rel_to_root = path_part.lstrip("/")
                    target_path = os.path.normpath(os.path.join(self.site_dir, rel_to_root))
                    if os.path.isdir(target_path) or path_part.endswith("/"):
                        target_file = os.path.join(target_path, "index.html")
                    else:
                        target_file = target_path
                else:
                    # Document-relative link
                    src_dir = os.path.dirname(src_path)
                    target_path = os.path.normpath(os.path.join(src_dir, path_part))
                    if os.path.isdir(target_path) or path_part.endswith("/"):
                        target_file = os.path.join(target_path, "index.html")
                    else:
                        target_file = target_path

                # Check file existence
                if not os.path.exists(target_file):
                    self.errors.append({
                        "source": src_path,
                        "link": raw_link,
                        "line": line,
                        "reason": f"Target file does not exist: '{os.path.relpath(target_file, self.site_dir)}'"
                    })
                    continue

                # If target is a directory, require index.html
                if os.path.isdir(target_file):
                    index_file = os.path.join(target_file, "index.html")
                    if not os.path.isfile(index_file):
                        self.errors.append({
                            "source": src_path,
                            "link": raw_link,
                            "line": line,
                            "reason": f"Directory has no index.html: '{os.path.relpath(target_file, self.site_dir)}'"
                        })
                    continue

                # Check anchor existence in HTML documents
                if fragment and target_file.endswith(".html"):
                    anchors = self.file_anchors.get(target_file)
                    if anchors is None:
                        # Target is an external HTML or unparsed file
                        if not os.path.isfile(target_file):
                            self.errors.append({
                                "source": src_path,
                                "link": raw_link,
                                "line": line,
                                "reason": f"Target file does not exist: '{os.path.relpath(target_file, self.site_dir)}'"
                            })
                    elif fragment not in anchors:
                        self.errors.append({
                            "source": src_path,
                            "link": raw_link,
                            "line": line,
                            "reason": f"Anchor '#{fragment}' not found in '{os.path.relpath(target_file, self.site_dir)}'"
                        })

        return len(self.errors) == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate internal links and assets in Jekyll output.")
    parser.add_argument("--site-dir", default="_site", help="Path to compiled site directory (default: _site)")
    parser.add_argument("--site-url", default="https://docs.openmandriva.org", help="Site production URL")
    parser.add_argument("--baseurl", default="", help="Site baseurl (default: empty)")
    args = parser.parse_args(argv)

    checker = LinkChecker(site_dir=args.site_dir, site_url=args.site_url, baseurl=args.baseurl)

    try:
        checker.scan()
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2

    success = checker.validate()

    print(f"Checked {checker.checked_count} internal link(s) across '{checker.site_dir}'.")
    if not success:
        print(f"Found {len(checker.errors)} broken reference(s):", file=sys.stderr)
        for err in sorted(checker.errors, key=lambda x: (x["source"], x["line"]))[:50]:
            rel_src = os.path.relpath(err["source"], checker.site_dir)
            print(f"  [{rel_src}:{err['line']}] -> {err['link']} ({err['reason']})", file=sys.stderr)
        if len(checker.errors) > 50:
            print(f"  ... and {len(checker.errors) - 50} more.", file=sys.stderr)
        return 1

    print("All internal links, assets, and anchors are valid!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
