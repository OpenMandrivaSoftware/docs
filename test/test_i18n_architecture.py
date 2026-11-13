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


if __name__ == "__main__":
    unittest.main()
