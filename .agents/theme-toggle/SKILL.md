---
name: theme-toggle
description: Adds a system-aware three-state (auto / dark / light) color-scheme toggle that persists the user's choice between sessions.
---

# Theme Toggle (Light / Dark) Implementation

This site uses the [Just the Docs](https://justthedocs.net/) theme, which ships three
precompiled stylesheets — `just-the-docs-default.css` (compiled from the `color_scheme`
setting in `_config.yml`, currently `dark`), `just-the-docs-dark.css`, and
`just-the-docs-light.css`. The theme exposes `jtd.setTheme()` for swapping the first
`[rel="stylesheet"]` link between these files, but it ships **no visible toggle UI** and
the scheme is fixed at build time by `_config.yml`.

This feature adds a header button (immediately to the left of the language switcher)
that cycles through three modes:

| Mode   | Behaviour |
|--------|-----------|
| **Auto**  | Follows the visitor's OS `prefers-color-scheme` preference and **updates live** as it changes. The default on first visit. |
| **Dark**  | Explicit dark theme; pinned so it wins over the system. |
| **Light** | Explicit light theme; pinned so it wins over the system. |

Clicking cycles `auto → dark → light → auto`.

## Preference precedence

| Source              | Priority | Behaviour |
|---------------------|----------|-----------|
| Explicit toggle     | Highest  | `dark` / `light` (and an explicit return to `auto`) is saved to `localStorage` and wins over the system, even after a system change. |
| `localStorage`      | Medium   | Remembered between sessions. If it is `auto`, the site follows the system. |
| `prefers-color-scheme` | Lowest | Used only while in `auto` mode (never chosen, or explicitly chosen `auto`). |

An auto-detected first visit (no saved value) is applied but **not** persisted, so the
site stays in "follow the system" mode and keeps reacting to system changes. Returning
to `auto` *is* persisted, so the explicit "I want auto" is remembered.

## Files

### New files

| File | Purpose |
|------|---------|
| `_includes/head_custom.html` | **Anti-Flicker (FOUT) inline script** — resolves the mode (saved choice → system), swaps the stylesheet and sets `data-theme` / `data-mode` on `<html>` *before first paint*, so the page never flashes with the wrong scheme. Stores the stylesheet base path (Liquid-resolved `relative_url`) on `<html>` for the external script. Also loads `assets/js/theme-toggle.js` with `defer`. |
| `assets/js/theme-toggle.js` | Interactive logic: applies a mode, swaps `just-the-docs-{light,dark}.css`, persists explicit choices to `localStorage`, updates the button `aria-*`, and listens for `prefers-color-scheme` changes while in `auto` mode. |
| `_sass/custom/setup.scss` | Overrides Just the Docs SCSS color variables so the site accent is **OpenMandriva Blue (`#257FBA`)** instead of the theme's default purple / periwinkle, in *both* schemes. |
| `test/theme-toggle.test.js` | Node behaviour tests for the three-state logic (run with `node test/theme-toggle.test.js`). Excluded from the published site via `_config.yml`. |

### Modified files

| File | Change |
|------|--------|
| `_includes/header_custom.html` | Wraps the language switcher in a `.header-extras` group and renders the `#theme-toggle` button (three inline SVGs: auto / dark / light) to its left. |
| `_includes/components/lang_switcher.html` | Rekeys the switcher's light-mode overrides from `@media (prefers-color-scheme: light)` (the OS) to `html[data-theme='light']` (the toggle), so its colours and hover tints track the active scheme regardless of the OS. |
| `_sass/custom/custom.scss` | Adds a `:root` block exposing the per-scheme SCSS color variables as CSS custom properties, the `.theme-toggle` button styles, `.header-extras`, and icon-visibility rules keyed off `html[data-mode]`. |
| `_config.yml` | Adds `test/` to `exclude` so the test harness is not published to `_site`. |

## How the stylesheet swap works

Just the Docs links the first stylesheet as `just-the-docs-default.css`. Both the
anti-flicker script and `theme-toggle.js` update that link's `href` to
`just-the-docs-light.css` or `just-the-docs-dark.css`. Because `_sass/custom/custom.scss`
is imported into **every** color-scheme build (see `_includes/css/just-the-docs.scss.liquid`
→ `{% include css/custom.scss.liquid %}`), each file carries its own scheme-appropriate
values, so a single swap recolors the whole site.

## Accent color (OpenMandriva Blue)

Just the Docs' default accent is a purple (`#6363__`-ish) that, in light mode, clashes
with the OpenMandriva logo; the dark scheme's periwinkle is close to but not exactly
OpenMandriva's brand color. This override pins the site accent to **OpenMandriva Blue
`#257FBA`** in *both* schemes.

The theme resolves its link/ button colors from SCSS variables, and it imports
`_sass/custom/setup.scss` *before* the color-scheme files (see
`_includes/css/just-the-docs.scss.liquid` → `@import "custom/setup"`). The override
therefore works as follows:

- **Light scheme** assigns `$link-color` and `$btn-primary-color` with `!default`, so the
  values set in `setup.scss` take precedence.
- **Dark scheme** assigns those same variables *without* `!default` (so it would normally
  win), but it derives them from `$blue-000` / `$blue-200`:
  - `$link-color: lighten($blue-000, 10%)`
  - `$btn-primary-color: $blue-200`

  Routing those upstream inputs through OM Blue in `setup.scss` makes the dark scheme
  resolve to `#257FBA` too — without touching any of the (unused) blue utility classes
  such as `.btn-blue-*` / `.text-blue-*`.

`_sass/custom/setup.scss`:

```scss
$link-color: #257FBA;
$btn-primary-color: #257FBA;

// Make `lighten($blue-000, 10%)` resolve to OM Blue (#257FBA) in the dark scheme.
$blue-000: darken(#257FBA, 10%);
// Make `$btn-primary-color` (= `$blue-200`) resolve to OM Blue in the dark scheme.
$blue-200: #257FBA;
```

To change the brand color, update those four assignments in `setup.scss` and rebuild.

## The `:root` custom properties

The language switcher (`_includes/components/lang_switcher.html`) and the
"Edit on GitHub" button are authored with `var(--border-color, …)`-style fallbacks. The
theme never defines those properties, so the dark fallbacks always won — the switcher
looked wrong in light mode. The new `:root` block emits the per-scheme SCSS variables as
CSS custom properties:

```scss
:root {
  --body-background-color: #{$body-background-color};
  --body-text-color: #{$body-text-color};
  --body-heading-color: #{$body-heading-color};
  --link-color: #{$link-color};
  --border-color: #{$border-color};
  --sidebar-color: #{$sidebar-color};
  --code-background-color: #{$code-background-color};
  --base-button-color: #{$base-button-color};
  --btn-primary-color: #{$btn-primary-color};
}
```

Each build resolves these to its own scheme values (e.g. dark.css → `--border-color: #44434d`,
`--sidebar-color: #27262b`; light.css → `--border-color: #eeebee`, `--sidebar-color: #f5f6fa`), so the
switcher's static colours adapt automatically. Its remaining light-mode overrides (hover tints and
dropdown shadow) are keyed off `html[data-theme='light']` rather than the OS media query, so they
follow the toggle in every scheme/OS combination.

