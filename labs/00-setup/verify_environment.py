#!/usr/bin/env python3
"""
Environment verification script for the All Clear boot camp.

Checks all required tools and configurations are in place before starting.
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def run_command(command: list[str], timeout: int = 30) -> tuple[bool, str, str]:
    """
    Run a command and return (success, stdout, stderr).

    Args:
        command: Command and arguments as a list
        timeout: Maximum seconds to wait for command

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=(sys.platform == "win32"),  # Shell needed on Windows for some commands
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except FileNotFoundError:
        return False, "", "Command not found"
    except Exception as e:
        return False, "", str(e)


def check_python_version() -> tuple[str, str, bool]:
    """Check Python version is >= 3.11."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 11:
        return "pass", f"Python {version_str}", True
    else:
        return "fail", f"Python {version_str} (need >= 3.11)", False


def check_node_version() -> tuple[str, str, bool]:
    """Check Node.js version is >= 18."""
    success, stdout, stderr = run_command(["node", "--version"])

    if not success:
        return "fail", "Node.js not found - install from https://nodejs.org/", False

    # Parse version like "v18.17.0"
    match = re.match(r"v?(\d+)\.(\d+)\.(\d+)", stdout)
    if match:
        major = int(match.group(1))
        version_str = stdout.lstrip("v")
        if major >= 18:
            return "pass", f"Node.js {version_str}", True
        else:
            return "fail", f"Node.js {version_str} (need >= 18)", False

    return "warn", f"Node.js version unknown: {stdout}", False


def check_azure_cli() -> tuple[str, str, bool]:
    """Check Azure CLI is installed and user is logged in."""
    # First check if az is installed
    success, stdout, stderr = run_command(["az", "--version"])
    if not success:
        return "fail", "Azure CLI not found - install from https://aka.ms/installazurecliwindows", False

    # Parse version from output
    version_match = re.search(r"azure-cli\s+(\d+\.\d+\.\d+)", stdout)
    version_str = version_match.group(1) if version_match else "unknown"

    # Check if logged in
    success, stdout, stderr = run_command(["az", "account", "show"])
    if not success:
        return "fail", f"Azure CLI {version_str} (not logged in - run 'az login')", False

    # Parse account info
    try:
        account = json.loads(stdout)
        user = account.get("user", {}).get("name", "unknown")
        return "pass", f"Azure CLI {version_str} (logged in as {user})", True
    except json.JSONDecodeError:
        return "warn", f"Azure CLI {version_str} (logged in)", True


def check_azd() -> tuple[str, str, bool]:
    """Check Azure Developer CLI is installed."""
    success, stdout, stderr = run_command(["azd", "version"])

    if not success:
        return "fail", "azd not found - install from https://aka.ms/azd-install", False

    # Parse version like "azd version 1.5.0 (commit abc123)"
    match = re.search(r"(\d+\.\d+\.\d+)", stdout)
    version_str = match.group(1) if match else stdout

    return "pass", f"azd {version_str}", True


def check_docker() -> tuple[str, str, bool]:
    """Check Docker is installed and running."""
    # Check if docker command exists
    success, stdout, stderr = run_command(["docker", "--version"])
    if not success:
        return "fail", "Docker not found - install Docker Desktop", False

    # Check if Docker daemon is running
    success, stdout, stderr = run_command(["docker", "info"], timeout=10)
    if not success:
        if "permission denied" in stderr.lower():
            return "fail", "Docker installed but permission denied (add user to docker group)", False
        elif "cannot connect" in stderr.lower() or "error during connect" in stderr.lower():
            return "fail", "Docker installed but not running (start Docker Desktop)", False
        else:
            return "fail", f"Docker not responding: {stderr[:100]}", False

    return "pass", "Docker Desktop running", True


def _project_root() -> Path:
    """Return the repository root."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent


