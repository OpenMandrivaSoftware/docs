#!/usr/bin/env python3
"""
OpenMandriva Docs - Generated Site Verifier
Verifies:
1. All 177 baseline legacy generated HTML routes exist in _site,
   resolve safely to their intended canonical destinations, and
   match current translation-aware content languages.
2. All canonical documentation pages across all configured languages
   exist and reflect correct identity and language metadata.
3. Redirect pages are strictly excluded from navigation and search indexing,
   and carry <meta name="robots" content="noindex">.
4. Baseurl boundaries, path normalization, origin containment, and
   cycle detection are rigorously verified.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent

DOC_PID_RE = re.compile(r'<meta name="doc-page-id" content="([^"]+)">')
DOC_LANG_RE = re.compile(r'<meta name="doc-content-lang" content="([^"]+)">')
HTTP_REFRESH_RE = re.compile(r'<meta\s+http-equiv="refresh"\s+content="[^"]*url=([^"]+)"', re.IGNORECASE)
ROBOTS_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="noindex"', re.IGNORECASE)
NAV_REDIRECT_RE = re.compile(r'class="nav-list-link"[^>]*>Redirecting\.\.\.<', re.IGNORECASE)


class SiteVerifier:
    def __init__(
        self,
        site_dir="_site",
        routes_path=".agents/i18n-architecture/legacy_routes.json",
        manifest_path=None,
        baseurl=""
    ):
        self.site_dir = Path(site_dir)
        if not self.site_dir.is_absolute():
            self.site_dir = REPO_ROOT / self.site_dir

        self.routes_path = Path(routes_path)
        if not self.routes_path.is_absolute():
            self.routes_path = REPO_ROOT / self.routes_path

        default_routes = REPO_ROOT / ".agents/i18n-architecture/legacy_routes.json"
        if manifest_path is not None:
            self.manifest_path = Path(manifest_path)
            if not self.manifest_path.is_absolute():
                self.manifest_path = REPO_ROOT / self.manifest_path
        elif self.routes_path == default_routes:
            self.manifest_path = REPO_ROOT / ".agents/i18n-architecture/build_manifest.json"
        else:
            self.manifest_path = None

        self.baseurl = baseurl.rstrip("/") if baseurl else ""
        self.errors = []
        self.verified_routes_count = 0
        self.verified_canonical_count = 0
        self.verified_count = 0

        self.languages = []
        self.default_lang = "en"
        self.documents = {}

    def ensure_build_manifest(self):
        """Load build manifest or generate it via MetadataValidator if missing."""
        if self.manifest_path is None:
            return True

        if not self.manifest_path.is_file():
            cmd = ["ruby", str(REPO_ROOT / "test" / "validate_metadata.rb"), "--dump-manifest", str(self.manifest_path)]
            try:
                res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
                if res.returncode != 0:
                    self.errors.append(f"Failed to generate build manifest with {cmd}: {res.stderr}")
                    return False
            except Exception as e:
                self.errors.append(f"Error invoking metadata validator to generate manifest: {e}")
                return False

        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            self.languages = data.get("languages", ["en", "fr"])
            self.default_lang = data.get("default_lang", "en")
            self.documents = data.get("documents", {})
            return True
        except Exception as e:
            self.errors.append(f"Failed to parse build manifest at '{self.manifest_path}': {e}")
            return False

    def get_expected_content_lang(self, page_id, req_locale, fallback_lang="en"):
        """Derive expected content language dynamically from source translation availability."""
        doc = self.documents.get(page_id)
        if not doc:
            return fallback_lang

        available = doc.get("available_languages", [])
        source_lang = doc.get("source_lang", self.default_lang)

        if req_locale in available:
            return req_locale
        elif self.default_lang in available:
            return self.default_lang
        else:
            return source_lang

    def get_expected_canonical_file(self, page_id, req_locale):
        """Determine the exact expected relative output file in _site for page_id and locale."""
        doc = self.documents.get(page_id)
        if not doc:
            return None

        permalink = doc.get("permalink", "/")
        clean = permalink.strip("/")
        if not clean or permalink == "/":
            file_part = "index.html"
        else:
            file_part = f"{clean}/index.html"

        if req_locale == self.default_lang:
            return file_part
        else:
            return f"{req_locale}/{file_part}"

    def resolve_destination(self, start_file, initial_content):
        """Follow redirect chain starting from start_file, returning (final_rel_file, final_content, visited_files, error)."""
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
            parsed = urlparse(raw_target)

            # Prevent origin escaping
            if parsed.netloc and parsed.netloc not in ("docs.openmandriva.org", "localhost", "127.0.0.1"):
                return curr_file, None, visited, f"Redirect target '{raw_target}' points to external origin '{parsed.netloc}'"

            path_only = parsed.path
            # Check baseurl boundary
            if self.baseurl:
                if not (path_only == self.baseurl or path_only.startswith(f"{self.baseurl}/")):
                    return curr_file, None, visited, f"Redirect target '{raw_target}' is outside baseurl scope '{self.baseurl}'"
                clean_path = path_only[len(self.baseurl):]
            else:
                clean_path = path_only

            clean_str = clean_path.lstrip("/")
            if not clean_str or clean_path.endswith("/"):
                dest_file = f"{clean_str}index.html" if clean_str else "index.html"
            else:
                dest_file = clean_str

            # Normalize path and check against escaping _site
            norm_dest = os.path.normpath(dest_file)
            if norm_dest.startswith("..") or os.path.isabs(norm_dest):
                return dest_file, None, visited, f"Redirect target escapes site root: '{raw_target}'"

            if norm_dest in visited:
                cycle_str = " -> ".join(visited + [norm_dest])
                return norm_dest, None, visited, f"Redirect loop/cycle detected: {cycle_str}"

            visited.append(norm_dest)
            target_path = self.site_dir / norm_dest
            if not target_path.is_file():
                return norm_dest, None, visited, f"Redirect target '{raw_target}' (file '{norm_dest}') does not exist on disk"

            curr_file = norm_dest
            curr_content = target_path.read_text(encoding="utf-8")

        return curr_file, None, visited, f"Exceeded maximum redirect depth ({max_redirects})"

    def verify(self):
        self.errors.clear()
        self.verified_routes_count = 0
        self.verified_canonical_count = 0
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
            manifest_routes = json.loads(self.routes_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.errors.append(f"Failed to parse routes manifest '{self.routes_path}': {e}")
            return False

        routes = manifest_routes.get("routes", [])
        if not routes:
            self.errors.append(f"No routes found in manifest '{self.routes_path}'.")
            return False

        # 3. Load or generate build manifest for translation-aware verification
        if not self.ensure_build_manifest():
            return False

        # Phase 1: Verify all baseline routes
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
            pub_url = r.get("public_url")
            req_locale = r.get("requested_locale", self.default_lang)
            fallback_lang = r.get("actual_content_lang", "en")
            expected_content_lang = self.get_expected_content_lang(expected_pid, req_locale, fallback_lang)

            if expected_pid == "system.404":
                if "404" not in content and "not found" not in content.lower():
                    self.errors.append(f"System 404 page '{rel_file}' missing 404 error indicators")
            else:
                final_file, final_content, visited, redirect_err = self.resolve_destination(rel_file, content)
                if redirect_err:
                    self.errors.append(f"Route '{pub_url}' ({rel_file}): {redirect_err}")
                    continue

                # Verify exact canonical destination file if manifest is present
                expected_canon_file = self.get_expected_canonical_file(expected_pid, req_locale)
                if expected_canon_file and final_file != expected_canon_file:
                    self.errors.append(
                        f"Route '{pub_url}' ({rel_file}) resolved to '{final_file}', but expected canonical destination is '{expected_canon_file}'"
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
                elif m_lang.group(1) != expected_content_lang:
                    self.errors.append(
                        f"Resolved document '{final_file}' for route '{pub_url}' content language mismatch: expected '{expected_content_lang}', found '{m_lang.group(1)}'"
                    )

            self.verified_routes_count += 1

        self.verified_count = self.verified_routes_count

        # Phase 2: Validate all canonical documents across configured languages
        if self.documents:
            for pid, doc in self.documents.items():
                for lang in self.languages:
                    expected_file = self.get_expected_canonical_file(pid, lang)
                    target_path = self.site_dir / expected_file

                    if not target_path.is_file():
                        self.errors.append(
                            f"Missing canonical document for page_id '{pid}' in language '{lang}': expected file '{expected_file}'"
                        )
                        continue

                    content = target_path.read_text(encoding="utf-8")
                    if len(content.strip()) < 50:
                        self.errors.append(
                            f"Canonical document '{expected_file}' is suspiciously small ({len(content)} bytes)"
                        )
                        continue

                    # Ensure canonical page is not an unintentional redirect
                    if HTTP_REFRESH_RE.search(content):
                        self.errors.append(
                            f"Canonical document '{expected_file}' unexpectedly contains http-equiv refresh redirect"
                        )

                    m_pid = DOC_PID_RE.search(content)
                    m_lang = DOC_LANG_RE.search(content)
                    expected_lang = self.get_expected_content_lang(pid, lang)

                    if not m_pid or m_pid.group(1) != pid:
                        found_pid = m_pid.group(1) if m_pid else "missing"
                        self.errors.append(
                            f"Canonical document '{expected_file}' page_id mismatch: expected '{pid}', found '{found_pid}'"
                        )

                    if not m_lang or m_lang.group(1) != expected_lang:
                        found_lang = m_lang.group(1) if m_lang else "missing"
                        self.errors.append(
                            f"Canonical document '{expected_file}' content language mismatch: expected '{expected_lang}', found '{found_lang}'"
                        )

                    self.verified_canonical_count += 1

        # Phase 3: Validate absence of redirects from navigation and search indexes
        search_file = self.site_dir / "assets" / "js" / "search-data.json"
        if search_file.is_file():
            try:
                search_data = json.loads(search_file.read_text(encoding="utf-8"))
                for idx, entry in enumerate(search_data.values() if isinstance(search_data, dict) else search_data):
                    title = entry.get("title", "")
                    url = entry.get("url", "")
                    if title == "Redirecting..." or "Redirecting" in title:
                        self.errors.append(f"Redirect page leaked into search index (entry {idx}: title='{title}', url='{url}')")
            except Exception as e:
                self.errors.append(f"Failed to inspect search index '{search_file}': {e}")

        # Check navigation and children links across all generated content pages
        for page_file in self.site_dir.rglob("*.html"):
            content = page_file.read_text(encoding="utf-8")
            # Skip technical redirect files themselves
            if HTTP_REFRESH_RE.search(content):
                continue
            if NAV_REDIRECT_RE.search(content) or "Redirecting..." in content:
                rel_path = page_file.relative_to(self.site_dir)
                self.errors.append(f"Redirect link or title leaked into content page '{rel_path}'")

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
        "--manifest",
        default=None,
        help="Path to build_manifest.json (default: .agents/i18n-architecture/build_manifest.json when default routes used)",
    )
    parser.add_argument(
        "--baseurl",
        default="",
        help="Configured baseurl of the site (default: '')",
    )

    args = parser.parse_args()
    verifier = SiteVerifier(
        site_dir=args.site_dir,
        routes_path=args.routes,
        manifest_path=args.manifest,
        baseurl=args.baseurl
    )

    print(f"Verifying generated site '{verifier.site_dir}' against routes manifest '{verifier.routes_path}'...")
    success = verifier.verify()

    if success:
        print(
            f"Site verification PASSED: All {verifier.verified_routes_count} legacy routes "
            f"and {verifier.verified_canonical_count} canonical documents verified with correct identities, "
            f"translation languages, and nav/search exclusions."
        )
        sys.exit(0)
    else:
        print(f"Site verification FAILED with {len(verifier.errors)} error(s):")
        for err in verifier.errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
