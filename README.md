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
