from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from auth import customer_for_token, init_auth_tables, login
from pipeline import process_ticket

init_auth_tables()

app = FastAPI()


class TicketIn(BaseModel):
    text: str


class LoginIn(BaseModel):
    customer_id: str
    password: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login")
def do_login(body: LoginIn):
    token = login(body.customer_id, body.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Wrong customer ID or password")
    return {"token": token}


@app.post("/tickets")
def create_ticket(ticket: TicketIn, authorization: str = Header()):
    scheme, _, token = authorization.partition(" ")
    customer_id = customer_for_token(token) if scheme.lower() == "bearer" else None
    if customer_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    result = process_ticket(ticket.text, customer_id)
    return {"route": result.route, "reply": result.reply}