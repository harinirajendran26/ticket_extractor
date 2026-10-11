import json
from pathlib import Path
from ticket_analysis import analyze

# (ticket text, expected intent, expected priority)

TESTS = [
    ("My package says delivered, but I haven't received anything. I've checked with my neighbors too.", "delivery", 4),
    ("I paid through UPI, but the payment failed and the money was deducted from my bank account.", "payment", 4),
    ("The shoes I received are two sizes smaller than what I ordered. I need an exchange.", "replacement", 3),
    ("I've been waiting for my refund for 15 days, and customer support keeps giving me the same answer.", "refund", 5),
    ("The delivery person marked my order as attempted, but nobody even called me.", "delivery", 3),
    ("I received a completely different product from the one shown in the pictures.", "product_quality", 3),
    ("Your website charged me twice, and I need the extra amount refunded immediately.", "payment", 4),
    ("Can I return a shirt if I removed the tag but haven't worn it?", "other", 2),
    ("This is ridiculous! My order was supposed to arrive last week, and nobody is helping me. I want a resolution NOW!", "delivery", 5),
    ("The headphones I bought stopped working after just two days. I want a replacement or my money back.", "replacement", 3),
    ("I accidentally placed two orders. How can I cancel one before it gets shipped?", "other", 2),
    ("My order status has been stuck on 'processing' for six days without any update.", "delivery", 3),
    ("I was promised a refund after the seller cancelled my order, but I still haven't received it.", "refund", 4),
    ("If you don't resolve this issue today, I will file a formal consumer complaint and share my experience publicly.", "other", 5),
    ("The glass bottle arrived shattered, and the liquid has leaked all over the other items in the package.", "product_quality", 4),
]

import json
from pathlib import Path

LAST_RUN = Path("last_run.json")


def evaluate():
    previous = json.loads(LAST_RUN.read_text()) if LAST_RUN.exists() else {}
    current = {}
    intent_ok = priority_ok = 0

    for i, (text, exp_intent, exp_priority) in enumerate(TESTS, 1):
        result = analyze(text)
        if result is None:
            print(f"#{i:02d} FAILED (no valid output)")
            current[str(i)] = "FAILED"
            continue
        i_pass = result.intent == exp_intent
        p_pass = result.priority == exp_priority
        intent_ok += i_pass
        priority_ok += p_pass
        status = ("ok " if i_pass else "INT") + " " + ("ok " if p_pass else "PRI")
        if not p_pass:
            print("   flags:", result.model_dump(exclude={"intent", "order_id", "sentiment", "product_category", "needs_human"}))
        print(f"#{i:02d} {status}  got {result.intent}/{result.priority}  "
              f"(want {exp_intent}/{exp_priority})  needs_human={result.needs_human}")
        current[str(i)] = f"{result.intent}/{result.priority}"

    changed = [k for k in current if k in previous and current[k] != previous[k]]
    if changed:
        print("\nChanged since last run:", ", ".join("#" + k.zfill(2) for k in changed))

    n = len(TESTS)
    print(f"\nIntent accuracy:   {intent_ok}/{n}")
    print(f"Priority accuracy: {priority_ok}/{n}")
    LAST_RUN.write_text(json.dumps(current))

if __name__ == "__main__":
    evaluate()