def _read_env_file(env_path: Path) -> dict[str, str]:
    """Read a simple KEY=VALUE dotenv file."""
    env_vars = {}
    if not env_path.exists():
        return env_vars
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def check_local_env_file() -> tuple[str, str, bool]:
    """Check local/mock env posture without requiring Azure secrets."""
    env_path = _project_root() / "backend" / ".env"
    env_vars = _read_env_file(env_path)

    if not env_path.exists():
        return "warn", "backend/.env not found; post-create or npm run reset:workshop will create it", True

    mock_mode = env_vars.get("MOCK_MODE") or os.environ.get("MOCK_MODE")
    use_mock_mode = env_vars.get("USE_MOCK_MODE") or os.environ.get("USE_MOCK_MODE")
    environment = env_vars.get("ENVIRONMENT") or os.environ.get("ENVIRONMENT")

    if _truthy(mock_mode) or _truthy(use_mock_mode) or environment == "test":
        return "pass", "backend/.env is configured for local/mock first success", True

    return "warn", "backend/.env is not mock-mode; set MOCK_MODE=true for Lab 00", True


def check_azure_env_file() -> tuple[str, str, bool]:
    """Check live Azure env variables for the optional facilitator path."""
    env_path = _project_root() / "backend" / ".env"
    env_vars = {**_read_env_file(env_path), **os.environ}

    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_KEY",
        "ADMIN_API_TOKEN",
    ]

    optional_vars = [
        "AZURE_COSMOS_ENDPOINT",
        "AZURE_COSMOS_KEY",
        "PHONE_WEBHOOK_SECRET",
        "PHONE_CALLBACK_BASE_URL",
    ]

    missing = [var for var in required_vars if not env_vars.get(var)]

    if missing:
        return "fail", f"live Azure env missing {', '.join(missing)}", False

    missing_optional = [var for var in optional_vars if not env_vars.get(var)]
    if missing_optional:
        return "warn", f"Azure env ready; optional unset: {', '.join(missing_optional)}", True

    return "pass", "backend/.env configured for live Azure facilitator path", True


def check_health_endpoint() -> tuple[str, str, bool]:
    """Check if backend health endpoint is reachable."""
    import urllib.request
    import urllib.error

    url = "http://localhost:8000/api/health"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                return "pass", "Backend /api/health responding", True
            else:
                return "warn", f"Backend returned status {response.status}", False
    except urllib.error.URLError:
        return "skip", "Health check skipped (backend not running)", True
    except Exception as e:
        return "skip", f"Health check skipped ({str(e)[:50]})", True


def print_result(status: str, message: str) -> None:
    """Print a check result with appropriate icon."""
    icons = {
        "pass": "\u2705",  # Green check
        "fail": "\u274c",  # Red X
        "warn": "\u26a0\ufe0f",   # Warning
        "skip": "\u23ed\ufe0f",   # Skip
    }
    icon = icons.get(status, "\u2753")  # Question mark for unknown
    print(f"{icon}  {message}")


def main() -> int:
    """Run all environment checks and report results."""
    parser = argparse.ArgumentParser(description="All Clear environment verification")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--local", action="store_true", help="credential-free local/mock preflight")
    mode.add_argument("--azure", action="store_true", help="facilitator live Azure preflight")
    args = parser.parse_args()

    azure_mode = args.azure
    mode_label = "Azure facilitator preflight" if azure_mode else "Local mock preflight"

    print(f"\nAll Clear Boot Camp - {mode_label}\n")
    print("=" * 50)
    print()

    checks = [
        ("Python", check_python_version),
        ("Node.js", check_node_version),
        ("Environment File", check_local_env_file),
        ("Health Endpoint", check_health_endpoint),
    ]
    if azure_mode:
        checks = [
            ("Python", check_python_version),
            ("Node.js", check_node_version),
            ("Azure CLI", check_azure_cli),
            ("Azure Developer CLI", check_azd),
            ("Docker", check_docker),
            ("Environment File", check_azure_env_file),
            ("Health Endpoint", check_health_endpoint),
        ]

    results = []
    for name, check_func in checks:
        try:
            status, message, passed = check_func()
            results.append((status, passed))
            print_result(status, message)
        except Exception as e:
            results.append(("fail", False))
            print_result("fail", f"{name}: Unexpected error - {str(e)[:50]}")

    print()
    print("=" * 50)

    # Calculate summary
    total = len(results)
    passed = sum(1 for status, p in results if p)
    failed = sum(1 for status, p in results if status == "fail")

    print()
    if failed == 0:
        print(f"Ready for {mode_label.lower()}! ({passed}/{total} checks passed)")
        return 0
    else:
        print(f"Some issues found ({passed}/{total} checks passed)")
        print("\nPlease resolve the failed checks before proceeding.")
        print("Run this script again after fixing issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
