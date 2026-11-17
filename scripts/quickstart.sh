#!/usr/bin/env bash
# All Clear offline or live quickstart for the canonical incident-response corpus.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python}"
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
mode="live"
run_smoke=true

usage() {
  cat <<'EOF'
Usage: scripts/quickstart.sh [--mock] [--no-smoke] [--help]

  --mock      Run the offline incident pipeline without Azure credentials.
  --no-smoke  Seed the live search index without checking the deployed API.
  --help      Show this help.

Without --mock, seed the Azure AI Search index from the canonical All Clear
incident-response corpus. The live lane requires Azure Search and OpenAI
endpoints plus a Search key (or an authenticated identity for OpenAI).
EOF
}

for arg in "$@"; do
  case "$arg" in
    --help|-h)
      usage
      exit 0
      ;;
    --mock)
      mode="mock"
      ;;
    --no-smoke)
      run_smoke=false
      ;;
    *)
      printf 'Unknown option: %s\n' "$arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$mode" == "mock" ]]; then
  cd "$root/backend"
  MOCK_MODE=true PYTHONPATH=. "$python_bin" - <<'PY'
import asyncio

from app.agents.pipeline import build_mock_pipeline


async def main() -> None:
    result = await build_mock_pipeline().process_signal(
        "A downed power line is sparking at 5th and Main.",
        session_id="quickstart",
    )
    assert result.action.incident_id.startswith("AC-")
    print(f"✅ Scenario-ready — {result.action.incident_id} ({result.action.severity.value})")


asyncio.run(main())
PY
  exit 0
fi

missing=()
[[ -n "${AZURE_SEARCH_ENDPOINT:-}" ]] || missing+=("AZURE_SEARCH_ENDPOINT")
if [[ -z "${AZURE_SEARCH_API_KEY:-}" && -z "${AZURE_SEARCH_KEY:-}" ]]; then
  missing+=("AZURE_SEARCH_API_KEY")
fi
[[ -n "${AZURE_OPENAI_ENDPOINT:-}" ]] || missing+=("AZURE_OPENAI_ENDPOINT")
if (( ${#missing[@]} > 0 )); then
  printf 'Missing required environment variables for the live seed lane:\n' >&2
  printf '  - %s\n' "${missing[@]}" >&2
  printf 'Use --mock for an offline check.\n' >&2
  exit 2
fi

index_name="${AZURE_SEARCH_INDEX_NAME:-${AZURE_SEARCH_INDEX:-knowledge-base}}"
cd "$root"
"$python_bin" scripts/seed_search_index.py --index-name "$index_name"

if [[ "$run_smoke" == false ]]; then
  printf '✅ Scenario-ready — index seeded; deployed API smoke check skipped.\n'
  exit 0
fi

if [[ -z "${AZURE_CONTAINERAPP_URL:-}" ]]; then
  printf 'Missing required environment variable for the deployed API smoke check:\n  - AZURE_CONTAINERAPP_URL\n' >&2
  printf 'Use --no-smoke when seeding before deployment.\n' >&2
  exit 2
fi

"$python_bin" - "$AZURE_CONTAINERAPP_URL" <<'PY'
import sys
from urllib.error import URLError
from urllib.request import urlopen

health_url = sys.argv[1].rstrip("/") + "/api/health"
try:
    with urlopen(health_url, timeout=15) as response:
        if response.status != 200:
            raise SystemExit(f"API health check returned HTTP {response.status}: {health_url}")
except (OSError, URLError) as exc:
    raise SystemExit(f"API health check failed for {health_url}: {exc}") from exc

print(f"✅ Scenario-ready — API health check passed: {health_url}")
PY
