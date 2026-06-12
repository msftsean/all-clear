#!/bin/bash
# quickstart.sh — Cold-Start Quickstart entry point (feature 006)
#
# One idempotent command that takes a configured environment to "scenario-ready"
# (Labs 01 & 04 effectively done). Also the exact command the azure.yaml
# `postprovision` hook invokes.
#
# Lanes:
#   live (default) : validate env -> seed index -> verify index -> backend smoke
#   --mock         : validate the mock pipeline + backend health, NO Azure creds
#
# Contract: specs/006-quickstart-headstart/contracts/quickstart-cli.md
# Exit codes: 0 scenario-ready | 1 a step failed | 2 pre-flight (missing env/args)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors (match scripts/smoke-test.sh)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓ PASS${NC}: $1"; }
fail() { echo -e "${RED}✗ FAIL${NC}: $1"; }
warn() { echo -e "${YELLOW}⚠ WARN${NC}: $1"; }
info() { echo -e "  ℹ $1"; }

SCENARIOS_LINK="labs/05-agent-orchestration/scenarios/ajcu/README.md"

# Defaults
MOCK=false
NO_SMOKE=false
DATA_DIR="$PROJECT_ROOT/infra/ai-search/seed-articles"

usage() {
  cat <<EOF
quickstart.sh — take a configured environment to "scenario-ready"

Usage:
  scripts/quickstart.sh [--mock] [--no-smoke] [--data-dir <path>] [-h|--help]

Flags:
  --mock              Offline lane. Validate the mock pipeline + backend health.
                      Requires NO Azure credentials.
  --no-smoke          Run seed + verify only; skip the backend smoke check
                      (used by the azd postprovision hook to stay fast/non-fatal).
  --data-dir <path>   Seed corpus directory
                      (default: infra/ai-search/seed-articles).
  -h, --help          Print this help and exit 0.

Required environment (live lane only — not needed with --mock):
  AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY (or AZURE_SEARCH_KEY),
  AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY
  Optional: AZURE_SEARCH_INDEX_NAME (default university-kb),
            AZURE_OPENAI_EMBEDDING_DEPLOYMENT (default text-embedding-ada-002)

Exit codes: 0 scenario-ready | 1 a step failed | 2 missing env / bad args
EOF
}

