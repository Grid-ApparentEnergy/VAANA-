# VAANA AI - MDM Integration

VAANA AI is a production-grade natural language interface for Meter Data Management (MDM) systems. It allows users to query complex electrical grid data using conversational English, backed by robust guardrails, RAG-based context memory, and secure streaming endpoints.

## 🚀 Project Overview

The VAANA AI Integration bridges natural language processing with raw relational data. By leveraging Vanna 2.0 and OpenAI's GPT models, the system translates conversational questions into precise SQL queries, executes them securely against a PostgreSQL MDM database, and structures the output into actionable insights, tables, KPIs, and visualization-ready chart configurations.

## 🏗️ Architecture

- **Frontend**: React + Vite (Port 5173). Serves the dashboard UI.
- **Backend API**: FastAPI (Port 8000). Handles streaming responses, input guardrails, output sanitization, and REST endpoints.
- **AI Core (`VAANA_MAIN`)**: Isolated Vanna bridge with custom Python training routines for MDM DDL and domain documentation.
- **Memory**: Persistent ChromaDB vector database storing trained QA examples and schema context locally.
- **Execution Engine**: SQLAlchemy-powered query executor enforcing timeout operations, read-only connections, and row truncations.

## 🧰 Tech Stack

- **Language**: Python 3.10+
- **Frameworks**: FastAPI, React
- **AI/LLM**: Vanna AI (v2.0), OpenAI (gpt-4o)
- **Database**: PostgreSQL (MDM Schema)
- **Vector Search**: ChromaDB
- **UI Tooling**: Vite, npm

## 📂 Directory Structure

```text
VAANA_AI/
├── frontend/                 # React UI application
├── backend/
│   ├── api/                  # FastAPI routers (query, feedback, streaming)
│   ├── config/               # Settings, DDL injections, Event codes
│   ├── core/                 # Vanna bridge and execution orchestrator
│   ├── guardrails/           # Input checking and PII/Model sanitization
│   ├── VAANA_MAIN/           # Core wrapper for Vanna training and setup
│   ├── main.py               # Main application entry point
│   └── requirements.txt      # Python dependencies
├── _large_files_manual_add/  # Instructions for local db/cache setup
├── .env.example              # Example environment configurations
└── .gitignore                # Production git exclusions
```

## ⚠️ Important Note on Large Files

Due to GitHub repository limits, large vectorized database caches (`vanna_2_0_chroma_db`) and virtual environments are **excluded** from this repository. 
Please refer to `_large_files_manual_add/INSTRUCTIONS.md` for strict guidance on how to restore the AI memory locally before running the backend.

## 🛠️ Installation Instructions

### 1. Prerequisites
- Python 3.10+
- Node.js & npm
- Access to the MDM PostgreSQL Database

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the `backend/` directory (you can copy `.env.example`).
**Required Variables**:
- `OPENAI_API_KEY`: Your OpenAI API Key.
- `OPENAI_MODEL`: (Optional) Defaults to `gpt-4o`.
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL connection details.

### 4. Running the Application

**Start the Backend API**:
```bash
cd backend
uvicorn main:app --reload
```
*Note: Upon first startup (if ChromaDB is empty), the agent will automatically read `mdm-ddl.sql` and `examples.json` to seed its memory.*

**Start the Frontend UI**:
```bash
cd frontend
npm install
npm run dev
```

## 📈 Usage

Navigate to `http://localhost:5173` in your browser. You can type queries like:
- *"Show me the top 10 devices by energy consumption this week"*
- *"What are the critical alerts right now?"*

The backend will process the prompt, stream the status natively via FastAPI, and return structured KPIs and chart representations.
