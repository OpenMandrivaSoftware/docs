// Behaviour tests for assets/js/theme-toggle.js with a mocked DOM.
// Run with:  node test/theme-toggle.test.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function makeContext(opts = {}) {
  const state = {
    theme: opts.theme != null ? opts.theme : null,              // localStorage value ('auto'|'dark'|'light'|null)
    systemDark: opts.systemDark !== undefined ? opts.systemDark : true,
    readyState: opts.readyState || 'complete',
    href: opts.href || '/assets/css/just-the-docs-default.css',
    dataTheme: null,
    dataMode: null,
    appliedHref: [],
  };

  const linkEl = {
    getAttribute: (n) => (n === 'href' ? state.href : null),
    setAttribute: (n, v) => { if (n === 'href') { state.appliedHref.push(v); state.href = v; } },
  };

  const rootEl = {
    _attrs: { 'data-theme-css-base': '/assets/css/just-the-docs-', 'data-theme': null, 'data-mode': null },
    getAttribute: (n) => rootEl._attrs[n] || null,
    setAttribute: (n, v) => { rootEl._attrs[n] = v; if (n === 'data-theme') state.dataTheme = v; if (n === 'data-mode') state.dataMode = v; },
  };

  const btn = {
    _attrs: { 'aria-pressed': 'false', 'aria-label': 'Toggle dark mode' },
    _listeners: {},
    getAttribute: (n) => btn._attrs[n],
    setAttribute: (n, v) => { btn._attrs[n] = v; },
    addEventListener: (type, fn) => { btn._listeners[type] = fn; },
  };

  let changeHandler = null;
  const makeMq = (matches) => ({
    matches: matches,
    addEventListener: (t, fn) => { if (t === 'change') changeHandler = fn; },
    addListener: (fn) => { changeHandler = fn; },
  });

  const localStorageMock = {
    getItem: (k) => (state.theme === null ? null : state.theme),
    setItem: (k, v) => { state.theme = v; },
    removeItem: (k) => { state.theme = null; },
  };

  const documentMock = {
    readyState: state.readyState,
    documentElement: rootEl,
    querySelector: (sel) => (sel === '[rel="stylesheet"]' ? linkEl : null),
    getElementById: (id) => (id === 'theme-toggle' ? btn : null),
    addEventListener: (type, fn) => { if (type === 'DOMContentLoaded') fn(); },
  };

  const sandbox = {
    window: { matchMedia: () => makeMq(state.systemDark) },
    document: documentMock,
    localStorage: localStorageMock,
    setTimeout: () => {},
    console: console,
  };

  return { sandbox, state, btn, linkEl, rootEl, getChangeHandler: () => changeHandler };
}

function loadScript(sandbox) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'assets', 'js', 'theme-toggle.js'), 'utf8');
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
}

let pass = 0;
function test(name, fn) {
  try { fn(); pass++; console.log('  ok - ' + name); }
  catch (e) { console.error('  FAIL - ' + name + '\n    ' + e.message); process.exitCode = 1; }
}
function assert(cond, msg) { if (!cond) throw new Error('ASSERT FAILED: ' + msg); }

console.log('theme-toggle.js (3-state) behavior tests\n');

test('auto on first visit follows a dark system', () => {
  const { sandbox, state } = makeContext({ systemDark: true });
  loadScript(sandbox);
  assert(state.dataMode === 'auto', 'mode auto; got ' + state.dataMode);
  assert(state.dataTheme === 'dark', 'theme dark; got ' + state.dataTheme);
  assert(state.href === '/assets/css/just-the-docs-dark.css', 'href dark; got ' + state.href);
  assert(state.theme === null, 'nothing persisted (auto mode); got ' + state.theme);
});

test('auto on first visit follows a light system', () => {
  const { sandbox, state } = makeContext({ systemDark: false });
  loadScript(sandbox);
  assert(state.dataMode === 'auto', 'mode auto');
  assert(state.dataTheme === 'light', 'theme light');
  assert(state.href === '/assets/css/just-the-docs-light.css', 'href light; got ' + state.href);
  assert(state.theme === null, 'nothing persisted; got ' + state.theme);
});

test('a saved explicit choice is honoured over the system', () => {
  const { sandbox, state } = makeContext({ theme: 'light', systemDark: true });
  loadScript(sandbox);
  assert(state.dataMode === 'light', 'mode light; got ' + state.dataMode);
  assert(state.dataTheme === 'light', 'theme light');
  assert(state.href === '/assets/css/just-the-docs-light.css', 'href light');
});

