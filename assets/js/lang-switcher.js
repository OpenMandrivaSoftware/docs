(function() {
  'use strict';

  function initDropdown() {
    var dropdown = document.querySelector('.lang-switcher .dropdown');
    if (!dropdown) return;

    var toggle = dropdown.querySelector('.dropdown-toggle');
    var menu = dropdown.querySelector('.dropdown-menu');
    if (!toggle || !menu) return;

    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var isOpen = menu.classList.contains('show');
      menu.classList.toggle('show', !isOpen);
      toggle.setAttribute('aria-expanded', !isOpen);
    });

    document.addEventListener('click', function(e) {
      if (!dropdown.contains(e.target)) {
        menu.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDropdown);
  } else {
    initDropdown();
  }
})();
