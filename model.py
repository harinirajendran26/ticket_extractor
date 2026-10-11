from pydantic import BaseModel, Field

class TicketAnalysis(BaseModel):
    # ... keep your existing intent, order_id, sentiment, needs_human, product_category ...

    injury_or_hazard: bool = Field(
        description="Someone was hurt, or the product is dangerous")
    legal_or_public_threat: bool = Field(
        description="Customer threatens consumer court, legal action, police, media, or social media")
    contacted_support_before: bool = Field(
        description="Customer says THEY already contacted the company's support and got no resolution")
    money_or_goods_lost: bool = Field(
        description="Money wrongly charged or deducted, refund owed but not received, "
                    "package lost or marked delivered but not received, or item arrived completely destroyed")
    order_problem: bool = Field(
        description="Something went wrong with an order (late, wrong item, defective, stuck status)")
    asks_about_own_order: bool = Field(
        description="Customer asks a question about an order they placed (cancel, return, change)")

    @property
    def priority(self) -> int:
        if self.injury_or_hazard or self.legal_or_public_threat or self.contacted_support_before:
            return 5
        if self.money_or_goods_lost:
            return 4
        if self.order_problem:
            return 3
        if self.asks_about_own_order:
            return 2
        return 1