test('explicit auto is honoured (follows system) and persisted', () => {
  const { sandbox, state } = makeContext({ theme: 'auto', systemDark: true });
  loadScript(sandbox);
  assert(state.dataMode === 'auto', 'mode auto; got ' + state.dataMode);
  assert(state.dataTheme === 'dark', 'theme dark (system)');
  assert(state.theme === 'auto', 'auto persisted; got ' + state.theme);
});

test('clicking cycles auto -> dark -> light -> auto and persists each step', () => {
  const ctx = makeContext({ systemDark: true, readyState: 'loading' });
  loadScript(ctx.sandbox);
  assert(ctx.state.theme === null, 'nothing persisted before any click');
  const click = () => ctx.btn._listeners.click({});

  click(); // auto -> dark
  assert(ctx.state.dataMode === 'dark', '1st click -> dark; got ' + ctx.state.dataMode);
  assert(ctx.state.dataTheme === 'dark', 'theme dark');
  assert(ctx.state.theme === 'dark', 'persisted dark; got ' + ctx.state.theme);
  assert(ctx.btn._attrs['aria-label'] === 'Theme: dark. Switch to light.', 'label: ' + ctx.btn._attrs['aria-label']);

  click(); // dark -> light
  assert(ctx.state.dataMode === 'light', '2nd click -> light; got ' + ctx.state.dataMode);
  assert(ctx.state.dataTheme === 'light', 'theme light');
  assert(ctx.state.theme === 'light', 'persisted light');

  click(); // light -> auto
  assert(ctx.state.dataMode === 'auto', '3rd click -> auto; got ' + ctx.state.dataMode);
  assert(ctx.state.dataTheme === 'dark', 'auto follows dark system; got ' + ctx.state.dataTheme);
  assert(ctx.state.theme === 'auto', 'explicit auto persisted; got ' + ctx.state.theme);

  click(); // auto -> dark (fixed cycle, not opposite-of-system)
  assert(ctx.state.dataMode === 'dark', '4th click -> dark; got ' + ctx.state.dataMode);
});

test('system change is followed while in auto mode', () => {
  const ctx = makeContext({ systemDark: true, readyState: 'loading' });
  loadScript(ctx.sandbox);
  assert(ctx.state.dataTheme === 'dark', 'starts dark');
  const handler = ctx.getChangeHandler();
  assert(!!handler, 'change handler captured');
  handler({ matches: false }); // system flips to light
  assert(ctx.state.dataMode === 'auto', 'still auto; got ' + ctx.state.dataMode);
  assert(ctx.state.dataTheme === 'light', 'follows system to light; got ' + ctx.state.dataTheme);
  assert(ctx.state.href === '/assets/css/just-the-docs-light.css', 'href light after system change');
  assert(ctx.state.theme === null, 'auto-detect not persisted; got ' + ctx.state.theme);
});

test('system change ignored after an explicit dark or light choice', () => {
  const ctx = makeContext({ theme: 'light', systemDark: true, readyState: 'loading' });
  loadScript(ctx.sandbox);
  assert(ctx.state.theme === 'light', 'starts with explicit light saved');
  const handler = ctx.getChangeHandler();
  handler({ matches: true }); // system flips to dark — must be ignored
  assert(ctx.state.dataMode === 'light', 'stays light; got ' + ctx.state.dataMode);
  assert(ctx.state.dataTheme === 'light', 'light wins over dark system');
});

test('system change is followed again once back in auto mode', () => {
  const ctx = makeContext({ systemDark: true, readyState: 'loading' });
  loadScript(ctx.sandbox);
  ctx.btn._listeners.click({});      // auto -> dark (explicit, persisted)
  assert(ctx.state.theme === 'dark', 'pinned dark');
  const handler = ctx.getChangeHandler();
  handler({ matches: false });       // system light — ignored (explicit)
  assert(ctx.state.dataTheme === 'dark', 'stays dark despite light system');
  ctx.btn._listeners.click({});      // dark -> light
  ctx.btn._listeners.click({});      // light -> auto (back to auto)
  assert(ctx.state.theme === 'auto', 'back to auto');
  handler({ matches: false });       // now system light is followed
  assert(ctx.state.dataTheme === 'light', 'follows light system again; got ' + ctx.state.dataTheme);
});

test('does not re-trigger stylesheet fetch when theme unchanged', () => {
  const ctx = makeContext({ theme: 'dark', systemDark: true });
  loadScript(ctx.sandbox);
  assert(ctx.state.appliedHref.length <= 1, 'avoid redundant href set; got ' + ctx.state.appliedHref.length);
});

console.log('\n' + pass + ' test(s) passed.');
