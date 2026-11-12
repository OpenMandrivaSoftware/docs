#!/usr/bin/env bash
# OpenMandriva Documentation - Automated Test and Validation Runner
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== 1/4: Running Python validator unit tests ==="
python3 -m unittest discover -s test -p "test_*.py"

echo ""
echo "=== 2/4: Running theme-toggle JavaScript unit tests ==="
if ! command -v node >/dev/null 2>&1; then
    for candidate in \
        "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin" \
        "/usr/lib/chatgpt/resources/cua_node/bin"
    do
        if [ -x "$candidate/node" ]; then
            export PATH="$candidate:$PATH"
            break
        fi
    done
fi

if ! command -v node >/dev/null 2>&1; then
    echo "Error: Node.js is required for running the complete test suite (theme-toggle.test.js)." >&2
    echo "Please install Node.js (18+) or ensure it is in your PATH." >&2
    exit 1
fi

node test/theme-toggle.test.js

echo ""
echo "=== 3/4: Building site with Jekyll (production) ==="
JEKYLL_ENV=production bundle exec jekyll build --trace

echo ""
echo "=== 4/4: Validating internal links, assets, and anchors ==="
python3 test/check_links.py --site-dir _site

echo ""
echo "All automated checks passed successfully!"
