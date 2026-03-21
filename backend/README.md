# MDM Vanna AI Integration

This project integrates the pre-built Vanna AI module into the FastAPI backend, bridging natural language queries to an MDM SQL database, and serving the queries via a seamless API exposed to a React frontend.

## Architecture

This backend securely isolates and interfaces with a read-only `VAANA_MAIN` module using `core/vanna_bridge.py`. It bypasses direct Python import issues and implements fallback routing.

- **`core/vanna_bridge.py`**: Singleton integration file handling LLM setup, training routines, and SQL generation.
- **`core/executor.py`**: SQLAlchemy-powered query executor enforcing timeout operations and result row truncations.
- **`api/routers/query.py`**: Executes the entire prompt extraction, SQL generation via Vanna, ranking, execution, and structure transformation pipeline.
- **`config/`**: Contains DDL, Event codes, and Documentation for the agent context memory.

## Setup Instructions

1. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment Variables**:
   Setup the API keys and Postgres Connection in `.env`.
   
3. **Start the API Server**:
   ```bash
   uvicorn main:app --reload
   ```
   *Note: Upon startup, the agent will verify if trained memory (`chroma_db/.trained`) exists, and run initialization training if missing.*

## Frontend Integration

The React GUI allows interacting with this backend endpoint natively.

1. Install Frontend dependencies:
   ```bash
   npm install
   ```
2. Start the Vite server:
   ```bash
   npm run dev
   ```

## Queries and Features
- **Generates KPI summary blocks**: Identifies unit summaries metrics for "this week", "today" and outputs concise cards.
- **Interactive UI Renderings**: Backend intelligently supplies chart configurations matching visual datasets.
- **Guardrails**: Safely verifies user inputs prohibiting model leakage, data modifications (DDL/DML instructions), and limits responses ensuring optimal usage parameters.
