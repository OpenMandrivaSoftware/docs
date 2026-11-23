#!/usr/bin/env python3
"""
Internal Link and Asset Validator for OpenMandriva Docs.

Scans the compiled Jekyll site directory to verify:
- Internal links (href) and assets (src) exist on disk within site_dir.
- Link resolution accurately models the published web site (using urljoin).
- Links respect the configured baseurl publication scope (with segment boundary checks).
- Page anchors (#id or <a name>) exist in current and target HTML documents.
- Query strings and URL fragments are parsed correctly without breaking file resolution.
- Directory links require a valid index.html.

Usage:
    python3 test/check_links.py [--site-dir DIR] [--site-url URL] [--baseurl URL]
"""

import argparse
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin, unquote


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

        # Normalize baseurl: empty string or leading slash with no trailing slash, e.g. "/docs"
        raw_base = baseurl.strip() if baseurl else ""
        self.baseurl = ("/" + raw_base.strip("/")) if raw_base.strip("/") else ""

        # Default origin for URL resolution
        if self.site_url:
            self.origin = self.site_url
            self.expected_netloc = urlparse(self.site_url).netloc
        else:
            self.origin = "http://localhost"
            self.expected_netloc = "localhost"

        self.file_anchors = {}  # {abs_html_path: set(anchors)}
        self.file_links = {}    # {abs_html_path: list((tag, attr, url, line))}
        self.errors = []        # list of dict(source, link, reason, line)
        self.checked_count = 0

    def is_within_baseurl(self, path):
        """Check if URL path is within the configured baseurl with strict segment boundaries."""
        if not self.baseurl:
            return True
        if path == self.baseurl or path == self.baseurl + "/":
            return True
        return path.startswith(self.baseurl + "/")

    def strip_baseurl(self, path):
        """Remove baseurl prefix from URL path."""
        if not self.baseurl:
            return path
        if path == self.baseurl or path == self.baseurl + "/":
            return "/"
        if path.startswith(self.baseurl + "/"):
            return path[len(self.baseurl):]
        return path

    def get_source_public_url(self, src_path):
        """Determine the public URL of a source HTML file."""
        rel_path = os.path.relpath(src_path, self.site_dir)
        rel_url_path = "/".join(rel_path.split(os.sep))
        if self.baseurl:
            doc_path = f"{self.baseurl}/{rel_url_path}"
        else:
            doc_path = f"/{rel_url_path}"
        return f"{self.origin}{doc_path}"

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
        """Pass 2: Validate all links and anchors by modeling the published site."""
        self.errors = []
        self.checked_count = 0

        for src_path, links in self.file_links.items():
            source_public_url = self.get_source_public_url(src_path)

            for tag, attr, raw_link, line in links:
                link = raw_link.strip()
                if not link:
                    continue

                # Skip non-HTTP schemes
                if link.startswith(("mailto:", "tel:", "javascript:", "data:", "irc:", "magnet:", "news:")):
                    continue

                # Step 1 & 2: Resolve URL relative to source document using standard urljoin
                resolved_url = urljoin(source_public_url, link)
                parsed = urlparse(resolved_url)

                # Step 3: Check origin (skip external links)
                if parsed.netloc != self.expected_netloc:
                    continue

                self.checked_count += 1

                # Check publication scope (baseurl segment boundary)
                if not self.is_within_baseurl(parsed.path):
                    self.errors.append({
                        "source": src_path,
                        "link": raw_link,
                        "line": line,
                        "reason": f"Target URL '{parsed.path}' is outside baseurl scope '{self.baseurl}'"
                    })
                    continue

                # Step 4: Transform URL path into local file path
                unquoted_path = unquote(parsed.path)
                stripped_path = self.strip_baseurl(unquoted_path)
                rel_file_path = stripped_path.lstrip("/")

                if not rel_file_path or stripped_path.endswith("/"):
                    target_path = os.path.normpath(os.path.join(self.site_dir, rel_file_path, "index.html"))
                else:
                    candidate = os.path.normpath(os.path.join(self.site_dir, rel_file_path))
                    if os.path.isdir(candidate):
                        target_path = os.path.join(candidate, "index.html")
                    else:
                        target_path = candidate

                # Step 5: Ensure target stays strictly inside site_dir
                abs_target = os.path.abspath(target_path)
                try:
                    in_bounds = os.path.commonpath([self.site_dir, abs_target]) == self.site_dir
                except ValueError:
                    in_bounds = False

                if not in_bounds:
                    self.errors.append({
                        "source": src_path,
                        "link": raw_link,
                        "line": line,
                        "reason": f"Target resolves outside published site directory: '{raw_link}'"
                    })
                    continue

                # Step 6: Check file existence
                if not os.path.exists(target_path):
                    self.errors.append({
                        "source": src_path,
                        "link": raw_link,
                        "line": line,
                        "reason": f"Target file does not exist: '{os.path.relpath(target_path, self.site_dir)}'"
                    })
                    continue

                # If target is a directory, require index.html
                if os.path.isdir(target_path):
                    index_file = os.path.join(target_path, "index.html")
                    if not os.path.isfile(index_file):
                        self.errors.append({
                            "source": src_path,
                            "link": raw_link,
                            "line": line,
                            "reason": f"Directory has no index.html: '{os.path.relpath(target_path, self.site_dir)}'"
                        })
                    target_path = index_file

                # Check anchor existence in target HTML file
                fragment = unquote(parsed.fragment)
                if fragment and target_path.endswith(".html"):
                    anchors = self.file_anchors.get(target_path)
                    if anchors is None:
                        if not os.path.isfile(target_path):
                            self.errors.append({
                                "source": src_path,
                                "link": raw_link,
                                "line": line,
                                "reason": f"Target file does not exist: '{os.path.relpath(target_path, self.site_dir)}'"
                            })
                    elif fragment not in anchors:
                        self.errors.append({
                            "source": src_path,
                            "link": raw_link,
                            "line": line,
                            "reason": f"Anchor '#{fragment}' not found in '{os.path.relpath(target_path, self.site_dir)}'"
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
