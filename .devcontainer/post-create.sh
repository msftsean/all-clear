#!/bin/bash
# Post-create setup for the All Clear hands-on lab (GitHub Codespaces / dev container).
#
# Portable by design: the repo root is derived from this script's own location, so it
# works no matter what the workspace folder is named. (The previous version hardcoded
# /workspaces/47doors and aborted the whole setup under `set -e`.)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo " Setting up the All Clear lab environment"
echo " Repo root: $REPO_ROOT"
echo "=========================================="

# --- Backend dependencies (installed into the container Python; no venv needed) -
echo ""
echo ">>> Installing backend dependencies..."
cd "$REPO_ROOT/backend" || { echo "ERROR: backend/ not found"; exit 1; }
pip install --upgrade pip
pip install -r requirements.txt

# --- Frontend dependencies ---------------------------------------------------
echo ""
echo ">>> Installing frontend dependencies..."
cd "$REPO_ROOT/frontend" || { echo "ERROR: frontend/ not found"; exit 1; }
npm install

# --- Playwright browser (E2E) — optional; never fail setup -------------------
echo ""
echo ">>> Installing Playwright browser (chromium) for E2E tests..."
npx playwright install --with-deps chromium || echo "WARN: Playwright browser install skipped (E2E is optional)."

# --- Environment files: mock mode by default (runs fully offline) ------------
echo ""
echo ">>> Creating .env files (MOCK MODE — no Azure credentials required)..."
cd "$REPO_ROOT/backend"
if [ ! -f .env ]; then
  cp .env.example .env && echo "Created backend/.env from .env.example (MOCK_MODE=true)."
fi
cd "$REPO_ROOT/frontend"
if [ ! -f .env ]; then
  cp .env.example .env && echo "Created frontend/.env (VITE_API_BASE_URL empty -> Vite proxies /api to backend)."
fi

# --- Verify ------------------------------------------------------------------
echo ""
echo ">>> Verifying installation..."
echo "Python: $(python --version 2>&1)  |  Node: $(node --version)  |  npm: $(npm --version)"
cd "$REPO_ROOT/backend"
if python -c "from app.main import app" 2>/dev/null; then
  echo "Backend imports: OK"
else
  echo "WARN: backend import check failed — re-run: cd backend && pip install -r requirements.txt"
fi

echo ""
echo "=========================================="
echo " Setup complete — All Clear is ready (mock mode, offline)."
echo "=========================================="
echo ""
echo "Quick start (two terminals):"
echo "  cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo "  cd frontend && npm run dev"
echo ""
echo "Verify the offline pipeline (no Azure):"
echo "  cd backend && MOCK_MODE=true PYTHONPATH=. python -m pytest tests/ -q"
echo "  npm run smoke-test"
echo ""
echo "Labs: start at labs/00-setup, then labs/01-understanding-agents -> labs/05-agent-orchestration."
echo ""
