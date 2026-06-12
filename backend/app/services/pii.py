"""PII redaction helpers shared by voice services."""

import re
from typing import Any

_PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    re.compile(r"\b\d{3}[-.]\d{3}[-.]\d{4}\b"),
    re.compile(r"\b\(\d{3}\)\s?\d{3}[-.]\d{4}\b"),
    re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b"),
]

# Context-anchored patterns: only redact when the number is explicitly labeled
# as a student/campus identifier. This avoids clobbering ticket IDs such as
# TKT-IT-20260601-0007 / ESC-MOCK-20260601-0003 which embed an 8-digit date.
# The id body allows an optional letter prefix plus an optional separator before
# 6-10 digits (e.g. "A-1234567", "A 1234567", "12345678").
_STUDENT_ID_PATTERN = re.compile(
    r"\b(student|campus)\s*"
    r"(id(?:entification)?(?:\s*number)?|number|no\.?|#)\s*"
    r"(?:is|:|#|=|of)?\s*"
    r"([A-Za-z][-\s]?)?\d{6,10}\b",
    re.IGNORECASE,
)
_NUMERIC_DOB = r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}"
_MONTH = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)
_TEXT_DOB = rf"{_MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}"
# Date of birth: only when anchored by a DOB/birth label, to avoid eating
# ordinary dates embedded in ticket IDs or knowledge-base content.
_DOB_PATTERN = re.compile(
    r"\b(date of birth|dob|born on|birth\s*date)\s*[:#]?\s*"
    rf"(?:{_NUMERIC_DOB}|{_TEXT_DOB})\b",
    re.IGNORECASE,
)


def redact_pii_text(value: str) -> str:
    """Replace common PII patterns with a safe redaction marker."""
    redacted = value
    redacted = _STUDENT_ID_PATTERN.sub(r"\1 \2 [REDACTED]", redacted)
    redacted = _DOB_PATTERN.sub(r"\1 [REDACTED]", redacted)
    for pattern in _PII_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def redact_pii(value: Any) -> Any:
    """Recursively redact common PII patterns from JSON-like values."""
    if isinstance(value, str):
        return redact_pii_text(value)
    if isinstance(value, list):
        return [redact_pii(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_pii(item) for key, item in value.items()}
    return value
