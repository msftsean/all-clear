#!/bin/bash
# Backward-compatible entry point for Lab 00 validation.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/readiness-check.sh"
