---
name: Cards Navigation System
description: Home page and section landing pages use a card-based navigation system driven by frontmatter data and a reusable Liquid include.
---

# Cards Navigation Implementation

The site uses a card-based navigation system on the home page and all section landing pages. Cards provide visual previews of documentation sections with a consistent style across the site.

## Components

| Component | Location | Purpose |
|---|---|---|
| **Home page cards** | `_data/home_cards.yml` | YAML data file for home page cards (title, description, links) |
| **Home page template** | `index.en.md` | Uses `layout: home` with inline Liquid loop |
| **Section cards include** | `_includes/section_cards.html` | Reusable Liquid include for section landing pages |
| **Stylesheet** | `_sass/custom/custom.scss` | Defines `.home-cards`, `.home-card`, `.section-cards`, `.section-card` |

## Home Page Cards

The home page reads from `_data/home_cards.yml` and renders cards with a title, description, and a list of links.

### Configuration

To add or modify home page cards:

1. Edit `_data/home_cards.yml`.
2. Add a new entry with `title`, `description`, `base_url` (or `url` for external links), and a `links` array.

### YAML Format

```yaml
- title: "Getting Started"
  description: "New to OpenMandriva? Start here."
  base_url: "/getting-started"
  links:
    - name: "Downloading OpenMandriva"
      base_url: "/getting-started/downloading-openmandriva"
    - name: "Copying to a USB"
      base_url: "/getting-started/copying-to-usb"
```

## Section Landing Page Cards

Section index pages (e.g., `user-guide/index.en.md`, `dev/index.en.md`) use frontmatter-driven card data and the `section_cards.html` include.

### Configuration

1. Add `card_columns: 3` to the frontmatter (or `2` for two columns).
2. Add a `cards` array to the frontmatter with `title`, `description`, and `url` for each card.
3. Add `{% include section_cards.html %}` in the page body where you want the cards to appear.

### Frontmatter Format

```yaml
---
layout: default
title: User Guide
nav_order: 20
card_columns: 3
cards:
  - title: "Managing Software"
    description: "Install, remove, and update software."
    url: "/user-guide/managing-software.en.html"
  - title: "Troubleshooting"
    description: "Fix common problems."
    url: "/user-guide/troubleshooting/index.en.html"
---
{% include section_cards.html %}
```

### Include Template

The `{% include section_cards.html %}` tag renders this HTML structure:

```html
<div class="section-cards cols-3">
  {% for card in page.cards %}
  <a href="{{ card.url }}" class="section-card">
    <div class="card-title">{{ card.title }}</div>
    <p class="description">{{ card.description }}</p>
  </a>
  {% endfor %}
</div>
```

> **Important:** Use `<div class="card-title">` instead of `<h3>`. Just the Docs automatically appends an anchor link to every heading. Since section cards use an `<a>` element as the card wrapper, nesting an `<h3>` with its anchor link inside the `<a>` creates nested anchors, which browsers break out of---scrambling the layout.

### Card Fields

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Card heading (renders as `<h3>`) |
| `description` | Yes | Short summary below the title |
| `url` | Yes | Destination link---the entire card is clickable |
| `base_url` | No | Alternative to `url`---appends `.en.html` |

## CSS Classes

### Home Cards

```scss
.home-cards          // Grid container
.home-cards.cols-1   // Single column
.home-cards.cols-2   // Two columns (used on home page)
.home-cards.cols-3   // Three columns (used on section pages)
.home-card           // Individual card (has hover effect, border, shadow)
```

### Section Cards

```scss
.section-cards          // Grid container (mirrors .home-cards)
.section-cards.cols-3   // Three columns on desktop, 1 on mobile
.section-card           // Individual card (same visual style as .home-card)
```

### Responsive Behavior

- On screens wider than 66.5rem: cards display in the specified column count (2 or 3).
- On smaller screens: all cards collapse to a single column.

### Visual Consistency

Section cards use the same border, padding, shadow, and hover effect as home cards for visual consistency. The key difference is that section cards are clickable blocks with just a title and description---no link lists.

## Lessons Learned

1. **CSS is in SCSS, not CSS.** The stylesheet is `_sass/custom/custom.scss`, not `assets/css/custom.css`. SCSS allows variable interpolation with Just the Docs theme variables like `$border-color`, `$link-color`, and `$body-background-color`.
2. **Frontmatter over YAML data files for sections.** Using frontmatter for card data keeps each language file (`.en.md`, `.fr.md`) self-contained, which works naturally with the jekyll-polyglot multilingual setup.
3. **Reuse CSS classes.** Section cards use a parallel class structure (`.section-cards` / `.section-card`) that mirrors the home card styles, making it easy to maintain a consistent look.
4. **Column count via frontmatter.** The `card_columns` frontmatter variable controls the grid layout. Three columns works well for section landing pages; two columns works for the home page which has more content per card.
5. **Avoid nested anchors.** Just the Docs appends anchor links to every heading. Never place an `<h3>` (or any heading) inside an `<a>` element. Use `<div class="card-title">` instead, styled via CSS to match the heading size.
