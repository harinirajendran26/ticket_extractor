from decide import decide
from model import TicketAnalysis


def make(**overrides) -> TicketAnalysis:
    base = dict(
        intent="delivery", order_id="OD123", sentiment="neutral", needs_human=False,
        product_category="other", person_hurt=False, legal_or_public_threat=False,
        contacted_support_before=False, wrong_charge=False, refund_overdue=False,
        package_lost=False, item_destroyed=False, asks_about_own_order=False,
    )
    base.update(overrides)
    return TicketAnalysis(**base)


GOOD_ORDER = {"order_id": "OD123", "status": "shipped"}
NOT_FOUND = {"error": "No order with this ID was found for the current account."}

CASES = [
    # (name, analysis, order, expected route)
    ("simple delivery question",   make(),                                  GOOD_ORDER, "auto_reply"),
    ("analyzer failed",            None,                                    None,       "human"),
    ("package lost (priority 4)",  make(package_lost=True),                 GOOD_ORDER, "human"),
    ("legal threat",               make(legal_or_public_threat=True),       GOOD_ORDER, "human"),
    ("model says needs_human",     make(needs_human=True),                  GOOD_ORDER, "human"),
    ("refund request",             make(intent="refund"),                   GOOD_ORDER, "human"),
    ("delivery, no order ID",      make(order_id=None),                     None,       "ask_for_order_id"),
    ("delivery, order not found",  make(),                                  NOT_FOUND,  "ask_for_order_id"),
]

passed = 0
for name, analysis, order, expected in CASES:
    d = decide(analysis, order)
    ok = d.route == expected
    passed += ok
    print(f"{'ok ' if ok else 'FAIL'}  {name:28} -> {d.route:17} ({d.reason})")

print(f"\n{passed}/{len(CASES)} passed")