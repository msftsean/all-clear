"""
Intent classifier for a Jesuit university's Universal Front Door support system.

AJCU scenario taxonomy (see 47Doors-AJCU-Scenario.md §1). Classifies student
queries into 6 mission-aligned intent categories:
- financial_aid: Cost, scholarships, aid packages, billing, work-study
- registrar: Registration, transcripts, enrollment, course changes, graduation
- campus_ministry: Liturgy, sacraments, retreats, chaplaincy, service & immersion,
  interfaith life, discernment & vocation
- it: Accounts, passwords, Wi-Fi, devices, learning systems
- student_wellness: Mental health, medical, crisis, accessibility, basic needs
- general: Anything else; mission and student-life questions

Campus Ministry and Student Wellness are first-class peers to IT and the
Registrar, reflecting cura personalis at a Jesuit institution.
"""

from dataclasses import dataclass
from typing import Literal

# Intent type - 6 Jesuit-context categories (AJCU scenario)
IntentType = Literal[
    "financial_aid",
    "registrar",
    "campus_ministry",
    "it",
    "student_wellness",
    "general",
]


@dataclass
class ClassificationResult:
    """Result of intent classification with confidence score."""

    intent: IntentType
    confidence: float


# Negation words that reduce keyword weights when they precede keywords
NEGATION_WORDS = {
    "not",
    "no",
    "don't",
    "doesn't",
    "didn't",
    "won't",
    "can't",
    "cannot",
    "couldn't",
    "never",
    "neither",
    "nor",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
}

# Negation discount factor: multiply keyword weight by this when negated
NEGATION_DISCOUNT = 0.2


# Weighted keyword patterns for each intent category
# Higher weights = stronger signals
INTENT_PATTERNS: dict[IntentType, dict[str, float]] = {
    "financial_aid": {
        # Strong indicators (3.0)
        "financial aid": 3.0,
        "more aid": 3.0,
        "fafsa": 3.0,
        "scholarship": 3.0,
        "magis grant": 3.0,
        # Medium indicators (2.0-2.5)
        "work-study": 2.5,
        "work study": 2.5,
        "aid package": 2.5,
        "special circumstances": 2.5,
        "appeal my aid": 2.5,
        "tuition": 2.0,
        "payment plan": 2.0,
        "bursar": 2.0,
        "billing": 2.0,
        "my package": 2.0,
        # Weak indicators (1.0-1.5)
        "grant": 1.5,
        "loan": 1.5,
        "package": 1.5,
        "aid": 1.0,
    },
    "registrar": {
        # Strong indicators (3.0)
        "transcript": 3.0,
        "add/drop": 3.0,
        "register for class": 3.0,
        "cross-registration": 3.0,
        # Medium indicators (2.0-2.5)
        "drop a class": 2.5,
        "dropping a class": 2.5,
        "withdrawal": 2.5,
        "withdraw": 2.5,
        "declare a minor": 2.5,
        "change my major": 2.5,
        "graduation application": 2.5,
        "degree audit": 2.5,
        "drop deadline": 2.5,
        "registration": 2.0,
        "enroll": 2.0,
        "course change": 2.0,
        # Weak indicators (1.0)
        "graduate": 1.0,
    },
    "campus_ministry": {
        # Strong indicators (3.0)
        "chaplain": 3.0,
        "campus ministry": 3.0,
        "mass": 3.0,
        "holy spirit": 3.0,
        "retreat": 3.0,
        "discernment": 3.0,
        "vocation": 3.0,
        "spiritual direction": 3.0,
        "year of service": 3.0,
        "service after graduation": 3.0,
        "jvc": 3.0,
        "interfaith": 3.0,
        # Medium indicators (2.0-2.5)
        "sacrament": 2.5,
        "reconciliation": 2.5,
        "ignatian": 2.5,
        "spiritual exercises": 2.5,
        "immersion": 2.0,
        "ministry": 2.0,
        # Weak indicators (1.0-1.5)
        "faith": 1.5,
        "prayer": 1.5,
        "catholic": 1.0,
    },
    "it": {
        # Strong indicators (3.0)
        "password": 3.0,
        "reset my password": 3.0,
        "can't log in": 3.0,
        "cannot log in": 3.0,
        "account is locked": 3.0,
        "locked out": 3.0,
        "wifi": 3.0,
        "wi-fi": 3.0,
        "eduroam": 3.0,
        "phishing": 3.0,
        "clicked the link": 3.0,
        "canvas": 3.0,
        # Medium indicators (2.0-2.5)
        "log in": 2.5,
        "login": 2.5,
        "mfa": 2.5,
        "two-factor": 2.5,
        "loaner laptop": 2.5,
        # Weak indicators (1.0-1.5)
        "email": 1.5,
        "locked": 1.5,
        "account": 1.0,
    },
    "student_wellness": {
        # Strong indicators (3.0)
        "counseling": 3.0,
        "counselor": 3.0,
        "therapy": 3.0,
        "mental health": 3.0,
        "crisis": 3.0,
        "crying": 3.0,
        "crying at night": 3.0,
        "don't belong": 3.0,
        "don't think i belong": 3.0,
        "panic": 3.0,
        "self-harm": 3.0,
        "harm myself": 3.0,
        "kill myself": 3.0,
        "suicide": 3.0,
        # Medium indicators (2.0-2.5)
        "anxiety": 2.5,
        "anxious": 2.5,
        "depressed": 2.5,
        "depression": 2.5,
        "overwhelmed": 2.5,
        "can't sleep": 2.5,
        "don't know who to talk to": 2.5,
        "food pantry": 2.5,
        "basic needs": 2.5,
        "belong here": 2.0,
        "accommodation": 2.0,
        "accessibility": 2.0,
        "wellness": 2.0,
    },
    "general": {
        # Mission, orientation, and student-life catch-all
        "what does jesuit": 3.0,
        "jesuit education": 3.0,
        "cura personalis": 3.0,
        "men and women for others": 3.0,
        "parent orientation": 3.0,
        # Spanish-language orientation signals (Challenge F)
        "día de orientación": 3.0,
        "orientación": 3.0,
        "padres": 2.0,
        # English orientation / mission
        "orientation": 2.5,
        "service-learning": 2.5,
        "find my advisor": 2.5,
        "magis": 2.0,
        "mission": 1.5,
    },
}


