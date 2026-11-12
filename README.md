# OpenMandriva Documentation

This repository builds the OpenMandriva documentation site with Jekyll, the Just the Docs theme, and the Jekyll Polyglot plugin.

## Prerequisites

To build and run the documentation site locally, you need:
- **Ruby:** 3.2 to 4.0 (`Gemfile` specifies `>= 3.2.0, < 4.1.0`; verified on Ruby 3.3 in CI and Ruby 4.0.9 on OpenMandriva Lx 26.09 ROME)
- **RubyGems:** 3.4.1+ (RubyGems 4.0.24 is included with Ruby on OpenMandriva Lx)
- **Bundler:** 4.0.24 (locked in `Gemfile.lock`)
- **Ruby development headers:** `ruby-devel` / `ruby-full` (for native gem compilation, including `sass-embedded`)
- **Build tools:** `gcc`, `g++`, `make`, `git`

For running the complete automated verification suite (`./test/run_checks.sh`):
- **Python:** 3.10+ (for `test/check_links.py` and unit tests, standard library only)
- **Node.js:** 18+ (for `test/theme-toggle.test.js`)

### OpenMandriva Lx
```sh
sudo dnf --refresh install ruby ruby-devel gcc gcc-c++ make git nodejs python3
```

### Fedora / RHEL
```sh
sudo dnf install ruby ruby-devel rubygem-bundler gcc gcc-c++ make git nodejs python3
```

### Debian / Ubuntu
```sh
sudo apt-get update && sudo apt-get install ruby-full build-essential zlib1g-dev git nodejs python3
gem install bundler -v 4.0.24
```

## Run the site locally

From the repository root, install the dependencies and start Jekyll:

```sh
bundle install
bundle exec jekyll serve
```

Open the [English home page](http://localhost:4000/index.en.html) or the [French home page](http://localhost:4000/fr/index.fr.html). The site root redirects to the English home page.

## Testing and Verification

To run all automated checks locally (Python unit tests, JavaScript theme toggle tests, production build, and link/asset validation):

```sh
./test/run_checks.sh
```

Individual checks can also be executed separately:

- **Python validator unit tests:**
  ```sh
  python3 -m unittest discover -s test -p "test_*.py"
  ```
- **JavaScript theme toggle tests:**
  ```sh
  node test/theme-toggle.test.js
  ```
- **Internal link and asset validation:**
  ```sh
  bundle exec jekyll build
  python3 test/check_links.py --site-dir _site
  ```

## Build and publish

```sh
JEKYLL_ENV=production bundle exec jekyll build
```

Jekyll writes the static site to `_site/`. Publish its contents with the directory structure intact. The current configuration assumes the site is served at the domain root. The home page redirect and several internal links use paths from that root. [`index.html`](index.html)

For GitHub Pages, run the Jekyll build separately and publish the generated files. The built-in Pages Jekyll build does not support Polyglot. [GitHub Pages documentation](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)

## Edit a page

Keep translations next to their source with the same filename stem, such as `getting-started/downloading-openmandriva.en.md` and `getting-started/downloading-openmandriva.fr.md`. Set `lang` in the YAML front matter. Use the exact `title` of the parent in the same language for `parent`. Omit `parent` on top-level pages.

```yaml
---
layout: default
title: Downloading OpenMandriva
parent: Getting Started
nav_order: 10
lang: en
---
```

Lower `nav_order` values appear first among siblings. Leave gaps of 10 between values to make room for new pages. The right-hand table of contents appears when the page has level-two to level-four headings with anchors. Setting `has_toc: false` hides it and the generated list of child pages.

## Edit landing page cards

### Home pages

Both home pages read card titles, descriptions, and link labels from [`_data/home_cards.yml`](_data/home_cards.yml). A card's `base_url` points to a section with a language-specific index page. Each item in `links` takes a `name` and either a `base_url` for a local page or a `url` for an external link.

```yaml
- title: Getting Started
  description: New to OpenMandriva? Start here to get up and running quickly.
  base_url: /getting-started
  links:
    - name: Copying to a USB Stick
      base_url: /getting-started/copying-openmandriva-to-a-usb-stick
```

On the English home page, this card links to `/getting-started/index.en.html` and its list item links to `/getting-started/copying-openmandriva-to-a-usb-stick.en.html`. The French home page uses the same labels and generates French paths, even for destinations without a translation. Check both home pages when changing the shared data.

### Section pages

Section landing pages keep their cards in front matter. Each card has a `title`, `description`, and `url`. Set `card_columns` to `2` or `3` and place `{% include section_cards.html %}` where the cards should appear in the page body.

```yaml
---
layout: default
title: User Guide
nav_order: 20
lang: en
card_columns: 3
cards:
  - title: Managing Software
    description: Install, remove, and update software.
    url: /user-guide/managing-software.en.html
  - title: Troubleshooting
    description: Fix common system problems.
    url: /user-guide/troubleshooting.en.html
---
```

Keep the section card title as a `div` when editing the include. Just the Docs adds anchor links to headings, and the card itself is already a link. [Card template](_includes/section_cards.html) · [Card styles](_sass/custom/custom.scss) · [User Guide example](user-guide/index.en.md)

## Add or update a translation

English is the default language and builds at the site root. French builds under `/fr/` and currently covers the home page and part of Getting Started. English fallback pages can retain their `.en.html` suffix under `/fr/`. For example, the installation guide builds at `/fr/getting-started/installing-openmandriva.en.html`. [Language configuration](_config.yml)

1. Add or edit the localized Markdown file next to the English page. Match the language suffix and `lang` value.
2. Translate the title and set `parent` to the localized parent's title when the page has a parent. Update links and image descriptions. Link to an existing destination when a related page has yet to be translated.
3. Preview the page in Jekyll. Check its sidebar, links, images, and language switcher.

The language menu reads its list from `_config.yml`. Its JavaScript supports English and French and constructs destination URLs without checking whether the translation exists. To add another language, update `languages` in the configuration, add its Markdown pages and home page, and update the switcher and home page links. [`lang-switcher.js`](assets/js/lang-switcher.js)

## Add images and other assets

Keep article-specific screenshots in an `images/` directory next to the Markdown file. Use the article's filename stem and number the screenshots in the order they appear. The [installation guide](getting-started/installing-openmandriva.en.md) uses `./images/installing-openmandriva-01.png`.

Keep reusable images in `assets/images/`. Polyglot shares the `assets/` directory across languages. For shared assets, use Jekyll's `relative_url` filter to include the site's base path.

```markdown
![OpenMandriva icon]({{ '/assets/images/favicon.png' | relative_url }})
```

Check image URLs in each language preview when adding screenshots to a translated page. See [AGENTS.md](AGENTS.md) for the project's image, naming, and writing conventions.
