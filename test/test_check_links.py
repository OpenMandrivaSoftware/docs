#!/usr/bin/env python3
"""
Unit tests for test/check_links.py link and asset validator.
"""

import os
import shutil
import sys
import tempfile
import unittest

# Ensure this directory is on sys.path to avoid collision with standard library 'test' package
_test_dir = os.path.dirname(os.path.abspath(__file__))
if _test_dir not in sys.path:
    sys.path.insert(0, _test_dir)

from check_links import LinkChecker, main


class TestLinkChecker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="om_link_test_")
        self.site_url = "https://docs.openmandriva.org"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def write_file(self, rel_path, content, binary=False):
        full_path = os.path.join(self.test_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        mode = "wb" if binary else "w"
        encoding = None if binary else "utf-8"
        with open(full_path, mode, encoding=encoding) as f:
            f.write(content)
        return full_path

    def test_valid_references(self):
        """Valid relative, absolute, same-origin, encoded, and anchor links must pass."""
        self.write_file("assets/image.png", b"\x89PNG\r\n\x1a\n", binary=True)
        self.write_file("js/app.js", "console.log('ok');")
        self.write_file("path with spaces.html", "<html><body id='spaced'>Spaced</body></html>")
        self.write_file("sub/index.html", "<html><body id='sub-root'>Sub</body></html>")
        self.write_file("other.html", """
            <!DOCTYPE html>
            <html>
            <head><title>Other</title></head>
            <body>
                <h1 id="other-header">Header</h1>
                <a name="legacy-anchor">Target</a>
            </body>
            </html>
        """)

        index_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="/assets/image.png">
                <script src="/js/app.js"></script>
            </head>
            <body>
                <div id="self-anchor">Self</div>
                <a href="#self-anchor">Local anchor</a>
                <a href="./other.html#other-header">Other page header</a>
                <a href="/other.html#legacy-anchor">Other legacy anchor</a>
                <a href="{self.site_url}/other.html">Same-origin link</a>
                <a href="./sub/">Directory link</a>
                <a href="./path%20with%20spaces.html#spaced">Encoded path</a>
                <a href="./other.html?query=param&test=1#other-header">Query params</a>
                <a href="mailto:test@openmandriva.org">Mailto</a>
                <a href="https://external.example.com/page">External</a>
                <img src="./assets/image.png" alt="Test image">
            </body>
            </html>
        """
        self.write_file("index.html", index_html)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        result = checker.validate()

        self.assertTrue(result, f"Expected validation to succeed, but found errors: {checker.errors}")
        self.assertEqual(len(checker.errors), 0)

    def test_missing_file_detected(self):
        """A link targeting a non-existent file must be caught."""
        self.write_file("index.html", """
            <html>
            <body>
                <a href="./nonexistent.html">Broken link</a>
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        result = checker.validate()

        self.assertFalse(result)
        self.assertEqual(len(checker.errors), 1)
        self.assertIn("Target file does not exist", checker.errors[0]["reason"])
        self.assertEqual(checker.errors[0]["link"], "./nonexistent.html")

    def test_missing_anchor_detected(self):
        """Both local and cross-page missing anchor fragments must be caught."""
        self.write_file("target.html", """
            <html>
            <body>
                <h2 id="existing-heading">Heading</h2>
            </body>
            </html>
        """)
        self.write_file("index.html", """
            <html>
            <body>
                <div id="local-heading">Local</div>
                <a href="#missing-local-heading">Broken local anchor</a>
                <a href="./target.html#missing-target-heading">Broken cross anchor</a>
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        result = checker.validate()

        self.assertFalse(result)
        self.assertEqual(len(checker.errors), 2)
        reasons = [e["reason"] for e in checker.errors]
        self.assertTrue(any("missing-local-heading" in r for r in reasons))
        self.assertTrue(any("missing-target-heading" in r for r in reasons))

    def test_missing_image_detected(self):
        """Missing images referenced in <img src="..."> must be reported."""
        self.write_file("index.html", """
            <html>
            <body>
                <img src="/assets/nonexistent.png" alt="Missing">
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        result = checker.validate()

        self.assertFalse(result)
        self.assertEqual(len(checker.errors), 1)
        self.assertIn("Target file does not exist", checker.errors[0]["reason"])

    def test_directory_without_index_html(self):
        """A directory missing index.html must be flagged, even if index.en.html is present."""
        self.write_file("folder/index.en.html", "<html><body>English only</body></html>")
        self.write_file("index.html", """
            <html>
            <body>
                <a href="/folder/">Link to directory</a>
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        result = checker.validate()

        self.assertFalse(result)
        self.assertEqual(len(checker.errors), 1)
        self.assertIn("index.html", checker.errors[0]["reason"])

    def test_baseurl_boundary_and_scope(self):
        """Regression test: baseurl /docs must accept /docs/page.html, but reject /docs-old and /assets."""
        self.write_file("page.html", "<html><body id='target'>Target</body></html>")
        self.write_file("assets/image.png", b"\x89PNG\r\n\x1a\n", binary=True)

        # Valid link within baseurl
        self.write_file("index.html", """
            <html>
            <body>
                <a href="/docs/page.html#target">Valid link</a>
            </body>
            </html>
        """)
        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url, baseurl="/docs")
        checker.scan()
        self.assertTrue(checker.validate())

        # Link to /docs-old (prefix match without segment boundary) must be rejected
        self.write_file("index.html", """
            <html>
            <body>
                <a href="/docs-old/page.html">Invalid segment prefix</a>
            </body>
            </html>
        """)
        checker_prefix = LinkChecker(site_dir=self.test_dir, site_url=self.site_url, baseurl="/docs")
        checker_prefix.scan()
        self.assertFalse(checker_prefix.validate())
        self.assertIn("outside baseurl scope", checker_prefix.errors[0]["reason"])

        # Link to /assets/image.png without required baseurl must be rejected
        self.write_file("index.html", """
            <html>
            <body>
                <img src="/assets/image.png" alt="Missing baseurl">
            </body>
            </html>
        """)
        checker_scope = LinkChecker(site_dir=self.test_dir, site_url=self.site_url, baseurl="/docs")
        checker_scope.scan()
        self.assertFalse(checker_scope.validate())
        self.assertIn("outside baseurl scope", checker_scope.errors[0]["reason"])

    def test_relative_link_to_neighbor_document(self):
        """Regression test: relative link to neighboring document must resolve correctly."""
        self.write_file("section/doc1.html", """
            <html>
            <body>
                <a href="./doc2.html#anchor2">Neighbor link</a>
                <a href="doc2.html">Direct neighbor link</a>
            </body>
            </html>
        """)
        self.write_file("section/doc2.html", """
            <html>
            <body id="anchor2">Doc 2</body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        self.assertTrue(checker.validate())

    def test_relative_link_escaping_site_directory(self):
        """Regression test: relative link targeting an existing file outside _site must be rejected."""
        # Create a file outside self.test_dir on disk
        outside_path = os.path.join(os.path.dirname(self.test_dir), "outside_secret.html")
        try:
            with open(outside_path, "w", encoding="utf-8") as f:
                f.write("<html><body>Secret outside site</body></html>")

            # Reference that file via relative traversal from site root
            self.write_file("index.html", """
                <html>
                <body>
                    <a href="../outside_secret.html">Attempt to access outside site</a>
                </body>
                </html>
            """)

            checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
            checker.scan()
            result = checker.validate()

            # Must fail: the validator models the published site, where root is top level
            self.assertFalse(result)
            self.assertEqual(len(checker.errors), 1)
            self.assertTrue(
                "Target file does not exist" in checker.errors[0]["reason"]
                or "outside published site directory" in checker.errors[0]["reason"]
            )
        finally:
            if os.path.exists(outside_path):
                os.remove(outside_path)

    def test_query_string_and_fragment_handling(self):
        """Regression test: query strings and fragments must be parsed without breaking target resolution."""
        self.write_file("target.html", """
            <html>
            <body>
                <h2 id="target-anchor">Target heading</h2>
            </body>
            </html>
        """)
        self.write_file("index.html", """
            <html>
            <body>
                <a href="./target.html?foo=bar&baz=1#target-anchor">Valid query and fragment</a>
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker.scan()
        self.assertTrue(checker.validate())

        # Now test with missing anchor on URL with query parameters
        self.write_file("index.html", """
            <html>
            <body>
                <a href="./target.html?foo=bar#nonexistent-anchor">Invalid anchor with query</a>
            </body>
            </html>
        """)
        checker_bad_anchor = LinkChecker(site_dir=self.test_dir, site_url=self.site_url)
        checker_bad_anchor.scan()
        self.assertFalse(checker_bad_anchor.validate())
        self.assertIn("nonexistent-anchor", checker_bad_anchor.errors[0]["reason"])

    def test_cli_execution(self):
        """CLI main() must return exit code 0 on valid site and 1 on broken site."""
        self.write_file("index.html", "<html><body><a href='#ok'></a><div id='ok'></div></body></html>")
        exit_code = main(["--site-dir", self.test_dir, "--site-url", self.site_url])
        self.assertEqual(exit_code, 0)

        # Break index.html
        self.write_file("index.html", "<html><body><a href='#broken'></a></body></html>")
        exit_code_broken = main(["--site-dir", self.test_dir, "--site-url", self.site_url])
        self.assertEqual(exit_code_broken, 1)


if __name__ == "__main__":
    unittest.main()
