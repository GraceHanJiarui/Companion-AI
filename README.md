# Companion AI

A FastAPI + PostgreSQL/pgvector + LLM backend for building a companion-style character system with:

- long-term memory
- boundary-aware behavior
- relationship state modeling
- controller/actor generation
- debug and observability tooling

## What It Does

This project is not a single-prompt chatbot. It is a stateful dialogue system designed to keep track of:

- full conversation history
- user boundaries and preferences
- episodic memories
- a multi-dimensional relationship state
- behavior controls that shape how the assistant speaks

The current chat pipeline is:

1. log the user event
2. extract and store beliefs / boundaries
3. estimate relational delta `ΔR`
4. update relationship state and projected behavior
5. retrieve relevant memories with embeddings + pgvector
6. generate a structured controller plan
7. generate the final natural-language reply with the actor
8. write debug snapshots and turn events

## Core Ideas

### Relationship state is explicit

The system tracks:

- `bond`
- `care`
- `trust`
- `stability`

These are projected into behavior variables such as warmth, directness, initiative, affective questioning, and disclosure level.

### Boundaries are persistent

User statements like “don’t ask me about stress again” can be extracted into long-lived beliefs and enforced as ongoing policy constraints.

### Memory is separate from raw history

The system keeps:

- raw append-only dialogue events
- summarized episodic memories stored with embeddings

This allows retrieval of semantically relevant past interactions without always replaying the entire transcript.

### Planning and language generation are split

- Controller: decides structured intent/behavior/constraints
- Actor: turns that plan into natural language

This makes behavior easier to debug, constrain, and eventually distill into smaller models.

## Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- pgvector
- OpenAI-compatible Responses API
- Pydantic

## Project Layout

```text
app/
  api/            HTTP endpoints
  beliefs/        boundary / belief extraction and policy logic
  controller/     structured planning layer
  core/           config, LLM client, core self
  db/             database session/base
  generation/     actor prompt construction
  inference/      tone / relational delta evaluator
  memory/         event logging, embeddings, memory retrieval
  models/         ORM models
  outbox/         async job queue worker
  relational/     relation -> behavior projection
migrations/       Alembic migrations
test/             batch-style regression scripts
```

## Main Endpoints

- `POST /chat`
- `GET /debug/sessions/{session_id}/state`
- `GET /debug/sessions/{session_id}/beliefs`
- `GET /debug/sessions/{session_id}/context`
- `GET /sessions/{session_id}/events`
- `GET /health/llm`

## Quick Start

### 1. Start Postgres

```bash
docker compose up -d
```

### 2. Install dependencies

```bash
pip install -e .
```

### 3. Create `.env`

```env
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/companion
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-5-nano
EMBEDDING_MODEL=text-embedding-3-small
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

## Example

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"session_id\":\"demo-1\",\"user_text\":\"别再问我压力大不大。\"}"
```

## Tooling

- `test/batch_style_tests.py`
  Regression checks for disclosure gating, de-obligation language, and leave-context violations.
- `actor_batch_probe.py`
  Offline actor probing across behavior profiles for analysis and dataset building.

## Current Status

Implemented in the current codebase:

- event logging
- belief extraction and storage
- relationship state updates
- relation-to-behavior projection
- memory retrieval with pgvector
- controller planning
- actor generation
- debug APIs
- outbox worker scaffold
- batch-style testing scripts

## Notes

This repository is actively evolving. Some non-critical paths, especially async belief extraction and summary-writing flow, still show signs of in-progress integration.

## Internal Docs

Detailed architecture and maintenance notes live in:

- [PROGRAM_DESIGN_DOCUMENT.md](d:/My%20Project/companion-ai/PROGRAM_DESIGN_DOCUMENT.md)
