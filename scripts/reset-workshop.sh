#!/bin/bash
# Reset local workshop state to a clean mock-mode posture without deleting source.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "All Clear workshop reset"
echo "Repo: $PROJECT_ROOT"
echo ""

backup_env() {
  local file="$1"
  if [ -f "$file" ]; then
    mv "$file" "$file.backup-$STAMP"
    echo "Backed up $(basename "$(dirname "$file")")/$(basename "$file")"
  fi
}

backup_env "$PROJECT_ROOT/backend/.env"
cp "$PROJECT_ROOT/backend/.env.example" "$PROJECT_ROOT/backend/.env"
echo "Reset backend/.env to mock-mode defaults"

backup_env "$PROJECT_ROOT/frontend/.env"
cp "$PROJECT_ROOT/frontend/.env.example" "$PROJECT_ROOT/frontend/.env"
echo "Reset frontend/.env to proxy-safe defaults"

rm -rf \
  "$PROJECT_ROOT/backend/.pytest_cache" \
  "$PROJECT_ROOT/backend/.ruff_cache" \
  "$PROJECT_ROOT/backend/htmlcov" \
  "$PROJECT_ROOT/backend/.coverage" \
  "$PROJECT_ROOT/frontend/dist" \
  "$PROJECT_ROOT/.pytest_cache"

echo "Removed local build/test caches"
echo ""
echo "Restart any running backend/frontend terminals, then run:"
echo "  npm run readiness"
echo "  npm run quickstart:mock"
