# 🖥️Code Reviewer and Management

This repository contains a Streamlit-based AI code review app and a small agent routing layer that selects different LLM providers depending on the review task.

Overview
--------

- UI: `app.py` — a Streamlit application where users upload or paste source code and run a review.
- Review logic: `agents/reviewer.py` — orchestrates three review types (bugs, security, deep review).
- Router: `agents/router.py` — maps review tasks to LLM client factories (Groq, Mistral, Gemini via LangChain integrations).
- Outputs: `output/reports` (Markdown reports) and `output/charts` (PNG summary charts).

Prerequisites
-------------

- Python 3.10+
- Install dependencies listed in `requirements.txt`.
- Provider API keys (for LLM clients) loaded via a `.env` file or environment variables.

Quick Start (Windows PowerShell)
-------------------------------

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the Streamlit URL shown in the terminal (usually http://localhost:8501).

How the app works
-----------------

- Use the sidebar to upload a file or paste code and (optionally) set a language hint.
- Click "Run Full Review" to run three review passes:
	- Quick bug scan (`bugs`) — routed to a fast model.
	- Security audit (`security`) — routed to a security-focused model.
	- Deep, architectural review (`deep_review`) — routed to a large-context model.
- The app saves a Markdown report to `output/reports` and PNG charts to `output/charts`.

Programmatic Example
---------------------

```python
from agents.reviewer import run_full_review

code = "def add(a, b):\n    return a + b"
results = run_full_review(code=code, language="Python")
print(results.keys())  # -> dict_keys(['bugs', 'security', 'deep_review'])
```

Configuration
-------------

- Put provider API keys in a `.env` file at the repo root or export them to your shell. `agents/router.py` calls `load_dotenv()`.
- Example variables (names depend on provider integrations):

```
OPENAI_API_KEY=...
MISTRALAI_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
```

Important Files
---------------

- `app.py` — Streamlit UI and orchestration.
- `agents/reviewer.py` — runs the three review tasks.
- `agents/router.py` — LLM client factories and routing logic.
- `requirements.txt` — dependencies; ensures `streamlit` and the provider packages are installed.

Troubleshooting
---------------

- If Streamlit won't start: confirm the virtual environment is activated and `streamlit` is installed.
- If LLM clients fail to initialize: confirm provider keys and the correct env var names for each LangChain integration.
- Check the terminal where `streamlit run app.py` was started for tracebacks.


