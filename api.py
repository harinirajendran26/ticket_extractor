from fastapi import FastAPI, Header
from pydantic import BaseModel

from pipeline import process_ticket

app = FastAPI()


class TicketIn(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets")
def create_ticket(ticket: TicketIn, x_customer_id: str = Header()):
    result = process_ticket(ticket.text, x_customer_id)
    return {"route": result.route, "reply": result.reply}