"""Offline citation-contract check for the Lab 04 local knowledge corpus."""

from __future__ import annotations

import re
import sys

from verify_index import _keyword_search, _load_local_corpus

NO_MATCH_ANSWER = "No source record covers this question; escalate to a person."

QUESTIONS = (
    (
        "What should field-operations do for a rotten-egg gas odor near a meter?",
        "field-operations",
    ),
    (
        "What should customer-comms say in a life-safety acknowledgment?",
        "customer-comms",
    ),
    (
        "Which statutory-clock source applies to breach-notification and recall reporting?",
        "compliance-desk",
    ),
)


def answer_from_local_corpus(
    corpus: list[dict[str, object]], question: str
) -> tuple[str, list[dict[str, object]]]:
    sources = _keyword_search(corpus, question, top=3)
    if not sources:
        return NO_MATCH_ANSWER, []

    answer = "Relevant source records: " + " ".join(
        f"{source['title']} [{number}]"
        for number, source in enumerate(sources, start=1)
    )
    return answer, sources


def verify_citation_contract() -> None:
    corpus = _load_local_corpus()
    assert corpus, "The local knowledge corpus is empty."
    corpus_article_ids = {record.get("article_id") for record in corpus}

    for question, expected_queue in QUESTIONS:
        answer, sources = answer_from_local_corpus(corpus, question)
        assert sources, f"No sources returned for: {question}"

        markers = re.findall(r"\[(\d+)\]", answer)
        assert markers, f"No citation markers returned for: {question}"
        for marker in markers:
            source_number = int(marker)
            assert 1 <= source_number <= len(sources), (
                f"[{marker}] does not map to a source for: {question}"
            )
            source = sources[source_number - 1]
            for field in ("article_id", "title", "url"):
                assert source.get(field), (
                    f"[{marker}] source is missing {field} for: {question}"
                )
            assert source["article_id"] in corpus_article_ids, (
                f"[{marker}] cites a source outside the corpus for: {question}"
            )

        assert any(source.get("queue") == expected_queue for source in sources), (
            f"Expected queue {expected_queue!r} is absent from sources for: {question}"
        )

    no_match_answer, no_match_sources = answer_from_local_corpus(
        corpus, "Orbital quantum axolotl melody zorb?"
    )
    assert no_match_answer == NO_MATCH_ANSWER, (
        f"Unexpected no-match answer: {no_match_answer!r}"
    )
    assert not no_match_sources, "The no-match question returned source records."


if __name__ == "__main__":
    try:
        verify_citation_contract()
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print("PASS: offline citation contract and no-match behavior")
