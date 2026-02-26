# AI Chatbot Project

## What is this project?
A FastAPI-based AI chatbot backend using OpenAI GPT-4o-mini.
Conversation history is stored in SQLite. Includes a simple HTML frontend.
Three-layer test infrastructure: unit (pytest), LLM eval (deepeval), e2e (playwright).

## Tech Stack
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **LLM:** OpenAI GPT-4o-mini (`openai` library)
- **DB:** SQLite (no external connection, file-based)
- **Unit Test:** Pytest + HTTPX (AsyncClient)
- **LLM Eval:** DeepEval
- **E2E Test:** Playwright + pytest-playwright
- **Config:** python-dotenv, `.env` file

## Project Structure
```
ai-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app, endpoints
│   ├── chat.py        # OpenAI integration, get_response()
│   ├── models.py      # Pydantic models (ChatRequest, ChatResponse)
│   └── database.py    # SQLite CRUD, conversation history
├── frontend/
│   └── index.html     # Single-page chat interface
├── tests/
│   ├── unit/
│   │   └── test_api.py
│   ├── eval/
│   │   └── test_llm_quality.py
│   └── e2e/
│       └── test_chat_ui.py
├── .env               # API key lives here (not committed to git)
├── .gitignore
└── requirements.txt
```
## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

## Commands
```bash
# Start the application
uvicorn app.main:app --reload --port 8000

# Unit tests
pytest tests/unit/ -v

# LLM eval tests
deepeval test run tests/eval/test_llm_quality.py

# E2E tests (application must be running)
pytest tests/e2e/ -v

# E2E with visible browser
pytest tests/e2e/ -v --headed

# All unit + e2e
pytest tests/unit/ tests/e2e/ -v
```

## Rules
- Never commit the `.env` file — it must be in `.gitignore`
- When adding a new endpoint, always write a test under `tests/unit/`
- Do not test LLM responses with `assert response == "..."` — they are non-deterministic. Use DeepEval metrics
- All OpenAI calls must go through `app/chat.py` only
- Conversation history must always be managed through `app/database.py`
- The system prompt is defined only in `app/chat.py` in the `SYSTEM_PROMPT` variable

## Environment Variables (.env)
```
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
APP_PORT=8000
```

## Important Notes
- `app/__init__.py` must exist but remain empty (required for Python package)
- The DB file (`chatbot.db`) is created automatically during the `startup` event on first launch
- The application must be running at `localhost:8000` before executing e2e tests
- DeepEval tests make requests to the OpenAI API and incur costs — run with caution

## CI/CD Pipeline
- GitHub Actions configured via `.github/workflows/ci.yml`
- Triggered automatically on push to the main branch
- Order: unit tests → playwright + deepeval (parallel)
- Add `OPENAI_API_KEY` to GitHub Secrets
- repo → Settings → Secrets → New secret → OPENAI_API_KEY
