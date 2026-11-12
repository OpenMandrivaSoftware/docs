# Architecture Specification: Scalable Multilingual Documentation

This document defines the target architecture, verified dependency behavior, metadata schema, and migration strategy for OpenMandriva Docs internationalization.

---

## 1. Executive Summary & Principles

The goal of this architecture is to provide a robust, maintainable, and scalable multilingual foundation for OpenMandriva Docs, supporting English (`en`), French (`fr`), German (`de`), Russian (`ru`), and future languages without hardcoded engine logic.

### Core Architectural Rules:
1. **Default Language:** English remains `default_lang: en`.
2. **Logical Identity (`page_id`):** Every logical document has an immutable, language-neutral `page_id` (e.g. `user-guide.managing-software.using-dnf`) shared across all its translations.
3. **Declared Content Locale (`lang`):** Each document file declares its actual language (`lang: en`, `lang: fr`, `lang: de`, `lang: ru`).
4. **Declared Original Locale (`source_lang`):** Each document declares `source_lang` identifying the original authoring language (e.g. `source_lang: fr` for French original articles).
5. **Canonical Language-Neutral Permalink:** All translations of a logical document declare the exact same clean permalink (e.g. `permalink: /user-guide/managing-software/using-dnf/`).
6. **Clean Public Routing:**
   - English default: `/user-guide/managing-software/using-dnf/` (served from site root)
   - French: `/fr/user-guide/managing-software/using-dnf/`
   - German: `/de/user-guide/managing-software/using-dnf/`
   - Russian: `/ru/user-guide/managing-software/using-dnf/`
7. **Robust Hierarchy (`parent_id`):** Page hierarchy is established by referencing the parent's `page_id` via `parent_id:` rather than translated page titles. This eliminates title collisions, title translation mismatches, and broken navigation when parents or children are in fallback mode.
8. **Deterministic Ordering (`nav_order`):** Explicit numeric ordering for predictable sibling sequencing.
9. **Zero Language Branching in Engine:** The engine, templates, and plugins contain zero hardcoded conditionals for specific languages (`en`, `fr`, `de`, `ru`).
10. **Zero Re-engineering for New Languages:** Adding a language requires only adding its code to `languages` in `_config.yml` and creating Markdown files.

---

## 2. Target Source Organization

Translations are co-located by logical document folder:

```
getting-started/
  index.en.md
  index.fr.md
  installation/
    index.en.md
    index.fr.md
    index.de.md
    index.ru.md
    images/
      step-01.png
```

### Routing Mapping:
| Logical Document | Language | Source File | Public Route | Output File |
|---|---|---|---|---|
| `home` | `en` | `index.en.md` | `/` | `_site/index.html` |
| `home` | `fr` | `index.fr.md` | `/fr/` | `_site/fr/index.html` |
| `getting-started` | `en` | `getting-started/index.en.md` | `/getting-started/` | `_site/getting-started/index.html` |
| `getting-started` | `fr` | `getting-started/index.fr.md` | `/fr/getting-started/` | `_site/fr/getting-started/index.html` |
| `getting-started.installation` | `en` | `getting-started/installation/index.en.md` | `/getting-started/installation/` | `_site/getting-started/installation/index.html` |
| `getting-started.installation` | `de` | `getting-started/installation/index.de.md` | `/de/getting-started/installation/` | `_site/de/getting-started/installation/index.html` |

---

## 3. Dependency Behavior & Verification

Verified against installed dependencies:
- **Jekyll:** `4.4.1`
- **Jekyll Polyglot:** `1.14.0`
- **Just the Docs:** `0.12.0`

### 3.1 Jekyll Polyglot Analysis
Source inspection of `jekyll-polyglot-1.14.0/lib/jekyll/polyglot/patches/jekyll/site.rb`:
- **`page_id`:** Native first-class support (`page_id = doc.data['page_id'] || url`). Used by `find_translations` to correlate variants.
- **Identical `permalink`:** When translations share `permalink: /path/`, Polyglot sets `@dest = "#{dest}/#{active_lang}"` during subsite processing and relativizes internal URLs in output HTML. Root-relative permalinks naturally resolve to localized subdirectories without manually prefixing `/lang/`.
- **`site.active_lang`:** Exported into site payload during each language pass.
- **`rendered_lang`:** Native field set on each page to indicate which language variant actually provided the rendered content. When a page falls back (e.g. English rendered on French subsite), `page.rendered_lang != site.active_lang`.
- **`permalink_lang`:** Hash `{ lang => permalink }` computed by `find_translations`.
- **`available_languages`:** Array of language codes for which actual variants exist.
- **`missing_languages`:** Configured languages lacking an actual variant (`configured - available_languages`).
- **Discovery of Assets:** `exclude_from_localization: ['assets', 'images', ...]` ensures static files are processed only once in the default pass and placed at root (`_site/assets/...`), preventing asset duplication.
- **Execution Lifecycle:** Polyglot coordinates documents in a `:site, :post_read` hook (`hooks/coordinate.rb`), before generators and renderers run.

