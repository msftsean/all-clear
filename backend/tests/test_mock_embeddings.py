"""Tests for deterministic mock embeddings + surge fixture integrity (T4a/T4b)."""

import itertools
import json
from collections import defaultdict
from pathlib import Path

from app.services.mock.embeddings import cosine_similarity, embed_text, mock_embed

DEDUP_THRESHOLD = 0.83
_FIXTURE = Path(__file__).parent.parent / "mock_data" / "surge_replay_25.json"


def test_deterministic() -> None:
    assert embed_text("downed power line at oak ave") == embed_text("downed power line at oak ave")


def test_l2_normalized() -> None:
    vec = embed_text("transformer substation explosion blackout")
    norm = sum(v * v for v in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-9


def test_empty_text_is_zero_vector() -> None:
    assert all(v == 0.0 for v in embed_text("the a an to of"))  # all stopwords


def test_near_duplicates_exceed_threshold() -> None:
    a = embed_text("downed power line sparking on fifth and main dangerous wire")
    b = embed_text("downed power line sparking on fifth and main dangerous pavement")
    assert cosine_similarity(a, b) >= DEDUP_THRESHOLD


def test_distinct_signals_below_threshold() -> None:
    a = embed_text("downed power line sparking fifth main street")
    b = embed_text("refund double charge on my monthly bill account")
    assert cosine_similarity(a, b) < DEDUP_THRESHOLD


async def test_async_mock_embed_matches_sync() -> None:
    assert await mock_embed("water main break flooding pine road") == embed_text(
        "water main break flooding pine road"
    )


def test_fixture_clusters_separable_under_threshold() -> None:
    """Each scripted cluster is internally cohesive and externally distinct."""
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    clusters: dict[str, list[list[float]]] = defaultdict(list)
    for s in data["signals"]:
        clusters[s["cluster"]].append(embed_text(s["text"]))

    for name, vecs in clusters.items():
        within = min(cosine_similarity(a, b) for a, b in itertools.combinations(vecs, 2))
        assert within >= DEDUP_THRESHOLD, f"cluster {name} not cohesive: {within:.3f}"

    names = list(clusters)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            cross = max(
                cosine_similarity(a, b)
                for a in clusters[names[i]]
                for b in clusters[names[j]]
            )
            assert cross < DEDUP_THRESHOLD, f"{names[i]} x {names[j]} too similar: {cross:.3f}"


def test_fixture_expected_counts_present() -> None:
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    assert len(data["signals"]) == 25
    assert data["expected"]["max_open_incidents"] == 6
    assert data["expected"]["min_attachments"] == 19
