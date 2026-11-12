#!/usr/bin/env python3
"""
Unit and regression tests for SiteVerifier (test/verify_generated_site.py).
Tests detection of missing directory, missing routes, identity mismatches,
and content language mismatches.
"""

import json
import tempfile
import unittest
from pathlib import Path

from verify_generated_site import SiteVerifier


class TestSiteVerifier(unittest.TestCase):
    def test_missing_site_directory_fails(self):
        verifier = SiteVerifier(site_dir="/nonexistent/site/dir")
        success = verifier.verify()
        self.assertFalse(success)
        self.assertTrue(any("does not exist" in e for e in verifier.errors))

    def test_missing_routes_manifest_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            site_dir = Path(tmp) / "_site"
            site_dir.mkdir()
            verifier = SiteVerifier(site_dir=site_dir, routes_path="/nonexistent/routes.json")
            success = verifier.verify()
            self.assertFalse(success)
            self.assertTrue(any("does not exist" in e for e in verifier.errors))

    def test_missing_route_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "_site"
            site_dir.mkdir()
            routes_file = tmp_path / "routes.json"
            routes_file.write_text(json.dumps({
                "routes": [
                    {
                        "file_in_site": "missing.html",
                        "public_url": "/missing.html",
                        "page_id": "test.missing",
                        "actual_content_lang": "en"
                    }
                ]
            }), encoding="utf-8")

            verifier = SiteVerifier(site_dir=site_dir, routes_path=routes_file)
            success = verifier.verify()
            self.assertFalse(success)
            self.assertTrue(any("Missing generated file" in e for e in verifier.errors))

    def test_mismatched_page_id_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "_site"
            site_dir.mkdir()

            doc_file = site_dir / "article.html"
            doc_file.write_text(
                '<!DOCTYPE html><html><head>'
                '<meta name="doc-page-id" content="wrong.id">'
                '<meta name="doc-content-lang" content="en">'
                '</head><body>Content longer than fifty bytes for testing purposes</body></html>',
                encoding="utf-8"
            )

            routes_file = tmp_path / "routes.json"
            routes_file.write_text(json.dumps({
                "routes": [
                    {
                        "file_in_site": "article.html",
                        "public_url": "/article.html",
                        "page_id": "expected.id",
                        "actual_content_lang": "en"
                    }
                ]
            }), encoding="utf-8")

            verifier = SiteVerifier(site_dir=site_dir, routes_path=routes_file)
            success = verifier.verify()
            self.assertFalse(success)
            self.assertTrue(any("page_id mismatch" in e for e in verifier.errors))

    def test_mismatched_content_lang_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "_site"
            site_dir.mkdir()

            doc_file = site_dir / "article.html"
            doc_file.write_text(
                '<!DOCTYPE html><html><head>'
                '<meta name="doc-page-id" content="my.article">'
                '<meta name="doc-content-lang" content="fr">'
                '</head><body>Content longer than fifty bytes for testing purposes</body></html>',
                encoding="utf-8"
            )

            routes_file = tmp_path / "routes.json"
            routes_file.write_text(json.dumps({
                "routes": [
                    {
                        "file_in_site": "article.html",
                        "public_url": "/article.html",
                        "page_id": "my.article",
                        "actual_content_lang": "en" # Expected en, but page has fr
                    }
                ]
            }), encoding="utf-8")

            verifier = SiteVerifier(site_dir=site_dir, routes_path=routes_file)
            success = verifier.verify()
            self.assertFalse(success)
            self.assertTrue(any("content language mismatch" in e for e in verifier.errors))

    def test_valid_site_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            site_dir = tmp_path / "_site"
            site_dir.mkdir()

            # 404 page
            (site_dir / "404.html").write_text(
                "<!DOCTYPE html><html><body><h1>404 Not Found</h1><p>Sorry</p></body></html>",
                encoding="utf-8"
            )
            # Root redirect
            (site_dir / "index.html").write_text(
                '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/index.en.html" /></head></html>',
                encoding="utf-8"
            )
            # Document
            (site_dir / "doc.html").write_text(
                '<!DOCTYPE html><html><head>'
                '<meta name="doc-page-id" content="sample.doc">'
                '<meta name="doc-content-lang" content="en">'
                '</head><body>Valid document body exceeding fifty bytes length requirement</body></html>',
                encoding="utf-8"
            )

            routes_file = tmp_path / "routes.json"
            routes_file.write_text(json.dumps({
                "routes": [
                    {
                        "file_in_site": "404.html",
                        "public_url": "/404.html",
                        "page_id": "system.404",
                        "actual_content_lang": "en"
                    },
                    {
                        "file_in_site": "index.html",
                        "public_url": "/index.html",
                        "page_id": "home",
                        "actual_content_lang": "en"
                    },
                    {
                        "file_in_site": "doc.html",
                        "public_url": "/doc.html",
                        "page_id": "sample.doc",
                        "actual_content_lang": "en"
                    }
                ]
            }), encoding="utf-8")

            verifier = SiteVerifier(site_dir=site_dir, routes_path=routes_file)
            success = verifier.verify()
            self.assertTrue(success, f"Expected success but got errors: {verifier.errors}")
            self.assertEqual(verifier.verified_count, 3)


if __name__ == "__main__":
    unittest.main()
