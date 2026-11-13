#!/usr/bin/env python3
"""
OpenMandriva Docs - Generated Site Verifier
Verifies that all 177 baseline generated HTML routes exist in _site,
have non-empty content, and match their intended page_id and content language.
Supports following redirect chains (with cycle detection) to verify destination
contracts for legacy routes.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOC_PID_RE = re.compile(r'<meta name="doc-page-id" content="([^"]+)">')
DOC_LANG_RE = re.compile(r'<meta name="doc-content-lang" content="([^"]+)">')
HTTP_REFRESH_RE = re.compile(r'<meta\s+http-equiv="refresh"\s+content="[^"]*url=([^"]+)"', re.IGNORECASE)


class SiteVerifier:
    def __init__(self, site_dir="_site", routes_path=".agents/i18n-architecture/legacy_routes.json", baseurl=""):
        self.site_dir = Path(site_dir)
        if not self.site_dir.is_absolute():
            self.site_dir = REPO_ROOT / self.site_dir

        self.routes_path = Path(routes_path)
        if not self.routes_path.is_absolute():
            self.routes_path = REPO_ROOT / self.routes_path

        self.baseurl = baseurl.rstrip("/") if baseurl else ""
        self.errors = []
        self.verified_count = 0

    def resolve_destination(self, start_file, initial_content):
        """Follow redirect chain starting from start_file, returning (final_rel_file, final_content, visited_urls, error)."""
        visited = [start_file]
        curr_content = initial_content
        curr_file = start_file
        max_redirects = 5

        for _ in range(max_redirects):
            m_ref = HTTP_REFRESH_RE.search(curr_content)
            if not m_ref:
                # Not a redirect, reached target document
                return curr_file, curr_content, visited, None

            raw_target = m_ref.group(1).strip()
            # Clean URL: strip fragment and query string
            clean_url = raw_target.split("?")[0].split("#")[0]
            if self.baseurl and clean_url.startswith(self.baseurl):
                clean_url = clean_url[len(self.baseurl):]

            # Map URL to file in _site
            path_str = clean_url.lstrip("/")
            if not path_str or clean_url.endswith("/"):
                dest_file = f"{path_str}index.html" if path_str else "index.html"
            else:
                dest_file = path_str

            if dest_file in visited:
                cycle_str = " -> ".join(visited + [dest_file])
                return dest_file, None, visited, f"Redirect loop/cycle detected: {cycle_str}"

            visited.append(dest_file)
            target_path = self.site_dir / dest_file
            if not target_path.is_file():
                return dest_file, None, visited, f"Redirect target '{raw_target}' (file '{dest_file}') does not exist on disk"

            curr_file = dest_file
            curr_content = target_path.read_text(encoding="utf-8")

        return curr_file, None, visited, f"Exceeded maximum redirect depth ({max_redirects})"

    def verify(self):
        self.errors.clear()
        self.verified_count = 0

        # 1. Require site directory to exist
        if not self.site_dir.exists():
            self.errors.append(f"Generated site directory '{self.site_dir}' does not exist. Run Jekyll build first.")
            return False

        if not self.site_dir.is_dir():
            self.errors.append(f"Expected site path '{self.site_dir}' is not a directory.")
            return False

        # 2. Require routes manifest to exist
        if not self.routes_path.is_file():
            self.errors.append(f"Routes manifest '{self.routes_path}' does not exist.")
            return False

        try:
            manifest = json.loads(self.routes_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.errors.append(f"Failed to parse routes manifest '{self.routes_path}': {e}")
            return False

        routes = manifest.get("routes", [])
        if not routes:
            self.errors.append(f"No routes found in manifest '{self.routes_path}'.")
            return False

        # 3. Verify each baseline route
        for r in routes:
            rel_file = r.get("file_in_site")
            if not rel_file:
                self.errors.append(f"Route entry missing 'file_in_site': {r}")
                continue

            target_path = self.site_dir / rel_file
            if not target_path.is_file():
                self.errors.append(
                    f"Missing generated file for route '{r.get('public_url')}': expected '{target_path}'"
                )
                continue

            content = target_path.read_text(encoding="utf-8")
            if len(content.strip()) < 50:
                self.errors.append(
                    f"Generated file '{rel_file}' is suspiciously small or empty ({len(content)} bytes)"
                )
                continue

            expected_pid = r.get("page_id")
            expected_lang = r.get("actual_content_lang")
            pub_url = r.get("public_url")
            req_locale = r.get("requested_locale")

            # Validate role-specific contracts
            if expected_pid == "system.404":
                # System 404 page contract
                if "404" not in content and "not found" not in content.lower():
                    self.errors.append(f"System 404 page '{rel_file}' missing 404 error indicators")
            else:
                final_file, final_content, visited, redirect_err = self.resolve_destination(rel_file, content)
                if redirect_err:
                    self.errors.append(f"Route '{pub_url}' ({rel_file}): {redirect_err}")
                    continue

                # Validate requested locale contract
                if req_locale == "en":
                    if final_file.startswith("fr/"):
                        self.errors.append(
                            f"Route '{pub_url}' requested locale 'en' but resolved to French file '{final_file}'"
                        )
                elif req_locale == "fr":
                    if not final_file.startswith("fr/"):
                        self.errors.append(
                            f"Route '{pub_url}' requested locale 'fr' but resolved to English file '{final_file}'"
                        )

                # Validate content document metadata on final target
                m_pid = DOC_PID_RE.search(final_content)
                m_lang = DOC_LANG_RE.search(final_content)

                if not m_pid:
                    self.errors.append(
                        f"Resolved document '{final_file}' for route '{pub_url}' missing <meta name=\"doc-page-id\">"
                    )
                elif m_pid.group(1) != expected_pid:
                    self.errors.append(
                        f"Resolved document '{final_file}' for route '{pub_url}' page_id mismatch: expected '{expected_pid}', found '{m_pid.group(1)}'"
                    )

                if not m_lang:
                    self.errors.append(
                        f"Resolved document '{final_file}' for route '{pub_url}' missing <meta name=\"doc-content-lang\">"
                    )
                elif m_lang.group(1) != expected_lang:
                    self.errors.append(
                        f"Resolved document '{final_file}' for route '{pub_url}' content language mismatch: expected '{expected_lang}', found '{m_lang.group(1)}'"
                    )

            self.verified_count += 1

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Verify OpenMandriva Docs generated site routes and metadata.")
    parser.add_argument(
        "--site-dir",
        default="_site",
        help="Path to generated site directory (default: _site)",
    )
    parser.add_argument(
        "--routes",
        default=".agents/i18n-architecture/legacy_routes.json",
        help="Path to legacy_routes.json manifest",
    )
    parser.add_argument(
        "--baseurl",
        default="",
        help="Configured baseurl of the site (default: '')",
    )

    args = parser.parse_args()
    verifier = SiteVerifier(site_dir=args.site_dir, routes_path=args.routes, baseurl=args.baseurl)

    print(f"Verifying generated site '{verifier.site_dir}' against routes manifest '{verifier.routes_path}'...")
    success = verifier.verify()

    if success:
        print(f"Site verification PASSED: All {verifier.verified_count} generated routes verified with matching identities and content languages.")
        sys.exit(0)
    else:
        print(f"Site verification FAILED with {len(verifier.errors)} error(s):")
        for err in verifier.errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
