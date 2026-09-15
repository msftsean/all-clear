#!/bin/bash
# Smoke Test Script for All Clear
# Quick validation that the environment is set up correctly.
# Run time: ~2-3 minutes after dependencies are installed.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    FAILED=$((FAILED + 1))
}

warn() {
    echo -e "${YELLOW}⚠ WARN${NC}: $1"
    WARNINGS=$((WARNINGS + 1))
}

info() {
    echo -e "  ℹ $1"
}

echo "=========================================="
echo "All Clear - Smoke Test Suite"
echo "=========================================="
echo ""

# ==========================================
# Section 1: Environment Check
# ==========================================
echo ">>> Section 1: Environment Check"
echo ""

# Python version
if python --version 2>&1 | grep -q "3.1[1-9]"; then
    pass "Python 3.11+ installed ($(python --version 2>&1))"
else
    fail "Python 3.11+ required (found: $(python --version 2>&1))"
fi

# Node version
if node --version 2>&1 | grep -q "v1[89]\|v2[0-9]"; then
    pass "Node.js 18+ installed ($(node --version))"
else
    fail "Node.js 18+ required (found: $(node --version 2>&1))"
fi

# npm
if command -v npm &> /dev/null; then
    pass "npm available ($(npm --version))"
else
    fail "npm not found"
fi

echo ""

# ==========================================
# Section 2: Dependencies Check
# ==========================================
echo ">>> Section 2: Dependencies Check"
echo ""

# Backend dependencies
cd "$PROJECT_ROOT/backend"
if python -c "import fastapi, pydantic, openai" 2>/dev/null; then
    pass "Backend Python packages installed"
else
    fail "Backend Python packages missing - run: pip install -r requirements.txt"
fi

# Frontend dependencies
cd "$PROJECT_ROOT/frontend"
if [ -d "node_modules" ] && [ -d "node_modules/react" ]; then
    pass "Frontend npm packages installed"
else
    fail "Frontend npm packages missing - run: npm install"
fi

# Playwright (optional but recommended)
if npx playwright --version &>/dev/null; then
    pass "Playwright available for E2E tests"
else
    warn "Playwright not installed - E2E tests will be skipped"
    info "Install with: npx playwright install --with-deps chromium"
fi

echo ""

# ==========================================
# Section 3: Backend Unit Tests
# ==========================================
echo ">>> Section 3: Backend Unit Tests (Critical)"
echo ""

cd "$PROJECT_ROOT/backend"

# Run a subset of critical tests that exists in the All Clear repo.
echo "Running critical backend tests..."
TEST_OUTPUT=$(MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python -m pytest \
    tests/test_pipeline_e2e.py tests/test_routes.py tests/test_router_no_llm.py -q --tb=short 2>&1)
TEST_RC=$?
echo "$TEST_OUTPUT" | tail -10
if [ "$TEST_RC" -eq 0 ]; then
    pass "Backend incident pipeline tests passing"
else
    fail "Backend incident pipeline tests failing"
fi

echo ""

# ==========================================
# Section 4: Backend API Health
# ==========================================
echo ">>> Section 4: Backend API Health"
echo ""

cd "$PROJECT_ROOT/backend"

# Check if port 8000 is already in use
if lsof -i:8000 &>/dev/null || netstat -an 2>/dev/null | grep -q ":8000.*LISTEN"; then
    info "Port 8000 already in use, testing existing server..."
    BACKEND_RUNNING=true
else
    BACKEND_RUNNING=false
fi

# Start backend if not running
if [ "$BACKEND_RUNNING" = false ]; then
    info "Starting backend server..."
    MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python -m uvicorn app.main:app --port 8000 &
    BACKEND_PID=$!
    sleep 5
fi

# Test health endpoint
if curl -s http://localhost:8000/api/health | grep -q "healthy\|ok"; then
    pass "Backend /api/health endpoint responding"
else
    fail "Backend /api/health not responding"
fi

# Test OpenAPI docs
if curl -s http://localhost:8000/api/docs | grep -q "swagger\|openapi"; then
    pass "Backend /api/docs (OpenAPI) available"
else
    warn "Backend /api/docs not available"
fi

# Cleanup
if [ "$BACKEND_RUNNING" = false ] && [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null || true
fi

echo ""

# ==========================================
# Section 5: Mock Mode Validation
# ==========================================
echo ">>> Section 5: Mock Mode Validation"
echo ""

cd "$PROJECT_ROOT/backend"

# Test deterministic mock classifier
if MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python -c "
from app.agents.schemas import SignalCategory
from app.services.mock.maf_chat_client import classify_signal

r = classify_signal('Power line down and sparking near Main Street')
assert r.intent_category is SignalCategory.FIELD_HAZARD
assert r.intent == 'report_field_hazard'
assert r.confidence > 0.5
" 2>/dev/null; then
    pass "Mock classifier working (intent classification)"
else
    fail "Mock classifier not working"
fi

# Test mock knowledge service
if MOCK_MODE=true USE_MOCK_MODE=true ENVIRONMENT=test python -c "
from app.services.mock.knowledge_service import MockKnowledgeService
import asyncio

async def test():
    service = MockKnowledgeService()
    results = await service.search('downed sparking power line')
    assert len(results) > 0
    return True

asyncio.run(test())
" 2>/dev/null; then
    pass "Mock knowledge service working (KB search)"
else
    warn "Mock knowledge service may have issues"
fi

echo ""

# ==========================================
# Section 6: Lab Files Check
# ==========================================
echo ">>> Section 6: Lab Files Check"
echo ""

cd "$PROJECT_ROOT"

# Check critical lab directories for the 180-minute spine.
LABS=("00-setup" "01-understanding-agents" "05-agent-orchestration")

for lab in "${LABS[@]}"; do
    if [ -d "labs/$lab" ] && [ -f "labs/$lab/README.md" ]; then
        pass "Lab $lab structure present"
    else
        fail "Lab $lab missing or incomplete"
    fi
done

# Check solution files for key labs
if [ -f "labs/04-build-rag-pipeline/solution/search_tool.py" ]; then
    pass "Lab 04 solution code present"
else
    warn "Lab 04 solution code missing"
fi

if [ -f "labs/05-agent-orchestration/solution/pipeline.py" ]; then
    pass "Lab 05 solution code present"
else
    warn "Lab 05 solution code missing"
fi

echo ""

# ==========================================
# Summary
# ==========================================
echo "=========================================="
echo "Smoke Test Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}=========================================="
    echo "All critical checks passed!"
    echo "Environment is ready for the All Clear workshop."
    echo -e "==========================================${NC}"
    exit 0
else
    echo -e "${RED}=========================================="
    echo "Some checks failed. Please fix issues above"
    echo "before starting the boot camp."
    echo -e "==========================================${NC}"
    exit 1
fi
