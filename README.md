# Support Ticket Assistant

An AI system that reads customer support tickets, looks up the order, and either
answers automatically or hands the ticket to a human agent.

Built to practise safe LLM engineering: the model extracts facts, and code makes the decisions.

## How it works

```
ticket -> [1] Analyzer (LLM extracts facts)
       -> [2] Order lookup (SQLite, scoped to the logged-in customer)
       -> [3] Decider (rules in code)
       -> auto reply, ask for the order ID, or hand off to a human
```

- **Analyzer:** a local LLM (llama3.2 via Ollama) fills a pydantic form of true/false facts
  (for example `wrong_charge`, `package_lost`). It does not decide priority.
- **Priority:** computed in Python from those facts, so wording inside a ticket cannot set it.
- **Order ID:** found with a regex, not by the LLM.
- **Repeat contact:** read from a stored ticket history, not guessed by the model.
- **Decider:** an allowlist. Only delivery-status questions are answered automatically.
  Everything else (refunds, payments, legal threats, anything unclear) goes to a human.
- **Replies:** templates filled from the order record, so the model cannot invent facts
  such as delivery dates.
- **Security:** customer identity comes from a login token created by the server, never from
  the ticket text. Another customer's order returns the same "not found" message as a missing one.

## Results

| Test | Result |
|---|---|
| Analyzer, practice set (15 tickets, used for tuning) | intent 15/15, priority 13/15 |
| Analyzer, held-out set (10 unseen tickets, run once) | intent 7/10, priority 7/10 |
| Full pipeline, 17 labelled tickets | 16/17 correct routes |
| Pipeline: wrong automatic replies | 0 |
| Pipeline: data leaked between customers | 0 |

Both prompt-injection tests resisted. The practice-set score is optimistic because prompts were tuned
against those tickets; the held-out score is the honest one.

## Known limitations

- Small hand-written test sets, so scores are rough estimates.
- A 3B local model sometimes sets facts wrongly (for example `person_hurt` on a legal threat).
  Wrong facts only add escalation, so these failures are safe but cost agent time.
- A simple status question written in lowercase ("whats the status of od123") was sent to a human.
- The "delivered but not received" rule uses a fixed phrase list, tested on one wording.
- Repeat contacts never expire, so an old ticket about an order still counts as a repeat.
- Login tokens never expire, and demo passwords are for testing only.
- The MCP server (`mcp_server.py`) starts and exposes one tool, but no client is built yet.
- The ticket-history reset button on the page is a demo shortcut.

## Run it

1. Install [Ollama](https://ollama.com), then run `ollama pull llama3.2`.
2. `pip install -r requirements.txt`
3. `python db.py` (creates sample orders)
4. `python try_auth.py` (creates demo users C1/pass1 and C2/pass2)
5. `uvicorn api:app`
6. In a second terminal: `streamlit run app.py`

## Tests

- `python test_pipeline.py` runs the end-to-end routing tests.
- `python test_decide.py` tests the routing rules without an LLM.
- Set `DB_PATH=test.db` so tests do not touch live data.

## Files

| File | Job |
|---|---|
| `model.py` | The form the LLM fills, plus the priority rules |
| `ticket_analysis.py` | Sends a ticket to the LLM and validates the result |
| `lookup.py` | Order lookup with the ownership check |
| `tickets.py` | Ticket history |
| `decide.py` | Routing rules |
| `pipeline.py` | Connects everything |
| `auth.py`, `api.py` | Login and the web API |
| `app.py` | Streamlit page |
| `mcp_server.py` | The order lookup exposed as an MCP tool |