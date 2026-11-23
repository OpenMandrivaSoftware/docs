# Architecture Specification: Scalable Multilingual Documentation (v2.0)

**Baseline Commit:** `b3014780fc0e53194e83cc822dad29f3fc289ba2`  
**Dependencies:** `jekyll 4.4.1`, `jekyll-polyglot 1.14.0`, `just-the-docs 0.12.0`  
**Target Languages:** English (`default_lang: en`), French (`fr`), German (`de`), Russian (`ru`)

---

## 1. Architectural Principles & Requirements

1. **Default Language:** English remains `default_lang: en`.
2. **Immutable Identity (`page_id`):** Every logical document has an immutable, language-neutral `page_id` (e.g. `user-guide.managing-software.using-dnf`) shared by all its translations.
3. **Content Locale (`lang`):** Every source file declares its actual language (`lang: en`, `lang: fr`, etc.).
4. **Authoritative Source Locale (`source_lang`):** Every document declares `source_lang`, identifying the authoritative repository variant used for translation and fallback. A document must never declare a `source_lang` that does not exist in the repository.
5. **Canonical Language-Neutral Permalink:** All translations of a logical document declare the exact same clean permalink (e.g. `permalink: /user-guide/managing-software/using-dnf/`).
6. **Clean Public Routing:**
   - English default: `/section/doc/` (served from root)
   - French: `/fr/section/doc/`
   - German: `/de/section/doc/`
   - Russian: `/ru/section/doc/`
7. **Robust Hierarchy (`parent_id`):** Hierarchy is established by referencing the parent's `page_id` via `parent_id:` rather than translated page titles.
8. **Deterministic Ordering (`nav_order`):** Explicit numeric ordering for predictable sibling sequencing.
9. **Zero Language Branching in Engine:** Zero hardcoded conditionals for specific languages (`en`, `fr`, `de`, `ru`) in layouts, includes, or plugins.
10. **Zero Re-engineering for New Languages:** Adding a language requires only adding its code to `languages` in `_config.yml` and authoring Markdown files.

---

## 2. Source Organization & Target Routing

Documents are co-located by logical document folder:

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

### Public Route Model:
- **Default (`en`):** Output at site root (e.g. `_site/getting-started/installation/index.html` -> `/getting-started/installation/`).
- **Non-default (`fr`, `de`, `ru`):** Output in language subdirectory (e.g. `_site/fr/getting-started/installation/index.html` -> `/fr/getting-started/installation/`).
- **Homepage:** `index.{lang}.md` with `permalink: /` renders directly to `/` (`_site/index.html`) for English, `/fr/` (`_site/fr/index.html`) for French, etc.

---

## 3. Dependency Behavior & Gap Analysis

### 3.1 Jekyll Polyglot 1.14.0
- **`page_id`:** Native first-class support in `Site#coordinate_documents` and `Site#find_translations`.
- **Identical `permalink`:** Polyglot sets `@dest = "#{@dest}/#{@active_lang}"` during localized passes and automatically relativizes internal URLs in HTML.
- **Native metadata:** `rendered_lang` (actual language of rendered content), `permalink_lang` (map of available translations), `available_languages`, and `missing_languages`.
- **Static assets:** Configured via `exclude_from_localization` (`assets`, `images`), keeping shared assets at root without duplication.
- **Execution hook:** Document coordination occurs at `:site, :post_read`.

### 3.2 The Polyglot Fallback Gap & Solution
#### The Limitation:
The fallback policy requires:
1. Actual translation in requested locale.
2. English variant (`default_lang`), if available.
3. Original variant identified by `source_lang`.
4. Metadata validation error if missing.

In native Polyglot (`site.rb` lines 186–196):
When an article has no English translation, and a visitor requests a language lacking a translation (e.g. Russian visitor, article exists only in French `source_lang: fr` and German `de`), Polyglot's fallback is non-deterministic: whichever file happens to be read second by the filesystem overwrites the first, ignoring `source_lang`.