# ----------------------------------------------------------------------------
# Parse flags
# ----------------------------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --mock) MOCK=true; shift ;;
    --no-smoke) NO_SMOKE=true; shift ;;
    --data-dir)
      if [ $# -lt 2 ]; then fail "--data-dir requires a path"; exit 2; fi
      DATA_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown argument: $1"; echo; usage; exit 2 ;;
  esac
done

echo "=================================================="
echo "47 Doors — Cold-Start Quickstart"
echo "=================================================="
echo ""

# ----------------------------------------------------------------------------
# Success banner — MUST contain the literal marker "✅ Scenario-ready"
# ----------------------------------------------------------------------------
print_banner_live() {
  local index_name="$1" count="$2"
  echo ""
  echo "=================================================="
  echo "✅ Scenario-ready"
  echo "   Index: ${index_name} (${count} articles seeded)"
  echo "   Next:  ${SCENARIOS_LINK}"
  echo "=================================================="
}

print_banner_mock() {
  echo ""
  echo "=================================================="
  echo "✅ Scenario-ready"
  echo "   Mock lane: pipeline validated with no Azure credentials."
  echo "   Next:  ${SCENARIOS_LINK}"
  echo "=================================================="
}

# ----------------------------------------------------------------------------
# Mock lane — no Azure credentials required
# ----------------------------------------------------------------------------
run_mock_lane() {
  echo ">>> Mock lane (USE_MOCK_MODE=true, no Azure required)"
  echo ""
  local rc=0
  cd "$PROJECT_ROOT/backend" || { fail "backend directory not found"; return 1; }

  # 1) Mock LLM intent classification (mirrors smoke-test.sh Section 5)
  if USE_MOCK_MODE=true python -c "
import asyncio
from app.services.mock.llm_service import MockLLMService

async def t():
    svc = MockLLMService()
    r = await svc.classify_intent('I forgot my password')
    assert r.intent == 'password_reset', r.intent
    assert r.confidence > 0.5

asyncio.run(t())
" 2>/dev/null; then
    pass "Mock LLM service (intent classification)"
  else
    fail "Mock LLM service not working"; rc=1
  fi

  # 2) Mock knowledge/KB search
  if USE_MOCK_MODE=true python -c "
import asyncio
from app.services.mock.knowledge_service import MockKnowledgeService

async def t():
    svc = MockKnowledgeService()
    results = await svc.search('password reset')
    assert len(results) > 0

asyncio.run(t())
" 2>/dev/null; then
    pass "Mock knowledge service (KB search)"
  else
    fail "Mock knowledge service not working"; rc=1
  fi

  # 3) Backend /api/health via in-process TestClient (no port, reliable in CI)
  if USE_MOCK_MODE=true python -c "
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
r = c.get('/api/health')
assert r.status_code == 200, r.status_code
assert 'healthy' in r.text or 'ok' in r.text

" 2>/dev/null; then
    pass "Backend /api/health responding (mock mode)"
  else
    fail "Backend /api/health not responding in mock mode"; rc=1
  fi

  cd "$PROJECT_ROOT" || true
  if [ "$rc" -eq 0 ]; then
    print_banner_mock
    return 0
  fi
  echo ""
  fail "Mock lane did not reach scenario-ready."
  return 1
}

# ----------------------------------------------------------------------------
# Live lane — validate env, seed, verify, (smoke)
# ----------------------------------------------------------------------------
validate_live_env() {
  local missing=()
  [ -z "${AZURE_SEARCH_ENDPOINT:-}" ] && missing+=("AZURE_SEARCH_ENDPOINT")
  if [ -z "${AZURE_SEARCH_API_KEY:-}" ] && [ -z "${AZURE_SEARCH_KEY:-}" ]; then
    missing+=("AZURE_SEARCH_API_KEY")
  fi
  [ -z "${AZURE_OPENAI_ENDPOINT:-}" ] && missing+=("AZURE_OPENAI_ENDPOINT")
  [ -z "${AZURE_OPENAI_API_KEY:-}" ] && missing+=("AZURE_OPENAI_API_KEY")

  if [ ${#missing[@]} -gt 0 ]; then
    fail "Missing required environment variable(s) for the live lane:"
    for v in "${missing[@]}"; do
      echo "   - $v"
    done
    info "Set them in your environment / .env, or run with --mock for the offline lane."
    return 2
  fi
  pass "Required live-lane environment present"
  return 0
}

run_live_lane() {
  validate_live_env
  local env_rc=$?
  [ $env_rc -eq 2 ] && return 2

  local index_name="${AZURE_SEARCH_INDEX_NAME:-university-kb}"

  # Step 1: seed index (idempotent upsert)
  echo ""
  echo ">>> Seeding index '${index_name}' from ${DATA_DIR}"
  if python "$SCRIPT_DIR/seed_search_index.py" --data-dir "$DATA_DIR" --index-name "$index_name"; then
    pass "Seed step completed"
  else
    fail "Seed step failed"; return 1
  fi

  # Step 2: verify index (reuse Lab 04 verifier; do not edit it)
  echo ""
  echo ">>> Verifying index"
  if python "$PROJECT_ROOT/labs/04-build-rag-pipeline/verify_index.py"; then
    pass "Verify step completed"
  else
    fail "Verify step failed"; return 1
  fi

  # Step 3: backend smoke (unless --no-smoke)
  if [ "$NO_SMOKE" = true ]; then
    info "Skipping backend smoke check (--no-smoke)"
  else
    echo ""
    echo ">>> Backend smoke check"
    if (cd "$PROJECT_ROOT/backend" && USE_MOCK_MODE=true python -c "
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
r = c.get('/api/health')
assert r.status_code == 200, r.status_code
" 2>/dev/null); then
      pass "Backend /api/health responding"
    else
      fail "Backend smoke check failed"; return 1
    fi
  fi

  # Count seeded articles for the banner (offline; no Azure call).
  local count
  count=$(python "$SCRIPT_DIR/seed_search_index.py" --data-dir "$DATA_DIR" --dry-run 2>/dev/null \
    | grep -Eo '[0-9]+ unique document IDs' | grep -Eo '^[0-9]+' || echo "?")
  print_banner_live "$index_name" "$count"
  return 0
}

# ----------------------------------------------------------------------------
# Dispatch
# ----------------------------------------------------------------------------
if [ "$MOCK" = true ]; then
  run_mock_lane
  exit $?
else
  run_live_lane
  exit $?
fi
