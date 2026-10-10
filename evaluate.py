from ticket_analysis import analyze

# (ticket text, expected intent, expected priority)
TESTS = [
    ("Order OD123 hasn't arrived in 12 days. This is my third complaint!!", "delivery", 5),
    ("I was charged twice for the same order", "payment", 3),
    ("What are your return timelines?", "other", 1),
    ("The phone screen arrived cracked. I want a replacement.", "replacement", 3),
    ("I will take you to consumer court if this is not fixed today", "other", 5),
]


def evaluate():
    intent_ok = priority_ok = 0
    for text, exp_intent, exp_priority in TESTS:
        result = analyze(text)
        if result is None:
            print(f"FAILED (no valid output): {text!r}")
            continue
        if result.intent == exp_intent:
            intent_ok += 1
        else:
            print(f"INTENT MISS: {text!r}\n   expected={exp_intent} got={result.intent}")
        if result.priority == exp_priority:
            priority_ok += 1
        else:
            print(f"PRIORITY MISS: {text!r}\n   expected={exp_priority} got={result.priority}")

    n = len(TESTS)
    print(f"\nIntent accuracy:   {intent_ok}/{n}")
    print(f"Priority accuracy: {priority_ok}/{n}")


if __name__ == "__main__":
    evaluate()