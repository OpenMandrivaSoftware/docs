#!/usr/bin/env python3
"""
Unit tests for test/check_links.py link and asset validator.
"""

import os
import shutil
import tempfile
import unittest

from test.check_links import LinkChecker, main


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

    def test_baseurl_handling(self):
        """Links with configured baseurl must be properly stripped and resolved."""
        self.write_file("sub/page.html", "<html><body id='sub-page'>Target</body></html>")
        self.write_file("index.html", """
            <html>
            <body>
                <a href="/mybase/sub/page.html#sub-page">Baseurl link</a>
            </body>
            </html>
        """)

        checker = LinkChecker(site_dir=self.test_dir, site_url=self.site_url, baseurl="/mybase")
        checker.scan()
        result = checker.validate()

        self.assertTrue(result, f"Expected baseurl link to resolve, but got: {checker.errors}")
        self.assertEqual(len(checker.errors), 0)

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
