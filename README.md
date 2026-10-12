# Ticket Extractor

Analyze customer support tickets with the Anthropic API and validate the
structured result with Pydantic.

## Requirements

- Python 3.10 or newer
- An Anthropic API key

## Install

From the project directory, create and activate a virtual environment, then
install the Python dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Set the API key in PowerShell before running the analysis:

```powershell
$env:ANTHROPIC_API_KEY = "your-api-key"
```

The environment variable is available only in the current PowerShell session.
Do not commit API keys to source control.

## Run

Run the included sample evaluation:

```powershell
python -c "from ticket_analysis import evaluate; evaluate()"
```

The evaluation makes API calls and prints the sample accuracy.

## Results

| Set | Intent | Priority |
|---|---|---|
| Practice (15 tickets, used for tuning) | 15/15 | 13/15 |
| Held-out (10 unseen tickets, run once) | 7/10 | 7/10 |

Model: llama3.2 (3B) running locally via Ollama.

## Design
The LLM extracts true/false facts from each ticket. Python code computes priority
from those facts, so wording inside a ticket cannot set the priority directly.
Both prompt-injection tests in the held-out set were resisted.

## Known limitations
- `contacted_support_before` sometimes fires when the customer never said they contacted support.
- No rule covers a package that arrives with an item missing.
- Unclear one-line tickets do not reliably set `needs_human`.
- Evaluated on small sets, so scores are rough estimates.