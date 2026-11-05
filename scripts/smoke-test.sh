#!/usr/bin/env bash
# Offline smoke gate: mock/test backend pytest suite, then frontend unit tests.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Running backend pytest suite (mock/test mode)"
(
  cd "$root/backend"
  ENVIRONMENT=test \
  MOCK_MODE=true \
  USE_MOCK_MODE=true \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=. \
  python -m pytest -q
)

echo "==> Running frontend unit tests"
(
  cd "$root/frontend"
  npm test -- --run
)
