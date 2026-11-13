#!/usr/bin/env python3
"""
Reproducible integration test for i18n architecture proof.
Validates Jekyll + Polyglot 1.14.0 behavior with languages ['en', 'fr', 'de', 'ru'].
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
import json

from verify_generated_site import SiteVerifier

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURE_DIR = os.path.join(REPO_ROOT, "test", "fixtures", "i18n_architecture")


class TestI18nArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dest = tempfile.mkdtemp(prefix="om_i18n_arch_site_")
        env = os.environ.copy()
        env["BUNDLE_GEMFILE"] = os.path.join(REPO_ROOT, "Gemfile")
        cmd = [
            "bundle", "exec", "jekyll", "build",
            "--source", FIXTURE_DIR,
            "--destination", cls.temp_dest,
            "--trace"
        ]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
        if res.returncode != 0:
            raise RuntimeError(f"Jekyll build of fixture failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dest, ignore_errors=True)

    def read_meta(self, rel_path):
        full_path = os.path.join(self.temp_dest, rel_path)
        self.assertTrue(os.path.isfile(full_path), f"File {rel_path} was not generated in {self.temp_dest}")
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        metas = dict(re.findall(r'<meta name="([^"]+)" content="([^"]*)"', content))
        title_m = re.search(r"<title>(.*?)</title>", content)
        metas["title"] = title_m.group(1) if title_m else ""
        return metas

    def test_localized_homepages(self):
        """Scenario 7: Homepage cleanly localized on root routes without query/redirect hacks."""
        en = self.read_meta("index.html")
        self.assertEqual(en["title"], "Home EN")
        self.assertEqual(en["rendered_lang"], "en")

        fr = self.read_meta("fr/index.html")
        self.assertEqual(fr["title"], "Accueil FR")
        self.assertEqual(fr["rendered_lang"], "fr")

        de = self.read_meta("de/index.html")
        self.assertEqual(de["title"], "Startseite DE")
        self.assertEqual(de["rendered_lang"], "de")

        ru = self.read_meta("ru/index.html")
        self.assertEqual(ru["title"], "Главная RU")
        self.assertEqual(ru["rendered_lang"], "ru")

    def test_english_original_with_translations(self):
        """Scenario 1: EN original with FR and DE translations, RU fallback to EN."""
        en = self.read_meta("articles/installation/index.html")
        self.assertEqual(en["title"], "Installation Guide EN")
        self.assertEqual(en["rendered_lang"], "en")

        fr = self.read_meta("fr/articles/installation/index.html")
        self.assertEqual(fr["title"], "Guide d'installation FR")
        self.assertEqual(fr["rendered_lang"], "fr")

        de = self.read_meta("de/articles/installation/index.html")
        self.assertEqual(de["title"], "Installationsanleitung DE")
        self.assertEqual(de["rendered_lang"], "de")

        ru = self.read_meta("ru/articles/installation/index.html")
        self.assertEqual(ru["title"], "Installation Guide EN")
        self.assertEqual(ru["rendered_lang"], "en")

    def test_english_only_article(self):
        """Scenario 2: English-only article rendered across all language trees in English."""
        for path, loc in [
            ("articles/kernel/index.html", "en"),
            ("fr/articles/kernel/index.html", "fr"),
            ("de/articles/kernel/index.html", "de"),
            ("ru/articles/kernel/index.html", "ru"),
        ]:
            meta = self.read_meta(path)
            self.assertEqual(meta["title"], "Kernel Tuning EN")
            self.assertEqual(meta["rendered_lang"], "en")
            self.assertEqual(meta["active_lang"], loc)

    def test_french_original_with_english_translation(self):
        """Scenario 3: French original with English translation; DE/RU fall back to EN."""
        fr = self.read_meta("fr/articles/cooker/index.html")
        self.assertEqual(fr["title"], "Dépôt Cooker FR")
        self.assertEqual(fr["rendered_lang"], "fr")
        self.assertEqual(fr["source_lang"], "fr")

        en = self.read_meta("articles/cooker/index.html")
        self.assertEqual(en["title"], "Cooker Repository EN")
        self.assertEqual(en["rendered_lang"], "en")

        de = self.read_meta("de/articles/cooker/index.html")
        self.assertEqual(de["title"], "Cooker Repository EN")
        self.assertEqual(de["rendered_lang"], "en")

    def test_french_original_without_english_fallback(self):
        """Scenario 4: French original with German translation, no English; RU falls back to FR original."""
        fr = self.read_meta("fr/articles/packaging-spec/index.html")
        self.assertEqual(fr["title"], "Spécification RPM FR")
        self.assertEqual(fr["rendered_lang"], "fr")

        de = self.read_meta("de/articles/packaging-spec/index.html")
        self.assertEqual(de["title"], "RPM Spezifikation DE")
        self.assertEqual(de["rendered_lang"], "de")

        # Crucial check: RU subsite must fall back to source_lang (fr), NOT de translation
        ru = self.read_meta("ru/articles/packaging-spec/index.html")
        self.assertEqual(ru["title"], "Spécification RPM FR")
        self.assertEqual(ru["rendered_lang"], "fr")

    def test_french_only_article(self):
        """Scenario 5: French-only article rendered as French across all language trees."""
        for path in [
            "articles/association-statutes/index.html",
            "fr/articles/association-statutes/index.html",
            "de/articles/association-statutes/index.html",
            "ru/articles/association-statutes/index.html",
        ]:
            meta = self.read_meta(path)
            self.assertEqual(meta["title"], "Statuts de l'Association FR")
            self.assertEqual(meta["rendered_lang"], "fr")

    def test_nested_hierarchy_mixed_translations(self):
        """Scenario 6: Nested hierarchy with mixed translation availability and parent_id preservation."""
        # Check Steam (FR only) in RU subsite:
        steam_ru = self.read_meta("ru/user-guide/steam/index.html")
        self.assertEqual(steam_ru["title"], "Installer Steam FR")
        self.assertEqual(steam_ru["parent_id"], "user-guide")
        self.assertEqual(steam_ru["rendered_lang"], "fr")
        # Approach A verification: parent resolved to active/fallback parent title in RU!
        self.assertEqual(steam_ru["resolved_parent"], "User Guide EN")

        # Check DNF (EN, FR, RU) in DE subsite (fallback to EN):
        dnf_de = self.read_meta("de/user-guide/dnf/index.html")
        self.assertEqual(dnf_de["title"], "Using DNF EN")
        self.assertEqual(dnf_de["parent_id"], "user-guide")
        self.assertEqual(dnf_de["rendered_lang"], "en")
        self.assertEqual(dnf_de["resolved_parent"], "User Guide EN")

        # Check DNF in FR subsite:
        dnf_fr = self.read_meta("fr/user-guide/dnf/index.html")
        self.assertEqual(dnf_fr["title"], "Utilisation de DNF FR")
        self.assertEqual(dnf_fr["resolved_parent"], "Guide de l'utilisateur FR")

    def test_shared_assets_not_duplicated(self):
        """Scenario 8: Assets in exclude_from_localization are only at site root."""
        root_asset = os.path.join(self.temp_dest, "assets", "images", "shared-logo.png")
        self.assertTrue(os.path.isfile(root_asset))

        # Must not be copied into localized subsites
        for loc in ["fr", "de", "ru"]:
            loc_asset = os.path.join(self.temp_dest, loc, "assets", "images", "shared-logo.png")
            self.assertFalse(os.path.exists(loc_asset), f"Asset was duplicated into {loc_asset}")

    def test_nonempty_baseurl_build(self):
        """Scenario 9: Non-empty baseurl compiles cleanly with Polyglot."""
        temp_dest = tempfile.mkdtemp(prefix="om_i18n_baseurl_site_")
        try:
            env = os.environ.copy()
            env["BUNDLE_GEMFILE"] = os.path.join(REPO_ROOT, "Gemfile")
            cmd = [
                "bundle", "exec", "jekyll", "build",
                "--source", FIXTURE_DIR,
                "--destination", temp_dest,
                "--baseurl", "/docs"
            ]
            res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(res.returncode, 0, f"Build with baseurl failed:\n{res.stderr}")
            # Verify root and localized index generated
            self.assertTrue(os.path.isfile(os.path.join(temp_dest, "index.html")))
            self.assertTrue(os.path.isfile(os.path.join(temp_dest, "fr", "index.html")))
        finally:
            shutil.rmtree(temp_dest, ignore_errors=True)

    def test_document_order_determinism(self):
        """Explicitly proves that fallback order is deterministic with the adapter."""
        # Create a test setup with two files where French is authoring source_lang
        temp_src = tempfile.mkdtemp(prefix="om_order_test_src_")
        temp_dest = tempfile.mkdtemp(prefix="om_order_test_dest_")
        try:
            shutil.copy(os.path.join(FIXTURE_DIR, "_config.yml"), temp_src)
            shutil.copytree(os.path.join(FIXTURE_DIR, "_layouts"), os.path.join(temp_src, "_layouts"))
            shutil.copytree(os.path.join(FIXTURE_DIR, "_plugins"), os.path.join(temp_src, "_plugins"))

            with open(os.path.join(temp_src, "index.en.md"), "w") as f:
                f.write("---\nlayout: default\npage_id: home\npermalink: /\ntitle: Home\n---\nHome")

            # Permutation 1: German named 'a_doc.de.md', French named 'z_doc.fr.md'
            os.makedirs(os.path.join(temp_src, "page"), exist_ok=True)
            with open(os.path.join(temp_src, "page", "a_doc.de.md"), "w") as f:
                f.write("---\nlayout: default\npage_id: test.page\nlang: de\nsource_lang: fr\ntitle: Title DE\npermalink: /page/\n---\nDE")
            with open(os.path.join(temp_src, "page", "z_doc.fr.md"), "w") as f:
                f.write("---\nlayout: default\npage_id: test.page\nlang: fr\nsource_lang: fr\ntitle: Title FR\npermalink: /page/\n---\nFR")

            env = os.environ.copy()
            env["BUNDLE_GEMFILE"] = os.path.join(REPO_ROOT, "Gemfile")
            cmd = ["bundle", "exec", "jekyll", "build", "--source", temp_src, "--destination", temp_dest]
            res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(res.returncode, 0)

            # In Russian subsite, must fall back to source_lang (Title FR)
            with open(os.path.join(temp_dest, "ru", "page", "index.html"), "r") as f:
                content = f.read()
            self.assertIn("Title FR", content)

            # Permutation 2: Swap names so French is 'a_doc.fr.md' and German is 'z_doc.de.md'
            os.remove(os.path.join(temp_src, "page", "a_doc.de.md"))
            os.remove(os.path.join(temp_src, "page", "z_doc.fr.md"))
            with open(os.path.join(temp_src, "page", "a_doc.fr.md"), "w") as f:
                f.write("---\nlayout: default\npage_id: test.page\nlang: fr\nsource_lang: fr\ntitle: Title FR\npermalink: /page/\n---\nFR")
            with open(os.path.join(temp_src, "page", "z_doc.de.md"), "w") as f:
                f.write("---\nlayout: default\npage_id: test.page\nlang: de\nsource_lang: fr\ntitle: Title DE\npermalink: /page/\n---\nDE")

            shutil.rmtree(temp_dest)
            os.makedirs(temp_dest, exist_ok=True)
            res2 = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(res2.returncode, 0)

            # In Russian subsite, must STILL fall back to source_lang (Title FR)
            with open(os.path.join(temp_dest, "ru", "page", "index.html"), "r") as f:
                content2 = f.read()
            self.assertIn("Title FR", content2)
        finally:
            shutil.rmtree(temp_src, ignore_errors=True)
            shutil.rmtree(temp_dest, ignore_errors=True)

    def test_translation_lifecycle_and_historical_redirect_stability(self):
        """
        Scenario 8: Decisive regression fixture for multilingual routing lifecycle.
        A. Build English-only article with historical French fallback URL.
        B. Add a genuine French translation without redirect metadata.
        C. Rebuild.
        D. Confirm:
           - Historical French URL still exists;
           - Resolves to the same logical document;
           - Canonical French article now contains French;
           - SiteVerifier accepts the improved translation;
           - 3rd (de) and 4th (ru) locales remain stable fallbacks.
        """
        temp_src = tempfile.mkdtemp(prefix="om_lifecycle_src_")
        temp_dest = tempfile.mkdtemp(prefix="om_lifecycle_dest_")
        try:
            # Copy base fixture
            for item in os.listdir(FIXTURE_DIR):
                s = os.path.join(FIXTURE_DIR, item)
                d = os.path.join(temp_src, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            # Ensure articles/kernel only has English original
            kernel_dir = os.path.join(temp_src, "articles", "kernel")
            for f in os.listdir(kernel_dir):
                if f != "index.en.md":
                    os.remove(os.path.join(kernel_dir, f))

            routes_manifest = os.path.join(temp_src, ".agents", "i18n-architecture", "legacy_routes.json")
            os.makedirs(os.path.dirname(routes_manifest), exist_ok=True)
            with open(routes_manifest, "w", encoding="utf-8") as f:
                json.dump({
                    "total_generated_routes": 2,
                    "routes": [
                        {
                            "public_url": "/articles/kernel.en.html",
                            "file_in_site": "articles/kernel.en.html",
                            "requested_locale": "en",
                            "actual_content_lang": "en",
                            "page_id": "articles.kernel",
                            "canonical_destination": "/articles/kernel/"
                        },
                        {
                            "public_url": "/fr/articles/kernel.en.html",
                            "file_in_site": "fr/articles/kernel.en.html",
                            "requested_locale": "fr",
                            "actual_content_lang": "en",
                            "page_id": "articles.kernel",
                            "canonical_destination": "/fr/articles/kernel/"
                        }
                    ]
                }, f)

            # Initial build manifest (English only)
            build_manifest_path = os.path.join(temp_src, ".agents", "i18n-architecture", "build_manifest.json")
            with open(build_manifest_path, "w", encoding="utf-8") as f:
                json.dump({
                    "languages": ["en", "fr", "de", "ru"],
                    "default_lang": "en",
                    "documents": {
                        "articles.kernel": {
                            "page_id": "articles.kernel",
                            "permalink": "/articles/kernel/",
                            "source_lang": "en",
                            "available_languages": ["en"]
                        }
                    }
                }, f)

            env = os.environ.copy()
            env["BUNDLE_GEMFILE"] = os.path.join(REPO_ROOT, "Gemfile")
            cmd = ["bundle", "exec", "jekyll", "build", "--source", temp_src, "--destination", temp_dest]

            # Step A: Build English-only article
            res_a = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(res_a.returncode, 0, f"Jekyll build failed:\n{res_a.stderr}")

            # Verify historical French fallback URL exists and redirects to canonical French article
            fr_hist_url = os.path.join(temp_dest, "fr", "articles", "kernel.en.html")
            self.assertTrue(os.path.isfile(fr_hist_url))
            with open(fr_hist_url, "r", encoding="utf-8") as f:
                hist_html = f.read()
            self.assertIn('url=/fr/articles/kernel/', hist_html)
            self.assertIn('<meta name="robots" content="noindex">', hist_html)

            # Verify French article currently renders English fallback
            fr_canon_file = os.path.join(temp_dest, "fr", "articles", "kernel", "index.html")
            self.assertTrue(os.path.isfile(fr_canon_file))
            with open(fr_canon_file, "r", encoding="utf-8") as f:
                canon_html_en = f.read()
            self.assertIn("Kernel Tuning EN", canon_html_en)

            # Verify with SiteVerifier: accepts English fallback
            verifier_a = SiteVerifier(
                site_dir=temp_dest,
                routes_path=routes_manifest,
                manifest_path=build_manifest_path
            )
            self.assertTrue(verifier_a.verify(), f"Verifier failed at Step A: {verifier_a.errors}")

            # Step B: Add genuine French translation (WITHOUT redirect metadata)
            fr_source_file = os.path.join(kernel_dir, "index.fr.md")
            with open(fr_source_file, "w", encoding="utf-8") as f:
                f.write(
                    "---\n"
                    "layout: default\n"
                    "page_id: articles.kernel\n"
                    "lang: fr\n"
                    "source_lang: en\n"
                    "permalink: /articles/kernel/\n"
                    "title: Optimisation du Noyau FR\n"
                    "---\n"
                    "Paramètres avancés d'optimisation du noyau Linux.\n"
                )

            # Update build manifest to reflect newly available French translation
            with open(build_manifest_path, "w", encoding="utf-8") as f:
                json.dump({
                    "languages": ["en", "fr", "de", "ru"],
                    "default_lang": "en",
                    "documents": {
                        "articles.kernel": {
                            "page_id": "articles.kernel",
                            "permalink": "/articles/kernel/",
                            "source_lang": "en",
                            "available_languages": ["en", "fr"]
                        }
                    }
                }, f)

            # Step C: Rebuild
            shutil.rmtree(temp_dest)
            os.makedirs(temp_dest, exist_ok=True)
            res_c = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(res_c.returncode, 0, f"Jekyll rebuild failed:\n{res_c.stderr}")

            # Step D: Confirm
            # 1. Historical French URL STILL exists and redirects to canonical French permalink
            self.assertTrue(os.path.isfile(fr_hist_url))
            with open(fr_hist_url, "r", encoding="utf-8") as f:
                hist_html2 = f.read()
            self.assertIn('url=/fr/articles/kernel/', hist_html2)

            # 2. Canonical French article now contains genuine French
            with open(fr_canon_file, "r", encoding="utf-8") as f:
                canon_html_fr = f.read()
            self.assertIn("Optimisation du Noyau FR", canon_html_fr)
            self.assertIn('<meta name="rendered_lang" content="fr">', canon_html_fr)

            # 3. Verifier accepts the improved translation without extra redirect metadata
            verifier_c = SiteVerifier(
                site_dir=temp_dest,
                routes_path=routes_manifest,
                manifest_path=build_manifest_path
            )
            self.assertTrue(verifier_c.verify(), f"Verifier failed at Step D: {verifier_c.errors}")

            # 4. Confirm 3rd (de) and 4th (ru) locales remain clean fallbacks without routing errors
            de_file = os.path.join(temp_dest, "de", "articles", "kernel", "index.html")
            ru_file = os.path.join(temp_dest, "ru", "articles", "kernel", "index.html")
            self.assertTrue(os.path.isfile(de_file))
            self.assertTrue(os.path.isfile(ru_file))
            with open(de_file, "r", encoding="utf-8") as f:
                self.assertIn("Kernel Tuning EN", f.read())
            with open(ru_file, "r", encoding="utf-8") as f:
                self.assertIn("Kernel Tuning EN", f.read())

        finally:
            shutil.rmtree(temp_src, ignore_errors=True)
            shutil.rmtree(temp_dest, ignore_errors=True)

    def test_absence_of_redirects_in_production_navigation_and_search(self):
        """Verifies that redirect entries are absent from Just the Docs navigation and search output."""
        site_dir = os.path.join(REPO_ROOT, "_site")
        if not os.path.isdir(site_dir):
            self.skipTest("_site directory not built yet")

        # 1. Search index check
        search_file = os.path.join(site_dir, "assets", "js", "search-data.json")
        if os.path.isfile(search_file):
            with open(search_file, "r", encoding="utf-8") as f:
                search_data = json.load(f)
            entries = search_data.values() if isinstance(search_data, dict) else search_data
            for entry in entries:
                title = entry.get("title", "")
                self.assertNotEqual(title, "Redirecting...", "Redirect leaked into search index")
                self.assertNotIn("Redirecting", title, "Redirect title leaked into search index")

        # 2. Navigation sidebar and children check across ALL content pages
        checked_pages = 0
        for root, dirs, files in os.walk(site_dir):
            for file in files:
                if not file.endswith(".html"):
                    continue
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    html = f.read()
                # Skip technical redirect pages
                if '<meta http-equiv="refresh"' in html:
                    continue
                rel_p = os.path.relpath(full_path, site_dir)
                self.assertNotIn('Redirecting...', html, f"Redirect link or title leaked into content page {rel_p}")
                checked_pages += 1
        self.assertGreater(checked_pages, 80, "Expected at least 80 content pages checked for navigation purity")


if __name__ == "__main__":
    unittest.main()