### 3.2 The Polyglot Fallback Gap & Solution
#### The Native Limitation:
The fallback policy requires:
1. Actual translation in requested locale.
2. English variant (`default_lang`), if available.
3. Original variant identified by `source_lang`.
4. Error if declared original is missing.

In native Polyglot (`site.rb` lines 186-196):
```ruby
next if @file_langs[page_id] == @active_lang
next if @file_langs[page_id] == @default_lang && lang != @active_lang
approved[page_id] = doc
@file_langs[page_id] = lang
```
When an article exists in French (`source_lang: fr`) and German (`de`), but has **no English translation**, and a Russian visitor (`ru`) requests the page:
- If `fr` is processed first, `approved[page_id] = fr`.
- When `de` is processed, `@file_langs[page_id]` is `"fr"` (neither `@active_lang` nor `@default_lang`).
- Therefore, line 194 blindly replaces `fr` with `de`!
- The variant selected for fallback is dictated solely by file discovery order on disk, completely ignoring `source_lang`.

#### The Minimal Compatible Adapter:
Without forking Polyglot, we introduce a 20-line adapter in `_plugins/polyglot_fallback_adapter.rb`:
```ruby
module Jekyll
  class Site
    alias_method :coordinate_documents_polyglot_orig, :coordinate_documents

    def coordinate_documents(docs)
      sorted_docs = docs.sort_by do |doc|
        lang = doc.data['lang'] || derive_lang_from_path(doc) || @default_lang
        source_lang = doc.data['source_lang']

        priority = 0
        priority = 1 if source_lang && lang == source_lang
        priority = 2 if lang == @default_lang
        priority = 3 if lang == @active_lang
        priority
      end
      coordinate_documents_polyglot_orig(sorted_docs)
    end
  end
end
```
By sorting documents in ascending priority order (`other < source_lang < default_lang < active_lang`), the most authoritative variant is processed last and deterministically wins. Proven in test fixtures to yield 100% deterministic, policy-compliant fallbacks.

---

## 4. Navigation Architecture (Just the Docs Override)

### 4.1 The Native Just the Docs Limitation
Native Just the Docs (`_includes/components/nav/pages.html` and `children.html`) structures hierarchy using translated page titles:
`nav_candidates = nav_parenthood | where: "name", include.node.title`
This causes critical failures in multilingual documentation:
1. Parent translated title changes break child linkage.
2. Mixed-language fallback leaves parents in English while children reference localized titles.
3. Identical titles in different sections cause hierarchy collisions.

### 4.2 The `page_id` / `parent_id` Navigation Engine
Because Polyglot's `coordinate_documents` already guarantees that `site.html_pages` contains exactly one coordinated page per `page_id` during each language pass, we override `_includes/components/nav/pages.html`:

```liquid
{%- assign by_parent = include.pages
      | where_exp: "item", "item.page_id != nil"
      | group_by: "parent_id" -%}

{%- assign top_group = by_parent
      | where_exp: "item", "item.name == nil or item.name == ''"
      | first -%}

{%- assign nav_top_nodes = top_group.items | sort: "nav_order" -%}
{%- assign nav_ancestors = "" | split: "" -%}
{%- include components/nav/links.html pages=nav_top_nodes ancestors=nav_ancestors all=include.all -%}
```

And in `children.html`:
```liquid
{%- assign child_group = nav_parenthood
      | where: "name", include.node.page_id
      | first -%}
{%- assign nav_children = child_group.items | sort: "nav_order" -%}
```

**Benefits:**
- 100% language-agnostic.
- Zero string matching on translated titles.
- Sibling ordering strictly follows numeric `nav_order`.
- Completely immune to title changes and fallback states.

---

## 5. Isolated Architecture Proof (Experimental Results)

Conducted in isolated sandbox fixture (`/tmp/om_polyglot_proof` and `/tmp/om_polyglot_adapter_proof`).

### Verified Scenarios:
1. **English original with French and German translations (`articles.installation`):**
   - `_site/articles/installation/index.html` rendered EN (Title: "Installation Guide EN").
   - `_site/fr/articles/installation/index.html` rendered FR (Title: "Guide d'installation FR").
   - `_site/de/articles/installation/index.html` rendered DE (Title: "Installationsanleitung DE").
   - `_site/ru/articles/installation/index.html` rendered EN fallback (`rendered_lang: en`).
2. **English-only article (`articles.kernel`):**
   - Rendered across all language trees (`/`, `/fr/`, `/de/`, `/ru/`) with `rendered_lang: en`.
