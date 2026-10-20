# OpenMandriva Documentation — Content Creator Guide

This guide explains how to author and manage content for the OpenMandriva documentation site.

---

## 1. Navigation (the `parent` directive)

The sidebar navigation is built automatically from your Markdown files. To nest a page under a parent, use the `parent` directive in the YAML headers:

```yaml
---
parent: Getting Started
---
```

- The value must match the **title** of the parent page exactly (not the filename).
- Top-level pages omit `parent` entirely.
- The nav is generated per-language (see `_includes/components/nav/pages.html`). A page only appears in the nav for the language declared in its `lang` field.

---

## 2. Ordering pages (the `nav_order` directive)

Control the order of sibling pages with `nav_order`:

```yaml
---
nav_order: 10
---
```

- Lower numbers appear first.
- Use increments of 10 (10, 20, 30…) so you can insert pages later without renumbering everything.
- Applies within each parent group.

---

## 3. Cards on landing pages

The home page and all section landing pages (Getting Started, User Guide, Developer Docs, Community) use card-based navigation for visual previews of documentation sections.

### Home page cards

The home page (`index.en.md`) uses `layout: home` with card data stored in `_data/home_cards.yml`. Each card can contain a title, description, and a list of links.

**To add or modify a home page card:**

1. Edit `_data/home_cards.yml`.
2. Add or modify an entry:

```yaml
- title: "Getting Started"
  description: "New to OpenMandriva? Start here to get up and running quickly."
  base_url: "/getting-started"
  links:
    - name: "Downloading OpenMandriva"
      base_url: "/getting-started/downloading-openmandriva"
    - name: "Copying to a USB"
      base_url: "/getting-started/copying-to-usb"
    - name: "Installing OpenMandriva"
      base_url: "/getting-started/installing-openmandriva"
```

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Card heading |
| `description` | Yes | Short summary below the title |
| `base_url` | Yes* | Internal link prefix (appends `/index.en.html` for the card title, or `.en.html` for links) |
| `url` | Yes* | External URL (use instead of `base_url` for links leaving the site) |
| `links` | No | Array of sub-links rendered as a list inside the card |

*Use `base_url` for internal pages or `url` for external links.

### Section landing page cards

Section index pages (e.g., `getting-started/index.en.md`, `user-guide/index.en.md`, `dev/index.en.md`, `community/index.en.md`) embed card data directly in the page's YAML frontmatter rather than in a shared data file. This keeps each language file self-contained.

**To add cards to a section landing page:**

1. Add `card_columns: 3` to the page's frontmatter (or `2` for two columns).
2. Add a `cards` array with `title`, `description`, and `url` for each card.
3. Place `{% include section_cards.html %}` in the page body where the cards should appear.

```yaml
---
layout: default
title: User Guide
nav_order: 20
card_columns: 3
lang: en
cards:
  - title: "Managing Software"
    description: "Install, remove, and update software using DNF, DnfDrake, and Steam."
    url: "/user-guide/software.en.html"
  - title: "Troubleshooting"
    description: "Fix broken bootloaders, connect in recovery mode, and resolve time issues."
    url: "/user-guide/troubleshooting/index.en.html"
---

# User Guide

Explore the sections below for detailed instructions.

{% include section_cards.html %}
```

| Card field | Required | Description |
|---|---|---|
| `title` | Yes | Card heading (renders as a styled `<div>`) |
| `description` | Yes | Short summary below the title |
| `url` | Yes | Full path to the destination page (e.g., `/path/page.en.html`) |

> **Important:** Card titles use `<div class="card-title">` in the include template, not `<h3>`. Just the Docs automatically appends anchor links to headings; nesting an `<h3>` inside the card's `<a>` wrapper would create invalid nested anchors and break the layout.

### Styling

Card styles live in `_sass/custom/custom.scss`:

- `.home-cards` / `.home-card` — home page grid and individual cards
- `.section-cards` / `.section-card` — section page grid and individual cards
- `.cols-2` / `.cols-3` — column count classes
- Mobile breakpoint at 66.5rem: all cards collapse to a single column

Section cards share the same border, padding, shadow, and hover-lift effect as home cards for visual consistency.

---

## 4. Adding a new language

1. **Edit `_config.yml`**  
   Add the language code to the `languages` array:
   ```yaml
   languages: ['en', 'fr', 'de']
   ```

2. **Create language-specific Markdown files**  
   For every page, add a `.xx.md` file alongside the English version:
   ```
   getting-started/index.en.md
   getting-started/index.fr.md
   getting-started/index.de.md   # new
   ```

3. **Add `lang` to front matter**  
   Each file must declare its language:
   ```yaml
   ---
   lang: de
   ---
   ```

4. **Create a localized home page**  
   Add `index.de.md` at the site root with the same structure as `index.en.md` / `index.fr.md`.

5. **Build and test**
   ```bash
   bundle exec jekyll build
   bundle exec jekyll serve
   # Visit http://localhost:4000/de/
   ```

No data-file changes are needed — templates construct URLs from `base_url` automatically.

---

## 5. Linking to images and downloadable assets

Place images that go with a specific piece of documentation in an `./images` folder next to that documentation: 

```
installing-openmandriva.en.md 
├── images/
│   └── installing-openmandriva-01.png
│   └── installing-openmandriva-02.png
```

Place global, reusable assets in the `assets/` directory:

```
assets/
├── images/
│   └── om-logo.png
└── files/
    └── openmandriva-install-guide.pdf
```

Reference them in Markdown using **site-root-relative paths**:

```markdown
![Alt text](/assets/images/screenshot.png)

[Download the guide](/assets/files/openmandriva-install-guide.pdf)
```

- `assets/` is listed in `exclude_from_localization` in `_config.yml`, so the same files serve all languages.
- Do **not** use `../` or absolute URLs — they break when the site is built into language subdirectories (e.g., `/fr/`).

---

## 6. Building and deploying

### Prerequisites
- Ruby ≥ 3.0
- Bundler (`gem install bundler`)

### Local development
```bash
bundle install
bundle exec jekyll serve
# Site runs at http://localhost:4000
```

### Production build
```bash
bundle exec jekyll build
```

Output is written to `_site/`:
```
_site/
├── index.en.html          # English home page
├── getting-started/
│   └── index.en.html
├── fr/
│   ├── index.fr.html      # French home page
│   └── getting-started/
│       └── index.fr.html
├── assets/                # Copied as-is (images, CSS, JS, PDFs)
└── ...
```

### Deploy
Upload the **entire `_site/` directory** to your web server or static hosting (Netlify, GitHub Pages, Cloudflare Pages, etc.). Configure the host to serve `index.html` for directory requests.

> **Note:** The site uses `jekyll-polyglot`. Source files for languages (Markdown) are next to the default (en) files for easy maintenance. When deployed, English (default language) stays at the root; other languages live under `/fr/`, `/de/`, etc. Ensure your host preserves this structure.

---

## 7. Quick reference: Required front matter

```yaml
---
layout: default
title: Page Title
nav_order: 10
parent: Parent Page Title   # omit for top-level
card_columns: 3             # optional: only for section landing pages
cards:                      # optional: only for section landing pages
  - title: "Card Title"
    description: "Card summary."
    url: "/path/to/page.en.html"
has_toc: true               # optional, enables right-sidebar TOC
lang: en                    # REQUIRED: en, fr, de, etc.
---
```

All content files live in the repo root or in subdirectories (e.g., `getting-started/`). Side-by-side language files (`.en.md`, `.fr.md`) go in the same folder.