## Icon behaviour

The button holds three inline SVGs and shows exactly one based on `data-mode` on `<html>`:

| `data-mode` | Icon | Label |
|-------------|------|-------|
| `auto`  | sun + moon | "Theme: auto (follows system). Switch to dark." |
| `dark`  | moon | "Theme: dark. Switch to light." |
| `light` | sun | "Theme: light. Switch to auto." |

With no JavaScript at all the page falls back to the `color_scheme: dark` default and the
auto icon is shown (the button is decorative in that case).

## Accessibility

- The toggle is a native `<button>`, so it is focusable and activates on Enter/Space.
- `aria-label` always describes the current mode and the result of clicking.
- `aria-pressed` is `true` for explicit (`dark`/`light`) modes and `false` for `auto`.
- The decorative icons carry `aria-hidden="true"`.

## Testing

The interactive logic is covered by a Node test harness with a mocked DOM
(`test/theme-toggle.test.js`). Run it with:

```bash
node test/theme-toggle.test.js
```

It asserts:

- `auto` matches the system on first visit (dark and light),
- a saved explicit choice is honoured over the system,
- an auto-detected first visit is **not** persisted to `localStorage`,
- clicking cycles `auto → dark → light → auto` and persists each explicit choice,
- system changes are followed in `auto` mode but ignored for explicit `dark`/`light`,
- returning to `auto` is persisted (so the user's "follow system" intent sticks),
- the stylesheet `href` is not redundantly re-set (no re-fetch).

## Customising

- To change the default scheme for no-JavaScript / first-visit visitors, adjust
  `color_scheme` in `_config.yml` (the anti-flicker script still overrides it once it
  runs).
- To change the storage key, edit the `STORAGE_KEY` constant in
  `assets/js/theme-toggle.js`.
- The cycle order lives in the `nextMode()` function in `theme-toggle.js`.
- The button colours use the theme's SCSS color variables, so they adapt automatically to
  both schemes — add overrides in the `.theme-toggle` rule in
  `_sass/custom/custom.scss`.