3. **French original with English translation (`articles.cooker`):**
   - EN subsite rendered EN translation.
   - FR subsite rendered FR original.
   - DE and RU subsites rendered EN fallback.
4. **French original with German translation, NO English translation (`articles.packaging-spec`):**
   - With native Polyglot: Non-deterministic fallback between FR and DE in RU tree depending on file order.
   - With `polyglot_fallback_adapter.rb`: RU tree deterministically rendered FR original (`rendered_lang: fr`) regardless of file read order.
5. **French-only article (`articles.association-statutes`):**
   - Rendered across all language trees (`/`, `/fr/`, `/de/`, `/ru/`) with `rendered_lang: fr`.
6. **Nested hierarchy with mixed translations (`user-guide` parent, `dnf` child, `steam` child):**
   - Tree structure remained perfectly intact across all languages.
   - French child `steam` nested under English parent `user-guide` in RU subsite without orphan errors.
7. **Localized Homepage on Root Route (`/`):**
   - Root `/index.html` generated EN homepage directly.
   - `/fr/index.html` generated FR homepage.
   - `/de/index.html` generated DE homepage.
   - `/ru/index.html` generated RU homepage.
   - Eliminates legacy redirect hack in root `index.html`.
8. **Shared Assets:**
   - Single instance of `/assets/images/shared-logo.png` at root; correctly referenced by all localized documents.
9. **Non-empty Baseurl (`baseurl: /docs`):**
   - Build succeeded with code 0; all relative links correctly prefixed.

---

## 6. Metadata Schema Specification

Every production documentation file must conform to this schema:

```yaml
---
layout: default
page_id: string          # Required. Dot-delimited logical identifier (e.g. 'getting-started.installation')
parent_id: string        # Optional. Reference to parent's page_id (omit or null for section roots)
lang: string             # Required. Two-letter ISO code of content ('en', 'fr', 'de', 'ru')
source_lang: string      # Required. Two-letter ISO code of original article authoring language
title: string            # Required. Localized human-readable title
permalink: string        # Required. Language-neutral canonical path with leading/trailing slash (e.g. '/getting-started/installation/')
nav_order: integer       # Required for ordered siblings. Numeric ordering weight
has_children: boolean    # Optional. Set true if page has child articles
has_toc: boolean         # Optional. True to render right-sidebar page TOC
---
```

---

## 7. Migration Plan

The migration will be carried out in 5 distinct, independently testable phases:

### Phase 1: Core Plugins & Navigation Overrides
- Add `_plugins/polyglot_fallback_adapter.rb` (deterministic `source_lang` fallback).
- Add `_plugins/metadata_validator.rb` (verifies `page_id`, `parent_id`, `source_lang` integrity at build time).
- Override `_includes/components/nav/pages.html` and `children.html` to support `parent_id` while maintaining backwards compatibility with legacy `parent:` title strings during migration.

### Phase 2: Content Reorganization & Metadata Migration (Sections 1 & 2)
- Reorganize `getting-started/` and `user-guide/` into logical document folders (`getting-started/installation/index.en.md`, etc.).
- Inject canonical `page_id`, `parent_id`, `source_lang`, and clean `permalink`.

### Phase 3: Content Reorganization & Metadata Migration (Sections 3 & 4 + Homepage)
- Reorganize `dev/`, `community/`, and root `index.{en,fr}.md`.
- Replace root `index.html` redirect with clean `permalink: /` on `index.en.md`.

### Phase 4: Backward-Compatible Legacy Redirects
- Implement `_plugins/legacy_redirects.rb` generator.
- Generates static redirect stubs with `<meta http-equiv="refresh">` and `<link rel="canonical">` for all 87 legacy `.en.html` and `.fr.html` paths.
- Ensures existing external links, bookmarks, and search engine indices do not 404.

### Phase 5: Language Switcher & Final Cleanup
- Refactor `_includes/components/lang_switcher.html` to use `page.permalink_lang` from Polyglot.
- Remove client-side JS path-guessing workarounds.
- Update link validator test suite to verify canonical URLs.

---

## 8. Remaining Risks & Editorial Decisions

1. **Original Language Verification:**
   - 4 documents have French variants (`index`, `getting-started/index`, `downloading-openmandriva`, `copying-openmandriva-to-a-usb-stick`).
   - Editorial confirmation is required on whether the French variants were translated from English, or if certain community bylaws originated in French. By default, `source_lang: en` is assigned to technical docs and `source_lang: fr` to French association legal texts where applicable.
2. **External Link Influx:**
   - Existing external links to `*.en.html` must remain operational indefinitely via the legacy redirect generator.
3. **Card Links:**
   - `_data/home_cards.yml` and section landing page cards currently point to legacy URLs. They will be updated to clean permalinks in Phase 2 & 3.
