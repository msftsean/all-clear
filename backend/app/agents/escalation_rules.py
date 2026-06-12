"""
Escalation & routing rules for the AJCU Jesuit scenario.

The ESCALATION_RULES dict below is the verbatim drop-in from
47Doors-AJCU-Scenario.md §4. It encodes cura personalis at the routing layer:

- student_wellness  → urgent on harm signals; ALWAYS create a ticket.
- campus_ministry   → offer, don't auto-create (pastoral relationships are opt-in).
- financial_aid     → high priority on hardship; ALWAYS create a ticket.

`evaluate_escalation()` and the SECURITY_INCIDENT_* constants are additive
runtime helpers (not part of the verbatim §4 dict). They apply the rules to a
message and implement the Challenge D security-incident workflow described in
the scenario card set (one phishing message → two tickets).
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# §4 — Verbatim drop-in from 47Doors-AJCU-Scenario.md
# ---------------------------------------------------------------------------
ESCALATION_RULES = {
    "student_wellness": {
        "auto_escalate_keywords": [
            "harm myself", "kill myself", "end it", "suicide",
            "hurt someone", "abuse", "assault",
        ],
        "priority": "urgent",
        "out_of_hours_response": (
            "If you are in immediate danger, call 911 or the campus "
            "safety line. You can also reach the 988 Suicide & Crisis "
            "Lifeline by calling or texting 988. A counselor will follow "
            "up with you within 24 hours."
        ),
        "always_create_ticket": True,
    },
    "campus_ministry": {
        # Pastoral concerns are never urgent in the clinical sense, but
        # discernment requests deserve a human, not a knowledge article.
        "human_touch_keywords": [
            "discernment", "vocation", "spiritual direction",
            "lost my faith", "grief", "miscarriage", "death of",
        ],
        "priority": "normal",
        "always_create_ticket": False,  # offer, don't auto-create
    },
    "financial_aid": {
        "human_touch_keywords": [
            "appeal", "special circumstances", "lost my job",
            "parent lost their job", "homeless", "evicted",
        ],
        "priority": "high",
        "always_create_ticket": True,
    },
}

# ---------------------------------------------------------------------------
# Additive runtime helpers (Challenge D security-incident workflow + matcher)
# ---------------------------------------------------------------------------

# A click on a malicious link / account-compromise signal fires a parallel
# security-incident workflow in addition to normal IT routing (Challenge D).
SECURITY_INCIDENT_KEYWORDS = [
    "clicked the link",
    "i clicked",
    "phishing",
    "account is locked",
    "my account is locked",
]

# Hardship phrasing varies ("lost my job" vs "my mom lost her job"). This
# regex matches the financial_aid hardship signal regardless of pronoun so the
# verbatim keyword list can stay intact (Challenge B).
_JOB_LOSS_RE = re.compile(r"lost\s+(?:my|her|his|their|the|a)\s+job")


def _matches_any(message: str, keywords: list[str]) -> bool:
    return any(kw in message for kw in keywords)


# Harm signals that MUST escalate regardless of the classified intent
# (scenario §2.2 SAFETY OVERRIDE). The verbatim student_wellness auto-escalate
# list is the scenario source of truth; the runtime safety net augments it with
# additional realistic crisis phrasings WITHOUT mutating the verbatim §4 dict.
_HARM_KEYWORDS = ESCALATION_RULES["student_wellness"]["auto_escalate_keywords"]

# Additional crisis phrasings for the LIVE runtime safety net only. Keyword
# matching is a backstop, NOT the primary detector (the LLM classifier is) —
# but for a crisis it must fail safe and catch common natural phrasings.
_EXTRA_HARM_KEYWORDS = [
    "want to die",
    "wanna die",
    "want to end it",
    "end my life",
    "take my life",
    "ending my life",
    "hurt myself",
    "harm myself",
    "harming myself",
    "cut myself",
    "cutting myself",
    "self harm",
    "self-harm",
    "overdose",
    "no reason to live",
    "don't want to live",
    "do not want to live",
    "can't go on",
    "cannot go on",
    "better off dead",
    "hurt myself or others",
]

_ALL_HARM_KEYWORDS = list(_HARM_KEYWORDS) + _EXTRA_HARM_KEYWORDS

# Light obfuscation-resistance: collapse internal whitespace so evasions like
# "kill my self" still match "kill myself". (Leetspeak / unicode homoglyph
# evasion is NOT covered here — see REDTEAM_FINDINGS.md; production should use
# the LLM classifier, not keywords, as the primary safety detector.)
_WS_RE = re.compile(r"\s+")


def _despace(message: str) -> str:
    return _WS_RE.sub("", message)


def contains_harm_signal(message: str) -> bool:
    """True if the message contains a self-harm / harm-to-others signal.

    Intent-independent: used by the safety net so a mis-classified or
    adversarially spoofed intent can never suppress a crisis escalation.
    """
    msg = (message or "").lower()
    if _matches_any(msg, _ALL_HARM_KEYWORDS):
        return True
    # Despaced comparison catches simple spacing evasions ("kill my self").
    despaced = _despace(msg)
    return any(_despace(kw) in despaced for kw in _ALL_HARM_KEYWORDS)


def evaluate_escalation(intent: str, message: str) -> dict:
    """
    Apply ESCALATION_RULES to a classified message.

    Returns a dict describing the escalation/ticketing behavior:
        {
          "intent": str,            # effective intent after any safety override
          "original_intent": str,   # intent as classified, pre-override
          "safety_override": bool,  # True if a harm signal forced wellness routing
          "escalate": bool,
          "priority": str,
          "create_ticket": bool,
          "offer_chaplain": bool,   # parallel pastoral path (cura personalis)
          "crisis_line": str | None,
          "tickets": list[str],     # departments that receive a ticket
        }
    """
    msg = (message or "").lower()

    # SAFETY OVERRIDE (scenario §2.2): ANY message indicating risk of harm routes
    # to student_wellness with escalate=true, regardless of the classified intent.
    # This closes the intent-spoofing bypass found in red teaming — keyword
    # stuffing can no longer divert a crisis message away from the wellness path.
    original_intent = intent
    harm = contains_harm_signal(message)
    safety_override = harm and intent != "student_wellness"
    if safety_override:
        intent = "student_wellness"

    result: dict = {
        "intent": intent,
        "original_intent": original_intent,
        "safety_override": safety_override,
        "escalate": False,
        "priority": "normal",
        "create_ticket": False,
        "offer_chaplain": False,
        "crisis_line": None,
        "tickets": [],
    }

    if intent == "student_wellness":
        rule = ESCALATION_RULES["student_wellness"]
        result["create_ticket"] = rule["always_create_ticket"]
        result["tickets"].append("student_wellness")
        # Whole-person overlap: always offer a chaplain in parallel, never as a gate.
        result["offer_chaplain"] = True
        if contains_harm_signal(message):
            # Safety override (obfuscation-resistant).
            result["escalate"] = True
            result["priority"] = rule["priority"]  # urgent
            result["crisis_line"] = rule["out_of_hours_response"]
        else:
            # Distress without explicit harm signal: ticket, but no gating.
            result["priority"] = "high"

        # Combined-vector preservation: if the message was ALSO an IT/account
        # compromise (e.g. phishing) before a safety override re-routed it here,
        # still raise the parallel security ticket so it is not silently dropped.
        if safety_override and original_intent == "it" and _matches_any(
            msg, SECURITY_INCIDENT_KEYWORDS
        ):
            result["tickets"].append("security")

    elif intent == "financial_aid":
        rule = ESCALATION_RULES["financial_aid"]
        result["create_ticket"] = rule["always_create_ticket"]
        result["priority"] = rule["priority"]  # high
        result["tickets"].append("financial_aid")
        # human_touch / hardship signals confirm the high-priority appeal.
        if _matches_any(msg, rule["human_touch_keywords"]) or _JOB_LOSS_RE.search(msg):
            result["escalate"] = True

    elif intent == "campus_ministry":
        rule = ESCALATION_RULES["campus_ministry"]
        # Offer, don't auto-create — pastoral relationships are opt-in.
        result["create_ticket"] = rule["always_create_ticket"]  # False
        result["priority"] = rule["priority"]  # normal
        result["offer_chaplain"] = True

    elif intent == "it":
        # Normal IT routing always opens an IT support ticket.
        result["create_ticket"] = True
        result["tickets"].append("it")
        # Challenge D: a click/compromise signal fires a second, parallel
        # security-incident ticket from the same message.
        if _matches_any(msg, SECURITY_INCIDENT_KEYWORDS):
            result["escalate"] = True
            result["priority"] = "high"
            result["tickets"].append("security")

    # general (and any other intent): no automatic escalation or ticket.

    return result