#### The Minimal Compatible Adapter:
A 20-line plugin in `_plugins/polyglot_fallback_adapter.rb`:
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
By sorting documents in ascending fallback priority (`other (0) < source_lang (1) < default_lang (2) < active_lang (3)`), the most authoritative variant is processed last and deterministically wins. Tested and proven in `test/test_i18n_architecture.py`.

---

## 4. Navigation Architecture: Approach Comparison & Selection

### 4.1 Evaluation of Approaches

#### Approach A: Metadata Resolution Adapter (Selected)
Author writes clean, immutable metadata in Markdown:
```yaml
page_id: user-guide.managing-software.dnf
parent_id: user-guide.managing-software
nav_order: 10
```
A lightweight Jekyll hook (`:site, :post_read`, priority: low) resolves `parent_id` into the exact title strings expected by Just the Docs:
```ruby
Jekyll::Hooks.register :site, :post_read, priority: :low do |site|
  pages_by_id = site.pages.each_with_object({}) { |p, h| h[p.data['page_id']] = p if p.data['page_id'] }
  site.pages.each do |p|
    if (parent_id = p.data['parent_id']) && (parent = pages_by_id[parent_id])
      p.data['parent'] = parent.data['title']
      if (g_id = parent.data['parent_id']) && (grand = pages_by_id[g_id])
        p.data['grand_parent'] = grand.data['title']
      end
    end
  end
end
```

**Why Approach A is superior:**
1. **Zero Upstream Template Overrides:** Leaves `breadcrumbs.html`, `links.html`, `children.html`, and `children_nav.html` completely standard and untouched.
2. **Breadcrumbs Compatibility:** Just the Docs `breadcrumbs.html` parses `site_nav` HTML and requires `page.parent` to be non-nil. Approach A populates `page.parent` dynamically with the parent's actual localized title.
3. **Fallback Child / Localized Parent:** If parent is in French ("Premiers pas") and child is English fallback, child's `parent` is resolved to "Premiers pas", maintaining intact hierarchy.
4. **Translated Child / Fallback Parent:** If parent is English fallback ("User Guide") and child is French, child's `parent` is resolved to "User Guide", seamlessly attaching it.
5. **Arbitrary Nesting & Ordering:** Preserves Just the Docs 3-level nesting, `child_nav_order`, and numeric `nav_order`.
6. **Cache Isolation:** The repository already overrides `_includes/components/sidebar.html` to omit `include_cached`, ensuring nav is re-evaluated per locale.

#### Approach B: Full Custom Navigation Tree (Rejected)
Overriding `site_nav.html`, `nav/pages.html`, `nav/children.html`, `nav/links.html`, `breadcrumbs.html`, and `children_nav.html` to use `page_id` directly.
- **Drawbacks:** High maintenance overhead, breaks on theme updates, risks markup/accessibility regressions (expander buttons, aria attributes).

---

## 5. Source Language (`source_lang`) Semantics

### Definition:
`source_lang` strictly identifies the **authoritative source variant currently present in the repository** that translations derive from and that fallback resolves to.

### Semantic Rules:
1. A document **must never** reference `source_lang: fr` if no French variant exists in the repository.
2. For all 83 English-only documents, `source_lang: en`. (Historical authoring language is an editorial concern and can be recorded as optional `original_lang:` without affecting engine fallback).
3. For the 4 translated documents in the repository:
   - `index.{en,fr}.md`: Authoritative source is `en`. (`source_lang: en`).
   - `getting-started/index.{en,fr}.md`: Authoritative source is `en`. (`source_lang: en`).
   - `getting-started/downloading-openmandriva.{en,fr}.md`: Authoritative source is `en`. (`source_lang: en`).
   - `getting-started/copying-openmandriva-to-a-usb-stick.{en,fr}.md`: Authoritative source is `en`. (`source_lang: en`).
4. Any document originating in French (e.g. future association statutes or community French drafts) that has a French source variant will set `source_lang: fr`.

---

## 6. Approved Phased Migration Sequence