class IntentClassifier:
    """
    Intent classifier for student support queries.

    Uses weighted keyword matching to classify queries into 6 intent categories.
    """

    def __init__(self, confidence_threshold: float = 0.5):
        """
        Initialize the classifier.

        Args:
            confidence_threshold: Minimum score difference to avoid 'general'
        """
        self.confidence_threshold = confidence_threshold
        self.patterns = INTENT_PATTERNS

    def classify(self, text: str) -> ClassificationResult:
        """
        Classify a student query into an intent category.

        Args:
            text: The student's question or request

        Returns:
            ClassificationResult with intent and confidence score
        """
        # Handle null/empty input
        if text is None or not isinstance(text, str):
            return ClassificationResult(intent="general", confidence=0.3)

        normalized = text.strip().lower()
        if not normalized:
            return ClassificationResult(intent="general", confidence=0.3)

        # Calculate scores for each intent
        scores: dict[IntentType, float] = {}
        for intent, patterns in self.patterns.items():
            scores[intent] = self._calculate_score(normalized, patterns)

        # Find the top two intents
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = sorted_intents[0]
        second_intent, second_score = sorted_intents[1] if len(sorted_intents) > 1 else (None, 0)

        # If top score is too low, default to general
        if top_score < 1.5:
            return ClassificationResult(intent="general", confidence=0.4)

        # If scores are too close (ambiguous), fall back to general
        score_gap = top_score - second_score
        if score_gap < self.confidence_threshold and top_score < 3.0:
            if top_intent != "general":
                return ClassificationResult(intent="general", confidence=0.5)

        # Calculate confidence based on score magnitude and gap
        confidence = min(0.95, 0.5 + (top_score / 10) + (score_gap / 5))

        return ClassificationResult(intent=top_intent, confidence=confidence)

    def _calculate_score(self, text: str, patterns: dict[str, float]) -> float:
        """Calculate weighted score for a set of patterns, with negation handling."""
        score = 0.0
        for pattern, weight in patterns.items():
            if pattern in text:
                # Check if this keyword is negated
                if self._is_negated(text, pattern):
                    # Apply negation discount
                    score += weight * NEGATION_DISCOUNT
                else:
                    score += weight
        return score

    def _is_negated(self, text: str, keyword: str) -> bool:
        """
        Check if a keyword appears in a negation context.
        
        Returns True if keyword is preceded by a negation word within 5 words.
        """
        # Find position of keyword in text
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return False
        
        # Extract text before keyword (up to 20 chars to cover ~5 words)
        start_pos = max(0, keyword_pos - 20)
        context_before = text[start_pos:keyword_pos]
        
        # Check for negation words in context
        words_before = context_before.split()
        for word in words_before[-5:]:  # Check last 5 words before keyword
            if word in NEGATION_WORDS:
                return True
        
        return False


# Convenience function for simple usage
def classify_intent(query: str) -> IntentType:
    """
    Classify a student query into one of 6 intent categories.

    Args:
        query: The student's question or request

    Returns:
        The classified intent category
    """
    classifier = IntentClassifier()
    result = classifier.classify(query)
    return result.intent
