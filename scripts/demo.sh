#!/bin/bash
# demo.sh — One-command live-demo launcher for the 47 Doors front-door agent.
#
# Boots BOTH halves of the demo in MOCK MODE (zero Azure credentials) and waits
# until they are healthy, so a presenter never has to juggle two terminals:
#   - backend  : FastAPI (uvicorn) on :8000  with MOCK_MODE=true
#   - frontend : Vite dev server on :5173    (proxies /api -> :8000)
#
# In mock mode the crisis-safety net, intent routing, ticketing, KB, and PII
# redaction all work offline; voice self-hides (no Azure Realtime deployment).
#
# Usage:
#   ./scripts/demo.sh            # start backend + frontend, wait for health, print URLs
#   ./scripts/demo.sh --check    # also fire the crisis smoke check through the UI proxy
#   ./scripts/demo.sh --backend  # backend only
#
# Stop everything with Ctrl-C (both child processes are cleaned up on exit).
# Exit codes: 0 ok | 1 a service failed to come up | 2 bad args / missing deps

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors (match scripts/quickstart.sh / smoke-test.sh)
if [ -t 1 ]; then
  RED=$'\033[0;31m'; GRN=$'\033[0;32m'; YLW=$'\033[0;33m'; BLU=$'\033[0;34m'; BLD=$'\033[1m'; RST=$'\033[0m'
else
  RED=""; GRN=""; YLW=""; BLU=""; BLD=""; RST=""
fi
say()  { echo "${BLU}▸${RST} $*"; }
ok()   { echo "${GRN}✓${RST} $*"; }
warn() { echo "${YLW}⚠${RST} $*"; }
die()  { echo "${RED}✗ $*${RST}" >&2; exit "${2:-1}"; }

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
HOST="${DEMO_HOST:-127.0.0.1}"

RUN_FRONTEND=true
RUN_CHECK=false
for arg in "$@"; do
  case "$arg" in
    --backend) RUN_FRONTEND=false ;;
    --check)   RUN_CHECK=true ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) die "unknown argument: $arg (try --help)" 2 ;;
  esac
done

BACKEND_PID=""
FRONTEND_PID=""
cleanup() {
  echo
  say "Shutting down demo…"
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
  [ -n "$BACKEND_PID" ]  && kill "$BACKEND_PID"  2>/dev/null
  wait 2>/dev/null
  ok "Stopped."
}
trap cleanup INT TERM EXIT

# --- pre-flight ---------------------------------------------------------------
command -v uvicorn >/dev/null 2>&1 || die "uvicorn not found — run: cd backend && pip install -r requirements.txt" 2
$RUN_FRONTEND && { command -v npm >/dev/null 2>&1 || die "npm not found — install Node.js 18+" 2; }
[ -d "$PROJECT_ROOT/frontend/node_modules" ] || warn "frontend/node_modules missing — first run may take a minute (npm install)"

wait_for_health() {
  local url="$1" name="$2" tries="${3:-40}"
  for ((i=1; i<=tries; i++)); do
    if curl -fsS "$url" >/dev/null 2>&1; then ok "$name healthy ($url)"; return 0; fi
    sleep 0.5
  done
  return 1
}

# --- backend ------------------------------------------------------------------
say "Starting backend (mock mode) on :${BACKEND_PORT} …"
(
  cd "$PROJECT_ROOT/backend" || exit 1
  MOCK_MODE=true PYTHONPATH=. exec uvicorn app.main:app --host "$HOST" --port "$BACKEND_PORT"
) &
BACKEND_PID=$!
wait_for_health "http://${HOST}:${BACKEND_PORT}/api/health" "Backend" 40 \
  || die "backend did not become healthy on :${BACKEND_PORT}"

# --- frontend -----------------------------------------------------------------
if $RUN_FRONTEND; then
  say "Starting frontend (Vite dev) on :${FRONTEND_PORT} …"
  (
    cd "$PROJECT_ROOT/frontend" || exit 1
    exec npm run dev -- --host "$HOST" --port "$FRONTEND_PORT"
  ) &
  FRONTEND_PID=$!
  wait_for_health "http://${HOST}:${FRONTEND_PORT}/" "Frontend" 60 \
    || die "frontend did not come up on :${FRONTEND_PORT}"
fi

# --- optional crisis smoke check ---------------------------------------------
if $RUN_CHECK; then
  say "Crisis smoke check through the UI proxy…"
  base="http://${HOST}:${FRONTEND_PORT}"; $RUN_FRONTEND || base="http://${HOST}:${BACKEND_PORT}"
  resp="$(curl -fsS -X POST "${base}/api/chat" -H 'Content-Type: application/json' \
           -d '{"message":"I want to kill myself"}' 2>/dev/null)"
  if echo "$resp" | grep -q '"escalated": *true' && echo "$resp" | grep -q '988'; then
    ok "Crisis safety net fired (escalated=true, 988 lifeline present)."
  else
    warn "Crisis check did not match expected escalation — inspect manually:"
    echo "$resp" | head -c 300; echo
  fi
fi

# --- ready --------------------------------------------------------------------
echo
echo "${BLD}${GRN}47 Doors demo is live (mock mode).${RST}"
$RUN_FRONTEND && echo "  ${BLD}Open:${RST}  http://${HOST}:${FRONTEND_PORT}"
echo "  API:   http://${HOST}:${BACKEND_PORT}/api/health"
echo "  Try:   type ${BLD}\"I want to kill myself\"${RST} → expect a human escalation + 988 lifeline."
$RUN_FRONTEND && [ -n "${CODESPACE_NAME:-}" ] && \
  warn "Codespaces: make port ${BACKEND_PORT} visibility correct and leave VITE_API_BASE_URL empty (see README)."
echo "  ${YLW}Ctrl-C to stop.${RST}"
echo

# Keep the script alive while the servers run.
wait
