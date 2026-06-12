"""
Deterministic mock embeddings for All Clear (001-maf-rehost, T4a).

A pure, offline EmbeddingFn twin of OpenAIEmbeddingClient. Maps text to a fixed-dim
L2-normalized bag-of-words hash vector, so cosine similarity tracks token overlap:
near-duplicate surge signals exceed DEDUP_THRESHOLD (default 0.83) while distinct
signals fall well below it. No Azure dependency, so the dedup demo and the lab's
threshold-tuning exercise run fully offline (Constitution Art. V.1).
"""

from __future__ import annotations

import hashlib
import math
import re

_DIM = 512

_STOPWORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be", "been",
        "to", "of", "in", "on", "at", "by", "for", "with", "from", "into", "this", "that",
        "it", "its", "my", "our", "your", "their", "we", "i", "you", "they", "he", "she",
        "there", "here", "have", "has", "had", "do", "does", "did", "will", "would",
        "can", "could", "should", "please", "im", "ive", "me", "us", "as", "so", "if",
        "about", "just", "now", "any", "get", "got", "out", "up", "down", "off",
    }
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return [
        t
        for t in _TOKEN_RE.findall(text.lower())
        if len(t) >= 3 and t not in _STOPWORDS
    ]


def _hash_dim(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % _DIM


def embed_text(text: str) -> list[float]:
    """Deterministic, L2-normalized bag-of-words hash embedding."""
    vec = [0.0] * _DIM
    tokens = _tokens(text)
    for tok in tokens:
        vec[_hash_dim(tok)] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0.0:
        return vec
    return [v / norm for v in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors."""
    return sum(x * y for x, y in zip(a, b))


async def mock_embed(text: str) -> list[float]:
    """Async EmbeddingFn entry point injected into RouterExecutor in mock mode."""
    return embed_text(text)