To prevent broken intermediate states, the migration is strictly divided into sequential, verified iterations:

### Iteration 03B: Stable Identities & File Reorganization
- Introduce stable frontmatter schema (`page_id`, `parent_id`, `source_lang`).
- Reorganize Markdown files into logical directories (`section/doc/index.{lang}.md`).
- **Preserve existing public routes:** Documents declare explicit `permalink:` pointing to their current legacy paths (e.g. `permalink: /getting-started/downloading-openmandriva.en.html`), ensuring zero URL breakage.
- Add `_plugins/metadata_validator.rb` to enforce ID uniqueness and parent validity at build time.

### Iteration 03C: Canonical Permalinks & Legacy Route Preservation
- Switch documents to clean canonical permalinks (`permalink: /getting-started/downloading-openmandriva/`).
- Preserve legacy routes via `redirect_from`:
  - Each document variant declares its old `.html` path in `redirect_from:`.
  - Verified redirect mechanism emits standard static redirect stubs with `<meta http-equiv="refresh">`, `<link rel="canonical">`, and JavaScript query/hash preservation.
- Update internal markdown links to canonical paths.
- Replace root `index.html` static redirect with canonical `/` on `index.en.md`.

### Iteration 04: Deterministic Fallback & Metadata-Driven Language Switching
- Implement `_plugins/polyglot_fallback_adapter.rb`.
- Refactor `_includes/components/lang_switcher.html` to use Polyglot's native `page.permalink_lang` instead of client-side path guessing.

### Iteration 05: Hierarchical Navigation & Parent Resolution
- Implement Approach A adapter (`_plugins/parent_id_adapter.rb`) resolving `parent_id` into Just the Docs parent/ancestor metadata.
- Clean up obsolete nav filters.

---

## 7. Redirect and Asset Strategy

### 7.1 Redirect Mechanism Verification
- Both `jekyll-redirect-from` and a dedicated zero-dependency generator emit the standard HTML redirect contract:
  ```html
  <link rel="canonical" href="https://docs.openmandriva.org/section/doc/">
  <meta http-equiv="refresh" content="0; url=https://docs.openmandriva.org/section/doc/">
  <script>window.location.href = 'https://docs.openmandriva.org/section/doc/' + window.location.search + window.location.hash;</script>
  ```
- **Preservation:** Fragment anchors (`#heading`) and query parameters (`?query`) are preserved by the script window location concatenation.
- **Cycles:** Zero risk of cycles because target `/section/doc/` is physically distinct from legacy `/section/doc.en.html`.

### 7.2 Asset Strategy
- **Global Assets:** Remain in `/assets/images/` and are excluded from localization (`exclude_from_localization`).
- **Document-Specific Images:** Co-located in `./images/` within the document folder. When moving `section/doc.en.md` to `section/doc/index.en.md`, the associated `images/` directory is moved to `section/doc/images/`. All relative links `./images/image-01.png` remain completely intact.

---

## 8. Reproducible Test Suite & Verification

The architecture and fallback behavior are backed by an automated integration test suite in `test/test_i18n_architecture.py` using fixture `test/fixtures/i18n_architecture/`:
- **Execution:** `python3 -m unittest test/test_i18n_architecture.py` (or `python3 -m unittest discover -s test -p "test_*.py"`).
- **Runtime:** ~1.5s for 10 automated test cases.
- **Scenarios Verified:**
  1. Localized homepages on `/`, `/fr/`, `/de/`, `/ru/`.
  2. English original with French/German translations; Russian fallback to English.
  3. English-only article rendering across all language trees in English.
  4. French original with English translation; German/Russian fallback to English.
  5. French original with German translation, no English; Russian fallback deterministically to French original (`source_lang: fr`).
  6. French-only article rendering across all language trees in French.
  7. Nested hierarchy with mixed translation availability and `resolved_parent` verification under Approach A.
  8. Shared assets excluded from localization and preserved at site root.
  9. Non-empty baseurl build.
  10. Document order determinism proof (permutations yield identical fallback).
