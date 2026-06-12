"""
Test harness for intent_classifier.py.
Evaluates All Clear signal classification accuracy against incident-triage examples.
"""

from intent_classifier import classify_intent

TEST_CASES = [
    ("Power line down across Main St, sparking near a school", "FIELD_HAZARD"),
    ("Water main break flooding the 200 block", "FIELD_HAZARD"),
    ("Tree down and blocked road at Pine and 4th", "FIELD_HAZARD"),
    ("Smell of gas near the community center", "PUBLIC_SAFETY"),
    ("Transformer fire on Oak Ave and people are trapped", "PUBLIC_SAFETY"),
    ("Explosion reported downtown with injured pedestrians", "PUBLIC_SAFETY"),
    ("Whole neighborhood has no power after the transformer blew", "INFRASTRUCTURE_OUTAGE"),
    ("Substation outage affecting the north grid", "INFRASTRUCTURE_OUTAGE"),
    ("Systems offline after the outage surge started", "INFRASTRUCTURE_OUTAGE"),
    ("When will power be restored on Elm St?", "CUSTOMER_INQUIRY"),
    ("How long until crews restore service near Maple Ave?", "CUSTOMER_INQUIRY"),
    ("Can you tell me the ETA for power restored in my area?", "CUSTOMER_INQUIRY"),
    ("I need to schedule a routine meter inspection", "SERVICE_REQUEST"),
    ("Please create a service request for a non-urgent appointment", "SERVICE_REQUEST"),
    ("Need to file the NFIRS report for last night's fire", "COMPLIANCE_REPORT"),
    ("Product recall notification must be filed within the statutory window", "COMPLIANCE_REPORT"),
    ("We have a breach notification reporting deadline today", "COMPLIANCE_REPORT"),
    ("I already reported AC-0042. Any update on the crew ETA?", "STATUS_CHECK"),
    ("What is the incident status for AC-1007?", "STATUS_CHECK"),
    ("This is urgent and I want to talk to a supervisor", "HUMAN_REQUEST"),
    ("Please escalate me to a real person", "HUMAN_REQUEST"),
    ("Hello, thanks for your help", "GENERAL_INQUIRY"),
    ("I am not sure what I need yet", "GENERAL_INQUIRY"),
]


def test_classifier():
    """Return True when classifier accuracy is at least 90%."""
    correct = 0
    failures = []
    for signal, expected in TEST_CASES:
        predicted = classify_intent(signal)
        if predicted == expected:
            correct += 1
            print(f"[PASS] {signal[:60]}...")
        else:
            failures.append((signal, expected, predicted))
            print(f"[FAIL] {signal[:60]}...")
            print(f"       Expected: {expected}, Got: {predicted}")

    total = len(TEST_CASES)
    accuracy = correct / total * 100
    print(f"\n{'=' * 60}")
    print(f"Accuracy: {accuracy:.1f}% ({correct}/{total})")
    print("Goal: 90%+")
    print("SUCCESS! Exceeded 90% accuracy target." if accuracy >= 90 else f"Failures: {failures}")
    print(f"{'=' * 60}\n")
    return accuracy >= 90.0


if __name__ == "__main__":
    raise SystemExit(0 if test_classifier() else 1)
