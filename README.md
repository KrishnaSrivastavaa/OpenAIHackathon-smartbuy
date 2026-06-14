# CommercePilot

CommercePilot is a full-stack AI-powered shopping assistant that helps users discover, compare, and refine product recommendations with natural language.

## Stack

- Frontend: React, TypeScript, Vite, TailwindCSS, shadcn-style reusable UI primitives, Axios, React Router, Lucide React
- Backend: FastAPI, Pydantic, Uvicorn, HTTPX, python-dotenv
- AI workflow: LangGraph, LangChain, Gemini 2.5 Flash through Google Generative AI packages

## Agentic workflow

The FastAPI backend exposes `POST /api/search` and runs a LangGraph workflow with these nodes:

1. Requirement Extraction Agent parses budget, category, use cases, excluded brands, and priorities.
2. Product Search Agent queries the configured provider.
3. Filtering Agent applies budget and brand constraints.
4. Review Analysis Agent derives scores, pros, and cons.
5. Recommendation Agent produces the final top-five recommendations and explanations.

Product providers are abstracted behind `ProductProvider`. The default mock provider works offline; `DummyJSONProvider` demonstrates an HTTP-backed implementation. A RapidAPI/Amazon provider can be added by implementing the same interface and selecting it from `PRODUCT_PROVIDER`.

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Optional: add GOOGLE_API_KEY for Gemini-backed enhancements
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173 and try:

- `I need a gaming laptop under ₹80,000 for coding and occasional gaming.`
- `Show lighter options.`
- `Prioritize battery life.`
- `Exclude Lenovo.`

## API

### `GET /api/health`

Returns service health.

### `POST /api/search`

Request:

```json
{
  "query": "I need a gaming laptop under ₹80,000 for coding and occasional gaming.",
  "session_id": null,
  "history": []
}
```

Response includes the session id, extracted requirements, top recommendations, product images, price, ratings, key specs, pros, cons, comparison rows, and assistant message.

## Environment variables

Backend:

- `GOOGLE_API_KEY`: optional Google Generative AI key.
- `GEMINI_MODEL`: defaults to `gemini-2.5-flash`.
- `PRODUCT_PROVIDER`: `mock` or `dummyjson`.
- `CORS_ORIGINS`: comma-separated frontend origins.

Frontend:

- `VITE_API_BASE_URL`: FastAPI base URL, default `http://localhost:8000`.
