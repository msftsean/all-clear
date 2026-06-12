"""Prepare the idempotent All Clear hero-board demo.

This script does not mutate incidents or fire LLM-backed signals. It verifies the
live backend's demo fixture and prints the exact blank/loaded frontend URLs for
stage use.

Usage:
  python scripts/seed_demo_board.py
  python scripts/seed_demo_board.py --backend https://... --frontend https://...
"""

from __future__ import annotations

import argparse
import sys

import httpx

DEFAULT_BACKEND = (
    "https://allclear-kt5fw24guxoxy-backend.nicebay-0aac45bb.eastus."
    "azurecontainerapps.io"
)
DEFAULT_FRONTEND = (
    "https://allclear-kt5fw24guxoxy-frontend.nicebay-0aac45bb.eastus."
    "azurecontainerapps.io"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify and print ClearBoard demo URLs.")
    parser.add_argument("--backend", default=DEFAULT_BACKEND, help="Backend base URL")
    parser.add_argument("--frontend", default=DEFAULT_FRONTEND, help="Frontend base URL")
    args = parser.parse_args()

    backend = args.backend.rstrip("/")
    frontend = args.frontend.rstrip("/")
    url = f"{backend}/api/demo/clearboard?mode=loaded"

    try:
        response = httpx.get(url, timeout=20.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"Demo fixture check failed: {exc}", file=sys.stderr)
        return 1

    board = response.json()
    total = int(board["total_signals"])
    incidents = board["incidents"]
    incident_count = len(incidents)
    duplicates = total - incident_count

    print("All Clear hero-board demo is ready.")
    print(f"Readout: {total:,} signals received -> {incident_count} incidents")
    print(f"Collapsed duplicates: {duplicates:,}")
    for incident in incidents:
        print(
            f"  - {incident['incident_id']}: {incident['title']} "
            f"({incident['report_count']:,} reports)"
        )
    print()
    print(f"Blank board:  {frontend}/?demo=blank")
    print(f"Loaded board: {frontend}/?demo=loaded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
