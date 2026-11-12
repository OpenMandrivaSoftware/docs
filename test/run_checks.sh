#!/usr/bin/env bash
# OpenMandriva Documentation - Automated Test and Validation Runner
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== 1/4: Running Python validator unit tests ==="
python3 -m unittest discover -s test -p "test_*.py"

echo ""
echo "=== 2/4: Running theme-toggle JavaScript unit tests ==="
if command -v node >/dev/null 2>&1; then
    node test/theme-toggle.test.js
else
    echo "Notice: node is not installed; skipping test/theme-toggle.test.js (tested in CI)."
fi

echo ""
echo "=== 3/4: Building site with Jekyll (production) ==="
JEKYLL_ENV=production bundle exec jekyll build --trace

echo ""
echo "=== 4/4: Validating internal links, assets, and anchors ==="
python3 test/check_links.py --site-dir _site

echo ""
echo "All automated checks passed successfully!"
