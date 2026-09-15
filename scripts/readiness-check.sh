#!/bin/bash
# Fast, deterministic workshop readiness check. Runs offline in mock mode.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0
WARNINGS=0

pass() { echo -e "${GREEN}✓ PASS${NC}: $1"; PASSED=$((PASSED + 1)); }
fail() { echo -e "${RED}✗ FAIL${NC}: $1"; FAILED=$((FAILED + 1)); }
warn() { echo -e "${YELLOW}⚠ WARN${NC}: $1"; WARNINGS=$((WARNINGS + 1)); }

run_check() {
  local label="$1"
  shift
  if "$@"; then
    pass "$label"
  else
    fail "$label"
  fi
}

echo "=========================================="
echo "All Clear workshop readiness"
echo "=========================================="
echo "Mode: offline mock; no Azure credentials required"
echo ""

run_check "Python 3.11+ available ($(python --version 2>&1))" bash -c \
  "python - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY"

run_check "Node.js 18+ available ($(node --version 2>&1))" bash -c \
  "node -e \"process.exit(Number(process.versions.node.split('.')[0]) >= 18 ? 0 : 1)\""

cd "$PROJECT_ROOT/backend" || { fail "backend directory exists"; exit 1; }
run_check "Backend imports with installed dependencies" python -c "from app.main import app; print(app.title)"

run_check "Mock incident knowledge search returns evidence" bash -c \
  "MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python - <<'PY'
import asyncio
from app.services.mock.knowledge_service import MockKnowledgeService

async def main():
    results = await MockKnowledgeService().search('downed sparking power line')
    assert results, 'no mock articles returned'
    assert results[0].article_id.startswith('kb-')

asyncio.run(main())
PY"

run_check "In-process /api/health is healthy in mock mode" bash -c \
  "MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app

r = TestClient(app).get('/api/health')
assert r.status_code == 200, r.text
body = r.json()
assert body['status'] == 'healthy'
assert body['mock_mode'] is True
PY"

run_check "Mock signal opens an All Clear incident" bash -c \
  "MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app

r = TestClient(app).post('/api/chat', json={'message': 'Power line down across Main St and sparking'})
assert r.status_code == 200, r.text
body = r.json()
assert body['action']['incident_id'].startswith('AC-'), body
assert body['routing']['outcome'] in {'OPEN_INCIDENT', 'ATTACH_TO_INCIDENT'}
PY"

cd "$PROJECT_ROOT/frontend" || { fail "frontend directory exists"; exit 1; }
if [ -d node_modules ] && [ -d node_modules/react ]; then
  pass "Frontend dependencies installed"
else
  warn "Frontend dependencies missing; run: cd frontend && npm install"
fi

cd "$PROJECT_ROOT" || exit 1
echo ""
echo "=========================================="
echo "Readiness summary"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"

if [ "$FAILED" -eq 0 ]; then
  echo "✅ Workshop-ready: mock pipeline works without Azure credentials."
  echo "Definition of done: backend health is healthy and /api/chat returns an AC-* incident."
  exit 0
fi

echo "❌ Not workshop-ready. Fix failed checks above, then rerun: npm run readiness"
exit 1
