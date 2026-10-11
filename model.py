from typing import Literal
from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    intent: Literal[
        "refund", "replacement", "delivery", "payment", "product_quality", "other"
    ] = Field(description="The customer's main request")

    order_id: str | None = Field(
        default=None,
        description="Order ID if written in the ticket, otherwise null",
    )

    sentiment: Literal["positive", "neutral", "negative"]

    needs_human: bool = Field(
        description="True if legal threats, safety concerns, or the ticket is unclear"
    )

    product_category: Literal["electronics", "clothing", "home", "other"] = Field(
        description="Closest product category, or other if unclear"
    )

    person_hurt: bool = Field(
        description="A person was physically injured or became ill (cut, burn, shock, rash). "
                    "A broken or leaking product on its own does not count."
    )
    legal_or_public_threat: bool = Field(
        description="Customer threatens consumer court, legal action, police, media, or social media"
    )
    contacted_support_before: bool = Field(
        description="Customer says THEY already contacted the company's support "
                    "(emailed, called, complained) and it was not resolved"
    )
    wrong_charge: bool = Field(
        description="Customer was charged twice, charged a wrong amount, "
                    "or a payment failed but money was deducted"
    )
    refund_overdue: bool = Field(
        description="A refund was promised or a return was completed, and the money has not arrived. "
                    "Merely asking for a refund does not count."
    )
    package_lost: bool = Field(
        description="Tracking or the courier says delivered but the customer did not receive it, "
                    "or the package is lost. A late package does not count."
    )
    item_destroyed: bool = Field(
        description="The item arrived broken into pieces, shattered, crushed, or leaked. "
                    "A small dent or scratch does not count."
    )
    asks_about_own_order: bool = Field(
        description="Customer asks a question about an order they placed (cancel, return, change)"
    )

    @property
    def priority(self) -> int:
        if self.person_hurt or self.legal_or_public_threat or self.contacted_support_before:
            return 5
        if self.wrong_charge or self.refund_overdue or self.package_lost or self.item_destroyed:
            return 4
        if self.intent != "other":      # any real order complaint is at least a 3
            return 3
        if self.asks_about_own_order:
            return 2
        return 1