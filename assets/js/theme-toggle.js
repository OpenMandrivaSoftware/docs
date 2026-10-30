/*!
 * Color-scheme toggle for the OpenMandriva docs (three-state: auto / dark / light).
 *
 * Wires up the `#theme-toggle` button rendered in `header_custom.html`. Behaviour:
 *   - "auto"  : follows the visitor's OS `prefers-color-scheme` preference,
 *               updates live as it changes, and is the default on first visit.
 *   - "dark"  : explicit dark theme; saved so it wins over the system.
 *   - "light" : explicit light theme; saved so it wins over the system.
 *
 * Clicking cycles `auto -> dark -> light -> auto`. Only explicit (dark/light) choices
 * — and an explicit return to auto — are persisted to localStorage; an auto-detected
 * first visit is applied but NOT saved, so the site keeps following the system.
 *
 * The stylesheet is swapped the way the theme's own `jtd.setTheme()` does, by updating
 * the `href` of the first `[rel="stylesheet"]` link in the document.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'theme';
  var ROOT = document.documentElement;
  var CSS_BASE_FALLBACK = '/assets/css/just-the-docs-';

  // aria-labels describe the current mode and hint at the next on click.
  var LABELS = {
    auto:  'Theme: auto (follows system). Switch to dark.',
    dark:  'Theme: dark. Switch to light.',
    light: 'Theme: light. Switch to auto.'
  };

  function getCssBase() {
    var base = ROOT.getAttribute('data-theme-css-base');
    return base || CSS_BASE_FALLBACK;
  }

  function getStylesheet() {
    return document.querySelector('[rel="stylesheet"]');
  }

  // Raw stored value: 'auto', 'dark', 'light', or null (never chosen).
  function getSavedMode() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function followSystem() {
    try {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch (e) {
      return 'dark';
    }
  }

  function resolveTheme(mode) {
    if (mode === 'dark' || mode === 'light') {
      return mode;
    }
    // 'auto' or null -> follow the OS preference right now.
    return followSystem();
  }

  function appliesExplicitMode() {
    var m = getSavedMode();
    return m === 'dark' || m === 'light';
  }

  // Apply the resolved theme + mode to the live page. Persists via `persist`.
  function applyTheme(theme, mode, persist) {
    ROOT.setAttribute('data-theme', theme);
    ROOT.setAttribute('data-mode', mode);

    var css = getStylesheet();
    if (css) {
      var href = getCssBase() + theme + '.css';
      // Only touch the href when it changes; re-setting the same value can make
      // the browser re-fetch the stylesheet.
      if (css.getAttribute('href') !== href) {
        css.setAttribute('href', href);
      }
    }

    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, mode);
      } catch (e) {
        // Ignore: storage is unavailable (e.g. private browsing).
      }
    }
  }

  function updateButton(btn, mode) {
    var m = mode || ROOT.getAttribute('data-mode') || 'auto';
    btn.setAttribute('aria-label', LABELS[m]);
    btn.setAttribute('aria-pressed', m === 'auto' ? 'false' : 'true');
  }

  // Fixed cycle: auto -> dark -> light -> auto.
  function nextMode(mode) {
    if (mode === 'dark') return 'light';
    if (mode === 'light') return 'auto';
    return 'dark';
  }

  function init() {
    var saved = getSavedMode();
    var mode = (saved === 'auto' || saved === 'dark' || saved === 'light') ? saved : 'auto';
    var theme = resolveTheme(mode);

    // Apply without persisting: an auto-detected first visit must stay "auto"
    // so the site keeps following the system.
    applyTheme(theme, mode, false);

    var btn = document.getElementById('theme-toggle');
    if (!btn) {
      return;
    }

    btn.addEventListener('click', function () {
      var current = ROOT.getAttribute('data-mode') || 'auto';
      var next = nextMode(current);
      applyTheme(resolveTheme(next), next, true); // explicit choice -> persist
      updateButton(btn, next);
    });

    updateButton(btn, mode);

    // Follow the OS preference while in auto mode.
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var handler = function (e) {
      if (appliesExplicitMode()) {
        return; // explicit dark/light choice takes priority
      }
      applyTheme(e.matches ? 'dark' : 'light', 'auto', false);
      updateButton(btn, 'auto');
    };

    if (typeof mq.addEventListener === 'function') {
      mq.addEventListener('change', handler);
    } else if (typeof mq.addListener === 'function') {
      mq.addListener(handler);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
