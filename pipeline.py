import re
from dataclasses import dataclass

from decide import decide, Decision
from lookup import get_order_status
from ticket_analysis import analyze
from tickets import init_tickets_table, save_ticket, count_previous_tickets

ORDER_ID_PATTERN = re.compile(r"\bOD\d{3,}\b", re.IGNORECASE)

STATUS_TEXT = {
    "placed":    "has been placed and is being prepared for dispatch",
    "shipped":   "has been shipped and is on its way to you",
    "delivered": "is marked as delivered in our records",
    "cancelled": "was cancelled",
}

# Safety net, not NLP: phrases saying the customer did not receive the package.
# Used ONLY to add escalation, and only when our records say "delivered".
NON_RECEIPT_PHRASES = [
    "never received", "not received", "didn't receive", "did not receive",
    "haven't received", "have not received", "never got", "didn't get",
    "did not get", "never arrived", "not arrived", "not delivered",
    "never delivered", "nahi mila", "nahi aaya",
]

init_tickets_table()      # safe to run every time (CREATE TABLE IF NOT EXISTS)


@dataclass
class Result:
    route: str
    reason: str
    reply: str                 # message for the customer (always set)
    handoff_note: dict | None  # summary for the support agent (None when no human is needed)
    flags: list                # true flags, for debugging on every route


def extract_order_id(text: str) -> str | None:
    """Find an order ID by its fixed format. Code does this, not the LLM."""
    match = ORDER_ID_PATTERN.search(text)
    return match.group(0).upper() if match else None


def disputes_delivery(order: dict | None, text: str) -> bool:
    """True if our records say 'delivered' but the customer says they did not get it."""
    if not order or order.get("status") != "delivered":
        return False
    t = text.lower().replace("\u2019", "'")      # normalise curly apostrophes
    return any(phrase in t for phrase in NON_RECEIPT_PHRASES)


def build_reply(decision: Decision, order: dict | None) -> str:
    """Customer-facing text. Facts come from the order record, never from the LLM."""
    if decision.route == "auto_reply":
        status = STATUS_TEXT.get(order["status"], f"is currently: {order['status']}")
        return (f"Your order {order['order_id']} ({order['product']}) {status}. "
                f"It was placed on {order['ordered_on']}.")

    if decision.route == "ask_for_order_id":
        if order is None:    # the customer gave no order ID
            return ("Could you please send your order ID? "
                    "You can find it in your confirmation email.")
        return ("We couldn't find that order on your account. "
                "Please check the order ID and send it again.")

    return ("Thanks for reaching out. A support agent will review your ticket "
            "and get back to you.")


def process_ticket(ticket_text: str, customer_id: str) -> Result:
    analysis = analyze(ticket_text)
    order_id = extract_order_id(ticket_text)

    # Memory lives in the database, not in the model.
    # Count BEFORE saving, or this ticket would count itself.
    previous = count_previous_tickets(customer_id, order_id) if order_id else 0

    if analysis is not None:
        analysis.order_id = order_id                        # code is the source of truth
        analysis.contacted_support_before = previous > 0    # a database fact replaces the guess

    order = None
    if analysis is not None and order_id:
        # Only the ID comes from the ticket. OUR code supplies who the customer is.
        order = get_order_status(order_id, current_customer_id=customer_id)

    # Guard: records say delivered, customer says not received. Only ever sets True.
    if analysis is not None and disputes_delivery(order, ticket_text):
        analysis.package_lost = True

    decision = decide(analysis, order)
    reply = build_reply(decision, order)

    save_ticket(customer_id, order_id, ticket_text, decision.route, decision.reason)

    true_flags = []
    if analysis is not None:
        true_flags = [k for k, v in analysis.model_dump().items()
                      if v is True and k != "needs_human"]

    if decision.route == "human":
        note = {
            "reason": decision.reason,
            "intent": analysis.intent if analysis else None,
            "priority": analysis.priority if analysis else None,
            "order_id": order_id,
            "previous_tickets": previous,
            "flags": true_flags,
            "ticket": ticket_text,
        }
        return Result("human", decision.reason, reply, note, true_flags)

    return Result(decision.route, decision.reason, reply, None, true_flags)