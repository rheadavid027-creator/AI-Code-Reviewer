# Code Reviewer and Management

A lightweight project for automated code review and report generation with a Next.js frontend and a Python backend.

## Overview

- Backend: `app.py` and `agents/` contain Python services and agent logic for reviewing code and routing tasks.
- Frontend: `frontend/` contains a Next.js app for submitting code and viewing reports.
- Output: `output/` stores generated charts and review reports.

## Prerequisites

- Python 3.10+ (Windows recommended, but Linux/macOS should work)
- Node.js 18+ and npm (for the frontend)
- Git (optional)

## Quick start — Backend

1. Create and activate a virtual environment:

```powershell
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# or on cmd:
# venv\Scripts\activate.bat
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the backend service:

```powershell
python app.py
```

Notes:
- `app.py` is the entrypoint for the backend. If your project uses a specific framework (Flask/FastAPI) the file will reflect that; otherwise run as above.
- The `agents/` folder contains: `reviewer.py` (review logic) and `router.py` (task routing). Inspect these for configuration and usage.

## Quick start — Frontend

1. Change to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

2. Run the frontend in development mode:

```bash
npm run dev
```

3. Open the app in your browser (usually at `http://localhost:3000`).

Notes:
- The frontend is built with Next.js and TypeScript. See `frontend/package.json` for available scripts.

## Project Structure

- `app.py` — Backend entrypoint.
- `requirements.txt` — Python dependencies.
- `agents/` — Python agents and routing logic:
  - `reviewer.py` — main code review agent.
  - `router.py` — dispatches review tasks.
- `frontend/` — Next.js frontend app.
- `output/` — generated charts and reports (e.g., `main_review.md`).
- `Test_code_file/` — sample/test files.

## Usage

1. Start the backend and frontend (see Quick start sections).
2. Use the frontend UI to submit code for review, or call the backend API endpoints directly (consult `app.py` for routes).
3. Generated reviews and artifacts are saved to `output/`.

## Development

- Linting & formatting: add and run tools like `black`/`flake8` for Python and `prettier`/`eslint` for the frontend.
- Add a virtual environment to `.gitignore` (e.g., `venv/`).
- When modifying agents, run the backend and use sample inputs from `Test_code_file/` to validate behavior.

## Testing

- There are no automated tests in the repo by default. Add `pytest` for Python tests and `vitest`/`jest` for frontend tests as needed.

## Deployment

- Backend: containerize with Docker or deploy to a Python-friendly host. Ensure environment variables and secrets are configured.
- Frontend: build with `npm run build` and deploy to Vercel, Netlify, or any static host; if SSR is required, host in a Node environment.

## Configuration

- Environment variables: if `app.py` or the agents expect configuration (API keys, timeouts), set them in your shell or a `.env` file and load them in the application.

## Contributing

- Fork the repo, create a feature branch, add tests, and open a pull request.
- Keep changes small and document higher-level design decisions in `output/` or a new `docs/` folder.

## Troubleshooting

- "Missing packages": ensure you're in the virtual environment and run `pip install -r requirements.txt`.
- "Frontend not starting": run `npm install` then `npm run dev` inside the `frontend/` folder.
- Check the console and logs for `app.py` for backend errors.

## Useful Commands

- Backend

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

- Frontend

```bash
cd frontend
npm install
npm run dev
```

## Where to Look Next

- Inspect `agents/reviewer.py` to understand how reviews are generated.
- Inspect `frontend/src/components` to customize the submission UI.
- Generated report examples: `output/main_review.md`, `output/pasted_code_review.md`.

## License

Add a `LICENSE` file for your preferred license.

---

If you'd like, I can: add a `Makefile` or PowerShell scripts to simplify these commands, expand the README with API examples from `app.py`, or generate a `requirements.txt` snapshot. Which would you prefer next?