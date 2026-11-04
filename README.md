# Personal AI OS

A local-first foundation for a personal robot assistant and its future mobile and web clients. The initial service is a Memory Service: it persists durable user facts, preferences, episodes, and procedures behind a small HTTP API.

## Current structure

```text
apps/                 Future robot UI, mobile app, and dashboard
agents/               Future LangGraph agent workflows
services/
  memory_service/     FastAPI service for long-term memory
shared/               Cross-service configuration, schemas, and utilities
infrastructure/       Container and database deployment assets
docs/                 Architecture decisions and service design notes
```

## Run locally

Python 3.12 or newer is required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn services.memory_service.app.main:app --reload
```

The supplied configuration targets PostgreSQL. Start it with `docker compose up -d db`, then open <http://127.0.0.1:8000/docs>.

For a database-free first run, set `DATABASE_URL=sqlite:///./personal_ai_os.db` in `.env`. SQLite is intended only for local development; PostgreSQL with pgvector is the intended production store.

## First API call

```bash
curl -X POST http://127.0.0.1:8000/v1/memories \
  -H 'content-type: application/json' \
  -d '{"content":"Prefers local models over cloud-only tooling.","memory_type":"preference","importance":0.9}'
```

## Roadmap

- Add Alembic migrations and pgvector embeddings.
- Add memory extraction, ranking, and retrieval through LangChain.
- Orchestrate assistant workflows with LangGraph.
- Connect Ollama through the Model Service rather than directly from agents.
