# VAANA AI Data Platform

A local Retrieval-Augmented Generation (RAG) analytics system providing natural language SQL queries for structured operations data.

## Overview

The VAANA AI Data Platform translates natural language questions into executable PostgreSQL queries using an offline-first ChromaDB vector store and OpenAI's language models. It targets technical operators and analysts querying complex relational databases without requiring manual SQL writing. The system employs prompt-injection guardrails, automatic SQL candidate ranking, and streaming response delivery to ensure safety and precision.

## Architecture

The platform operates on a separated frontend and backend model. The backend acts as the secure execution layer, interacting with an underlying telemetry database.

```text
[ React Frontend ] <--(Server-Sent Events)--> [ FastAPI Backend ]
                                                     |
                                            [ Vanna Bridge ]
                                             /              \
                          [ ChromaDB Index ]               [ OpenAI / LLM ]
                                 (Schema Context)               (SQL Generation)
                                                     |
                                            [ Executor ]
                                                 |
                                         (Read-Only DB)
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Vanna AI
- **Frontend**: React 18, Vite, TailwindCSS
- **Vector Storage**: ChromaDB (Local implementation)
- **Database Engine**: PostgreSQL (Target database)

## Project Structure

```text
.
├── backend/                  # API server and core AI logic
│   ├── api/                  # FastAPI routers and endpoints
│   ├── config/               # Pydantic settings and DDL schema definitions
│   ├── core/                 # Vanna integration, execution validation, prompt manipulation
│   ├── guardrails/           # Preventative LLM injection interceptors
│   ├── VAANA_MAIN/           # Core underlying Vanna training and data CLI
│   └── feedback/             # SQLite-backed feedback loops
└── frontend/                 # React UI client
    ├── public/               # Static assets (logos, icons)
    └── src/                  # React components, layout, API fetching logic
```

## Prerequisites

- Node.js >= 20.x
- Python >= 3.11
- PostgreSQL connection credentials

## Installation

1. Clone the repository.
   ```bash
   git clone <repository_url>
   cd VAANA_AI
   ```

2. Setup the backend Python environment.
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Setup the frontend node environment.
   ```bash
   cd ../frontend
   npm install
   ```

4. Populate environment variables.
   ```bash
   cd ../backend
   cp .env.example .env
   ```
   Edit `.env` strictly per the Environment Variables section.

## Environment Variables

| Variable Name         | Required | Description                                  | Example Value                       |
|-----------------------|----------|----------------------------------------------|-------------------------------------|
| `OPENAI_API_KEY`      | Yes      | API key utilized for the LLM SQL generation. | `sk-proj-...`                       |
| `OPENAI_MODEL`        | No       | LLM model designation.                       | `gpt-4o`                            |
| `DB_HOST`             | Yes      | Target PostgreSQL hostname/IP.               | `localhost`                         |
| `DB_PORT`             | Yes      | Target PostgreSQL port.                      | `5432`                              |
| `DB_USER`             | Yes      | Target PostgreSQL read-only user.            | `readonly_user`                     |
| `DB_PASSWORD`         | Yes      | Target PostgreSQL password.                  | `securepass`                        |
| `DB_NAME`             | Yes      | Target PostgreSQL database name.             | `mdm_database`                      |

*Refer to `backend/.env.example` for the template structure.*

## Manual Assets Required

This project filters large vector caches and temporary data dumps from Git tracking. The system rebuilds memory dynamically on the first execution based on provided text DDLs.
- Reference `_manual_assets/SETUP.md` for information regarding large un-tracked testing CSV artifacts (>200MB) excluded natively from the push.

## Running the Application

### Development
Launch two segregated terminal instances:

**Terminal 1 (Backend API):**
```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 (Frontend Client):**
```bash
cd frontend
npm run dev
```

### Production
For production environments, bundle the React frontend to static assets and serve via Nginx, communicating transparently with the FastAPI backend mapped through Uvicorn/Gunicorn.
```bash
# Build Frontend
cd frontend
npm run build

# Start Backend via ASGI Server
cd backend
.venv\Scripts\activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Database Setup

The integration connects strictly as a read-only client to an existing operational PostgreSQL MDM database.
1. No schema migrations are required locally.
2. The agent interprets the target database structure implicitly through `backend/config/ddl.py` and structural configuration files in `backend/VAANA_MAIN/data/`.

## Deployment

Deploy the Dockerized backend via a scalable container orchestration platform (e.g., Kubernetes, ECS) with persistent or ephemeral volumes, as ChromaDB vectors will automatically regenerate from `backend/VAANA_MAIN/data/` if lost. Serve the compiled frontend via CDN (Cloudfront, Vercel) pointing strictly to the backend API origin.

## Known Issues / Limitations

- Un-optimized multi-join LLM queries can trigger database timeouts defined at the executor level (currently capped at 30 seconds).
- ChromaDB vector bindings rely on native C extensions which require C++ build tools if compiled linearly outside of pre-built wheels.
- Row limits hard-cap SQL retrieval output at 5,000 records to prevent browser memory exhaustion on the frontend DOM.

## License

Proprietary. Copyright 2026.
