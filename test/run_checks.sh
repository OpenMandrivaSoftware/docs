#!/usr/bin/env bash
# OpenMandriva Documentation - Automated Test and Validation Runner
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== 1/6: Running Ruby validator and generator unit tests ==="
ruby test/test_metadata_validator.rb
ruby test/test_redirect_generator.rb

echo ""
echo "=== 2/6: Validating source document metadata and migration retention ==="
ruby test/validate_metadata.rb --check-migration

echo ""
echo "=== 3/6: Running Python validator unit tests ==="
python3 -m unittest discover -s test -p "test_*.py"

echo ""
echo "=== 4/6: Running theme-toggle JavaScript unit tests ==="
if ! command -v node >/dev/null 2>&1; then
    echo "Error: Node.js is required for running the complete test suite (theme-toggle.test.js)." >&2
    echo "Please install Node.js (18+) or ensure it is in your PATH." >&2
    exit 1
fi

node test/theme-toggle.test.js

echo ""
echo "=== 5/6: Building site with Jekyll (production) ==="
JEKYLL_ENV=production bundle exec jekyll build --trace

echo ""
echo "=== 6/6: Verifying generated site routes, metadata, and assets ==="
python3 test/verify_generated_site.py --site-dir _site
python3 test/check_links.py --site-dir _site

echo ""
echo "All automated checks passed successfully!"
