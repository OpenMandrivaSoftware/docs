#!/usr/bin/env python3
"""
Unit and integration tests for OpenMandriva Docs metadata schema.
Validates page_id uniqueness, parent_id integrity, source_lang validity,
and legacy route retention.
"""

import json
import os
import re
import unittest
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

FM_PATTERN = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.DOTALL)


def get_content_documents():
    """Find all markdown documentation files in the repository."""
    docs = []
    excluded_dirs = {".git", ".agents", "test", "_site", "vendor", ".jekyll-cache"}
    excluded_files = {"README.md", "AGENTS.md", "LICENSE.md"}

    for p in REPO_ROOT.rglob("*.md"):
        if any(part in excluded_dirs for part in p.parts):
            continue
        if p.name in excluded_files:
            continue
        rel_path = str(p.relative_to(REPO_ROOT))
        docs.append((rel_path, p))
    return sorted(docs, key=lambda x: x[0])


class TestMetadataSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = get_content_documents()
        cls.parsed_docs = []
        for rel_path, path in cls.docs:
            text = path.read_text(encoding="utf-8")
            m = FM_PATTERN.match(text)
            cls.assertTrue(cls, m is not None, f"Document {rel_path} has no valid YAML frontmatter")
            fm = yaml.safe_load(m.group(1)) or {}
            cls.parsed_docs.append({
                "rel_path": rel_path,
                "path": path,
                "frontmatter": fm,
            })

    def test_document_count(self):
        """Repository must contain exactly 91 document variants (87 English, 4 French)."""
        self.assertEqual(len(self.parsed_docs), 91)
        langs = [d["frontmatter"].get("lang") for d in self.parsed_docs]
        self.assertEqual(langs.count("en"), 87)
        self.assertEqual(langs.count("fr"), 4)

    def test_required_metadata_presence(self):
        """Every documentation file must declare all required schema fields."""
        required_fields = ["page_id", "lang", "source_lang", "title", "permalink", "nav_order"]
        for doc in self.parsed_docs:
            fm = doc["frontmatter"]
            rel_path = doc["rel_path"]
            for field in required_fields:
                self.assertIn(
                    field, fm,
                    f"Document '{rel_path}' is missing required metadata field '{field}'"
                )
                self.assertTrue(
                    fm[field] is not None and str(fm[field]).strip() != "",
                    f"Document '{rel_path}' has empty value for field '{field}'"
                )
            self.assertIsInstance(
                fm["nav_order"], int,
                f"Document '{rel_path}' nav_order must be an integer, got {type(fm['nav_order'])}"
            )
            self.assertTrue(
                fm["permalink"].startswith("/"),
                f"Document '{rel_path}' permalink must start with '/', got '{fm['permalink']}'"
            )

    def test_page_id_uniqueness(self):
        """Each page_id must be unique per language."""
        seen = {}
        for doc in self.parsed_docs:
            fm = doc["frontmatter"]
            key = (fm["page_id"], fm["lang"])
            self.assertNotIn(
                key, seen,
                f"Duplicate page_id '{fm['page_id']}' for language '{fm['lang']}' in '{doc['rel_path']}' (already in '{seen.get(key)}')"
            )
            seen[key] = doc["rel_path"]

    def test_parent_id_validity(self):
        """parent_id must refer to a valid, existing page_id and must not form cycles."""
        all_page_ids = set(d["frontmatter"]["page_id"] for d in self.parsed_docs)
        self.assertEqual(len(all_page_ids), 87, "Expected exactly 87 unique logical documents")

        parent_map = {}
        for doc in self.parsed_docs:
            fm = doc["frontmatter"]
            pid = fm["page_id"]
            parent_id = fm.get("parent_id")
            if parent_id is not None:
                parent_str = str(parent_id).strip()
                self.assertNotEqual(
                    parent_str, pid,
                    f"Document '{doc['rel_path']}' has itself as parent_id ('{parent_str}')"
                )
                self.assertIn(
                    parent_str, all_page_ids,
                    f"Document '{doc['rel_path']}' has invalid parent_id '{parent_str}': parent page_id not found"
                )
                parent_map[pid] = parent_str

        # Cycle detection
        for start_id in parent_map:
            visited = set()
            curr = start_id
            while curr in parent_map:
                self.assertNotIn(
                    curr, visited,
                    f"Cyclic hierarchy detected involving page_id '{curr}' starting from '{start_id}'"
                )
                visited.add(curr)
                curr = parent_map[curr]

    def test_source_lang_validity(self):
        """source_lang must strictly identify an authoritative repository variant that exists."""
        docs_by_id = {}
        for doc in self.parsed_docs:
            pid = doc["frontmatter"]["page_id"]
            lang = doc["frontmatter"]["lang"]
            docs_by_id.setdefault(pid, {})[lang] = doc

        for pid, variants in docs_by_id.items():
            for lang, doc in variants.items():
                source_lang = doc["frontmatter"]["source_lang"]
                self.assertIn(
                    source_lang, variants,
                    f"Document '{doc['rel_path']}' declares source_lang '{source_lang}', but no variant for '{source_lang}' exists in the repository for page_id '{pid}'"
                )

    def test_multilingual_metadata_consistency(self):
        """All language variants of a logical document must share page_id, parent_id, and source_lang."""
        docs_by_id = {}
        for doc in self.parsed_docs:
            pid = doc["frontmatter"]["page_id"]
            docs_by_id.setdefault(pid, []).append(doc)

        for pid, variants in docs_by_id.items():
            if len(variants) > 1:
                first_fm = variants[0]["frontmatter"]
                for other in variants[1:]:
                    other_fm = other["frontmatter"]
                    self.assertEqual(
                        first_fm.get("parent_id"), other_fm.get("parent_id"),
                        f"parent_id mismatch for page_id '{pid}' between '{variants[0]['rel_path']}' and '{other['rel_path']}'"
                    )
                    self.assertEqual(
                        first_fm.get("source_lang"), other_fm.get("source_lang"),
                        f"source_lang mismatch for page_id '{pid}' between '{variants[0]['rel_path']}' and '{other['rel_path']}'"
                    )

    def test_legacy_routes_manifest_retention(self):
        """All 177 generated public routes from legacy_routes.json must be accounted for and match _site."""
        manifest_path = REPO_ROOT / ".agents/i18n-architecture/legacy_routes.json"
        self.assertTrue(manifest_path.is_file(), "legacy_routes.json manifest not found")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        routes = manifest["routes"]
        self.assertEqual(len(routes), 177, "Expected exactly 177 routes in legacy_routes.json")

        site_dir = REPO_ROOT / "_site"
        if site_dir.is_dir():
            missing = []
            for r in routes:
                fpath = site_dir / r["file_in_site"]
                if not fpath.is_file():
                    missing.append(r["file_in_site"])
            self.assertEqual(
                len(missing), 0,
                f"Missing {len(missing)} routes in _site: {missing[:10]}"
            )


if __name__ == "__main__":
    unittest.main()
