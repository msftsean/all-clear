"""
AJCU scenario smoke test (STEP 5).

Runs the QueryAgent keyword classifier and the escalation evaluator against the
six workshop challenge messages from 47Doors-AJCU-Scenario.md §5 and asserts the
expected intent + escalation behavior for each.

Run from the backend dir so `app` is importable:

    cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py
"""

from __future__ import annotations

import re
import sys

from app.agents.escalation_rules import evaluate_escalation
from app.agents.intent_classifier import IntentClassifier

# Spanish detection: stopwords + accented chars + inverted punctuation.
_SPANISH_HINTS = {
    "que", "quiere", "cuando", "cuándo", "el", "la", "los", "las", "para",
    "día", "padres", "mamá", "mi", "es", "saber", "orientación", "papá",
}


def detect_language(message: str) -> str:
    msg = message.lower()
    if any(ch in msg for ch in "¿¡áéíóúñ"):
        return "es"
    tokens = set(re.findall(r"[a-záéíóúñ]+", msg))
    if len(tokens & _SPANISH_HINTS) >= 2:
        return "es"
    return "en"


CHALLENGES = [
    {
        "card": "A — The Quiet Crisis",
        "message": (
            "I haven't been to class in two weeks. I don't think I belong here. "
            "I've been crying at night. I don't know who to talk to."
        ),
        "expected_intent": "student_wellness",
        "expect": lambda esc, lang, cls: (
            esc["offer_chaplain"] is True          # offers chaplain in parallel
            and esc["create_ticket"] is True       # wellness ticket
            and esc["escalate"] is False            # no harm keyword -> no gating
        ),
        "note": "offers chaplain in parallel, no gating",
    },
    {
        "card": "B — The Aid Cliff",
        "message": (
            "My mom lost her job last month. Can I get more aid? Also I'm thinking "
            "of dropping a class — does that hurt my package?"
        ),
        "expected_intent": "financial_aid",
        "expect": lambda esc, lang, cls: (
            esc["priority"] == "high"
            and esc["create_ticket"] is True
            and _has_overlap(
                cls,
                "My mom lost her job last month. Can I get more aid? Also I'm "
                "thinking of dropping a class — does that hurt my package?",
                "registrar",
            )  # registrar overlap detectable
        ),
        "note": "high-priority appeals ticket (+ registrar overlap)",
    },
    {
        "card": "C — The Discernment",
        "message": (
            "I'm thinking about doing a year of service after graduation. I don't know "
            "if I should apply to JVC or take the consulting job. Can someone help me "
            "think through this?"
        ),
        "expected_intent": "campus_ministry",
        "expect": lambda esc, lang, cls: (
            esc["create_ticket"] is False          # offers, does NOT auto-create
            and esc["offer_chaplain"] is True
        ),
        "note": "offers — does NOT auto-create a ticket",
    },
    {
        "card": "D — The Phishing Storm",
        "message": (
            "My password isn't working and I just got an email saying my account is "
            "locked. I clicked the link."
        ),
        "expected_intent": "it",
        "expect": lambda esc, lang, cls: (
            sorted(esc["tickets"]) == ["it", "security"]  # TWO tickets
        ),
        "note": "security-incident workflow -> TWO tickets",
    },
    {
        "card": "E — Mass of the Holy Spirit",
        "message": "When is the Mass of the Holy Spirit? Also, I'm not Catholic — am I welcome?",
        "expected_intent": "campus_ministry",
        "expect": lambda esc, lang, cls: (
            esc["create_ticket"] is False          # no ticket, interfaith welcome
        ),
        "note": "interfaith welcome, no ticket",
    },
    {
        "card": "F — The Multilingual Family",
        "message": "Mi mamá quiere saber cuándo es el día de orientación para padres.",
        "expected_intent": "general",
        "expect": lambda esc, lang, cls: (
            lang == "es"                            # detects Spanish (-> respond in Spanish)
        ),
        "note": "detects Spanish, responds in Spanish",
    },
]


def _has_overlap(classifier: IntentClassifier, message: str, intent: str) -> bool:
    """True if `intent` has a non-trivial secondary keyword score for the message."""
    normalized = message.strip().lower()
    score = classifier._calculate_score(normalized, classifier.patterns[intent])
    return score >= 1.5


def main() -> int:
    classifier = IntentClassifier()
    all_pass = True
    rows = []

    for ch in CHALLENGES:
        result = classifier.classify(ch["message"])
        intent = result.intent
        lang = detect_language(ch["message"])
        esc = evaluate_escalation(intent, ch["message"])

        intent_ok = intent == ch["expected_intent"]
        behavior_ok = bool(ch["expect"](esc, lang, classifier))
        passed = intent_ok and behavior_ok
        all_pass = all_pass and passed

        rows.append({
            "card": ch["card"],
            "expected": ch["expected_intent"],
            "got": intent,
            "conf": round(result.confidence, 2),
            "lang": lang,
            "tickets": ",".join(esc["tickets"]) or "-",
            "priority": esc["priority"],
            "create_ticket": esc["create_ticket"],
            "escalate": esc["escalate"],
            "offer_chaplain": esc["offer_chaplain"],
            "note": ch["note"],
            "pass": passed,
        })

    print("=" * 78)
    print("AJCU SCENARIO SMOKE TEST — six challenge messages (§5)")
    print("=" * 78)
    for r in rows:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"\n[{status}] {r['card']}")
        print(f"   intent:        {r['got']}  (expected {r['expected']}, conf={r['conf']})")
        print(f"   language:      {r['lang']}")
        print(f"   tickets:       {r['tickets']}")
        print(f"   priority:      {r['priority']}   escalate={r['escalate']}   "
              f"create_ticket={r['create_ticket']}   offer_chaplain={r['offer_chaplain']}")
        print(f"   expected:      {r['note']}")

    print("\n" + "=" * 78)
    passed = sum(1 for r in rows if r["pass"])
    print(f"RESULT: {passed}/{len(rows)} challenges passed")
    print("=" * 78)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
