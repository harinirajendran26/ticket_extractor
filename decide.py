from dataclasses import dataclass
from typing import Literal

from model import TicketAnalysis

Route = Literal["auto_reply", "ask_for_order_id", "human"]

AUTOMATED_INTENTS = {"delivery"}      # allowlist: the only intent we automate for now


@dataclass
class Decision:
    route: Route
    reason: str


def decide(analysis: TicketAnalysis | None, order: dict | None) -> Decision:
    """Choose what happens to a ticket. First matching rule wins."""
    if analysis is None:
        return Decision("human", "analyzer produced no valid result")

    if analysis.priority >= 4:
        return Decision("human", f"priority {analysis.priority}")

    if analysis.needs_human:
        return Decision("human", "analyzer flagged needs_human")

    if analysis.intent not in AUTOMATED_INTENTS:
        return Decision("human", f"intent '{analysis.intent}' is not automated yet")

    if analysis.order_id is None:
        return Decision("ask_for_order_id", "no order ID in the ticket")

    if order is None or "error" in order:
        return Decision("ask_for_order_id", "order not found for this account")

    return Decision("auto_reply", "delivery status question with a valid order")