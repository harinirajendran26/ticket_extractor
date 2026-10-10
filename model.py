from typing import Literal
from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    intent: Literal[
        "refund", "replacement", "delivery", "payment", "product_quality", "other"
    ] = Field(description="The customer's main request")

    order_id: str | None = Field(
        default=None,
        description="Order ID if mentioned in the ticket, otherwise null",
    )

    priority: int = Field(
        ge=1, le=5,
        description="1 = general question, 3 = normal problem, 5 = urgent",
    )

    sentiment: Literal["positive", "neutral", "negative"]

    needs_human: bool = Field(
        description="True if legal threats, safety concerns, or the ticket is unclear"
    )

    product_category: Literal["electronics", "clothing", "home_goods", "beauty", "other"] = Field(
        description="Product category if mentioned, otherwise 'other'"
    )