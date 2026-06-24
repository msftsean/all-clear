"""
Lab 04 - Verify All Clear Knowledge Data

In live mode this script verifies the Azure AI Search index. In MOCK_MODE=true,
or when Azure Search settings are absent, it verifies the local data/*.json
knowledge corpus so first-time participants can run the lab offline.
"""

from __future__ import annotations

import json
import os
import sys
import io
from pathlib import Path
from typing import Any

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is optional for local verification
    load_dotenv = None

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "00-setup"))

# Load environment variables from Lab 00 setup
env_path = Path(__file__).parent.parent / "00-setup" / ".env"
if load_dotenv is not None:
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # Try current directory


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _search_config() -> tuple[str | None, str | None, str]:
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_API_KEY") or os.getenv("AZURE_SEARCH_KEY")
    index_name = (
        os.getenv("AZURE_SEARCH_INDEX")
        or os.getenv("AZURE_SEARCH_INDEX_NAME")
        or "allclear-kb"
    )
    return endpoint, api_key, index_name


def _load_local_corpus() -> list[dict[str, Any]]:
    corpus: list[dict[str, Any]] = []
    data_dir = Path(__file__).parent / "data"
    for data_file in sorted(data_dir.glob("*.json")):
        records = json.loads(data_file.read_text(encoding="utf-8"))
        for record in records:
            record["_source_file"] = data_file.name
            corpus.append(record)
    return corpus


def _keyword_search(corpus: list[dict[str, Any]], query: str, top: int = 3) -> list[dict[str, Any]]:
    terms = [term.lower() for term in query.replace("-", " ").split() if len(term) > 2]
    scored: list[tuple[int, dict[str, Any]]] = []
    for record in corpus:
        haystack = " ".join(
            str(record.get(field, ""))
            for field in ("title", "content", "snippet", "category", "queue")
        ).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:top]]


def verify_local_corpus(reason: str) -> bool:
    """Verify the mock/local knowledge corpus."""
    print(f"Mock/local verification: {reason}")
    print()

    corpus = _load_local_corpus()

    print("Test 1: Local Document Count")
    print("-" * 40)
    if len(corpus) >= 15:
        print(f"✅ Found {len(corpus)} local knowledge records")
    else:
        print(f"❌ Only found {len(corpus)} local records (expected at least 15)")
        return False
    print()

    print("Test 2: All Clear Keyword Search")
    print("-" * 40)
    results = _keyword_search(corpus, "downed power line", top=3)
    if results:
        print("✅ Local keyword search working!")
        print("   Top results for 'downed power line':")
        for record in results:
            print(f"   - {record.get('title', 'Unknown')}")
    else:
        print("❌ Local keyword search returned no results")
        return False
    print()

    print("Test 3: Category Filter")
    print("-" * 40)
    field_hazard_records = [r for r in corpus if r.get("category") == "field_hazard"]
    if field_hazard_records:
        print("✅ Filtering by category working!")
        print(f"   Found {len(field_hazard_records)} field_hazard articles")
    else:
        print("❌ No results for category eq 'field_hazard'")
        return False
    print()

    print("=" * 60)
    print("✅ Mock-mode knowledge verification complete!")
    print("=" * 60)
    print()
    return True


def verify_azure_index(endpoint: str, api_key: str, index_name: str) -> bool:
    """Verify the pre-indexed Azure AI Search data."""
    try:
        from azure.core.credentials import AzureKeyCredential
        from azure.search.documents import SearchClient
    except ImportError as exc:
        print(f"❌ Azure Search SDK not installed: {exc}")
        print('   Install lab dependencies or run with MOCK_MODE=true for offline verification.')
        return False

    print(f"Search Endpoint: {endpoint}")
    print(f"Index Name: {index_name}")
    print()

    try:
        client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )

        print("Test 1: Document Count")
        print("-" * 40)
        all_results = list(client.search(search_text="*", top=100))
        doc_count = len(all_results)

        if doc_count >= 15:
            print(f"✅ Found {doc_count} documents in index")
        else:
            print(f"⚠️  Only found {doc_count} documents (expected at least 15)")
        print()

        print("Test 2: Keyword Search")
        print("-" * 40)
        query_results = list(client.search(search_text="downed power line", top=3))

        if query_results:
            print("✅ Keyword search working!")
            print("   Top results for 'downed power line':")
            for result in query_results:
                print(f"   - {result.get('title', 'Unknown')}")
        else:
            print("❌ Keyword search returned no results")
            return False
        print()

        print("Test 3: Vector Field Check")
        print("-" * 40)
        if query_results and "content_vector" in query_results[0]:
            print("✅ Vector embeddings are present")
        else:
            print("✅ Index accessible (vector field not in default select)")
        print()

        print("Test 4: Category Filter")
        print("-" * 40)
        field_results = list(
            client.search(search_text="*", filter="category eq 'field_hazard'", top=3)
        )

        if field_results:
            print("✅ Filtering by category working!")
            print(f"   Found {len(field_results)} field_hazard articles")
        else:
            print("⚠️  No results for category eq 'field_hazard'")
        print()

        print("=" * 60)
        print("✅ Index verification complete!")
        print("=" * 60)
        print()
        print("You're ready to start Step 4: Implement the Search Tool")
        print()
        return True

    except Exception as e:
        print(f"❌ Error connecting to Azure AI Search: {e}")
        return False


def verify_index() -> bool:
    """Verify Azure AI Search when configured, otherwise verify the mock corpus."""
    print("=" * 60)
    print("Lab 04 - Verify All Clear Knowledge Data")
    print("=" * 60)
    print()

    endpoint, api_key, index_name = _search_config()
    if _truthy(os.getenv("MOCK_MODE")):
        return verify_local_corpus("MOCK_MODE=true")
    if not endpoint or not api_key:
        return verify_local_corpus(
            "Azure Search env vars not present; using offline data/*.json corpus"
        )
    return verify_azure_index(endpoint, api_key, index_name)


if __name__ == "__main__":
    success = verify_index()
    sys.exit(0 if success else 1)
