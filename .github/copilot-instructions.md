# AI Sales Assistant - BI Agent MVP

## ⚠️ IMPORTANT: Project Structure Policy

**ALL code MUST respect the structure defined in `PROJECT_STRUCTURE.md`.**

### Before Creating/Modifying ANYTHING:
1. **Check Phase**: Identify which phase (0-5) this belongs to
2. **Check Location**: Consult `PROJECT_STRUCTURE.md` and `STRUCTURE_QUICK_REFERENCE.md`
3. **Follow Conventions**: Spanish for business domain, English for technical
4. **Add Tests**: Unit tests + integration tests
5. **Use StructuredLogger**: Always for logging (from `utils/logging_config.py`)

### Documentation Policy
**DO NOT automatically generate documentation files.** Only create `.md` files when explicitly requested:
- ❌ Auto-generated status files (`FINAL_STATUS.md`, `PHASE_STATUS.md`, etc.)
- ❌ Auto-generated migration guides or summaries
- ✅ ONLY create when user explicitly says "create a guide..." or names specific file

**Goal**: Keep project clean, organized per structure, and clutter-free.

---

## 📂 Project Structure Overview

```
bi-agent/
├── agent/                      # CORE: Agent + tools (Fase 1+)
├── api/                        # API: REST endpoints (Fase 2+)
├── security/                   # Validation: Input/output (Fase 1.5+)
├── evaluation/                 # Evaluation: RAGAS (Fase 3+)
├── monitoring/                 # Monitoring: Prometheus (Fase 2+)
├── mlflow/                     # MLOps: Experiments (Fase 3+)
├── utils/                      # Shared: Logging, config, metrics
├── tests/                      # Testing: unit/ + integration/
├── empresa_docs/               # DATA: Business data (read-only)
├── data/                       # Processing: ChromaDB (Fase 5+)
├── config/                     # Configuration: .env, docker, prometheus
├── scripts/                    # Automation: setup, deploy, evaluation
├── docs/                       # Documentation: guides, implementations
├── logs/                       # Output: logs, results
└── .github/                    # CI/CD: workflows, copilot instructions
```

**Reference Files** (Essential - Review Before Coding):
- `PROJECT_STRUCTURE.md` - Complete blueprint of structure + conventions
- `PROJECT_STATUS.md` - Current state + what's next
- `STRUCTURE_QUICK_REFERENCE.md` - Quick reference matrix

---

## Project Overview
This is a **Business Intelligence agent** MVP built with **LangGraph** and Google Gemini that enables natural language queries over consulting company data (projects, consultants, clients, case studies, proposals). The project uses **LangGraph StateGraph** for explicit control flow, conversational memory, automatic retries, and visual debugging.

## Architecture Philosophy

### LangGraph Architecture (Phases 0-5)
- **Phase 0**: Setup (venv, .env, requirements with langgraph)
- **Phases 1-4 (Core MVP)**: LangGraph with ReAct + Memory
  - Explicit StateGraph with reasoning → tools → conditional routing
  - Conversational memory (AgentState TypedDict)
  - Automatic retries and fallback strategies
  - 5-10s startup time, 2-5s query latency
  - Generic tools: `discover_files()`, `read_collection()`, `search_by_text()`
  - Visual debugging with LangSmith graph traces
  
- **Phase 5 (Optional)**: Hybrid System with indexed search
  - 15-20s startup for indexing, 50-200ms query latency (20x faster)
  - Adds ChromaDB + semantic search via sentence-transformers
  - Only implement if needed for production scale

### Key Design Patterns
1. **LangGraph StateGraph**: Explicit graph with nodes (reasoning, tools) and conditional edges - better than LangChain chains
2. **Conversational Memory**: AgentState TypedDict persists context between turns for multi-step analysis
3. **Automatic Retries**: Conditional routing handles tool failures with automatic retry logic
4. **Observability from Day 1**: LangSmith tracing (graph visualization), structured JSON logging, Prometheus metrics
5. **Format-Agnostic Tools**: Generic file discovery & search tools that work with ANY data structure (JSON, CSV, text, nested objects, etc.)
6. **No Domain Coupling**: Tools don't assume fixed schemas - agent dynamically handles any data format
7. **ReAct Pattern + Graph**: Agent uses reasoning-action cycles within explicit StateGraph with Google Gemini 2.0 Flash
8. **Guardrails**: Input validation (SQL/prompt injection) and output validation (PII detection) via Guardrails AI
9. **Structure-First Development**: All new code respects defined directory structure

## Data Structure (EXAMPLE)

### Location: `empresa_docs/`
All business data lives in JSON files with consistent Spanish naming:
- `proyectos.json` - Projects with team, tech stack, budget, duration
- `consultores.json` - Consultants with skills, experience, availability, daily rates
- `clientes.json` - Clients with industry, location, size
- `casos_estudio.json` - Case studies with results and impact
- `propuestas.json` - Commercial proposals with status and probability

### Key Data Patterns
- IDs use prefixes: `PROJ001`, `CONS030`, `CLI008`
- Nested structures: projects contain team arrays, consultants contain skill arrays
- Spanish field names: `años_experiencia`, `tarifa_dia_usd`, `disponibilidad`
- Mixed data types: some fields are strings, some are structured objects

**⚠️ REMEMBER**: Data can be in ANY format. Use generic tools (`discover_files`, `read_collection`, `search_by_text`) that work with any structure.

---

## Where Code Goes (Phase-Based Placement)

| Need | Phase | Directory | File |
|------|-------|-----------|------|
| Modify agent | 1 | `agent/` | `bi_agent.py` |
| Add tool | 1 | `agent/` | `tools.py` |
| Input validation | 1.5 | `security/` | `input_validator.py` |
| PII detection | 1.5 | `security/` | `output_validator.py` |
| REST endpoint | 2 | `api/routes/` | `[name].py` |
| API model | 2 | `api/models/` | `request.py`, `response.py` |
| API auth | 2 | `api/middleware/` | `auth.py` |
| Prometheus metrics | 2 | `monitoring/` | `prometheus_config.py` |
| RAGAS evaluation | 3 | `evaluation/` | `ragas_evaluator.py` |
| Experiment tracking | 3 | `mlflow/` | `tracker.py` |
| Unit tests | Any | `tests/unit/` | `test_[module].py` |
| Integration tests | Any | `tests/integration/` | `test_[flow].py` |

**For complete reference**: See `STRUCTURE_QUICK_REFERENCE.md` Matrix section.

---

## ### ⚠️ ChromaDB & Semantic Search (Phase 5+ ONLY)
**IMPORTANT**: ChromaDB is NOT part of Phases 1-4 (Core MVP).

- **Phases 1-4 Tools** (Copilot-Like): `discover_files()`, `read_collection()`, `search_by_text()`
  - ✅ Query latency: 2-5 seconds
  - ✅ Zero startup time
  - ✅ Sufficient for demo/portfolio

- **Phase 5 Additional Tools** (Optional Hybrid): `semantic_search()`, `semantic_similarity()`
  - ✅ Query latency: 50-200ms (20x faster)
  - ⚠️ Startup time: 15-20s for indexing
  - ✅ Only if needed: > 500 queries/day OR dataset > 1MB

**Default is Copilot-Like (Phases 1-4)**. Semantic search is purely optional and added in Phase 5.

---

## Critical Workflows

### Development Setup (Phases 1-4: Core MVP)
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install base dependencies (Copilot-Like MVP)
pip install -r requirements-base.txt

# Configure environment variables
# .env file MUST include:
# - GOOGLE_API_KEY (Gemini)
# - LANGCHAIN_TRACING_V2=true
# - LANGCHAIN_API_KEY (for observability)
# - LANGCHAIN_PROJECT=bi-agent-dev
```

### Optional: Hybrid System Setup (Phase 5+)
```powershell
# IF you need semantic search + indexing (Phase 5+ only)
pip install -r requirements-hybrid.txt

# Then initialize ChromaDB
python scripts/setup_chromadb.py

# Enable in .env:
# ENABLE_HYBRID=true
```

### Testing Queries
- **Use CLI**: `python main.py "Your question"`
- **Use Interactive**: `python main.py --interactive`
- **Run tests**: `pytest tests/unit/ -v` or `python test_fase1_5.py`
- **Every query traces to LangSmith** (https://smith.langchain.com/) automatically
- **Check logs**: `Get-Content logs/app.log | ConvertFrom-Json | Format-Table`

### Monitoring Stack
- **LangSmith**: Deep LLM observability, trace every agent step
- **Prometheus**: Metrics collection on `/metrics` endpoint
- **Grafana**: Visual dashboards (port :3000)
- **RAGAS**: Automated evaluation (Phase 3+)

---

## Project-Specific Conventions

### File Organization (Respect Structure!)
```
agent/          - Core agent logic (tools, prompts, agent class)
api/            - REST API (routes, models, middleware)
security/       - Input/output validation, guardrails
evaluation/     - RAGAS evaluation suite
monitoring/     - Prometheus + Grafana configs
mlflow/         - Experiment tracking
utils/          - Helpers (logging_config, metrics, data_loader)
tests/          - Unit and integration tests
docs/           - Implementation guides
config/         - Configuration files
scripts/        - Automation scripts
empresa_docs/   - Business data (NEVER modify programmatically)
logs/           - Structured JSON logs and results
```

### Naming Conventions
- **Spanish for business domain**: `consultores`, `proyectos`, `clientes`, `bi_agent`
- **English for technical code**: `utils`, `api`, `models`, `middleware`, `routes`
- **Tools are verbs**: `discover_files()`, `read_collection()`, `search_by_text()`
- **Metrics use snake_case**: `bi_agent_query_duration_seconds`, `tool_usage_counter`

### Logging Standards
All logs must be **structured JSON** with required fields:
```python
{
  "timestamp": "ISO-8601 format",
  "level": "INFO|WARNING|ERROR",
  "message": "Human-readable description",
  "user_input": "First 100 chars of query",
  "latency": 2.34,  # seconds
  "status": "success|error"
}
```

**Always use**: `StructuredLogger` from `utils/logging_config.py`, not raw `logging` module.

### Tool Implementation Pattern
```python
from langchain.tools import tool
from typing import Optional

@tool
def your_tool_name(param: str, optional_param: Optional[str] = None) -> str:
    """
    Clear docstring - LLM uses this to decide when to call tool.
    
    Include:
    - When to use this tool (specific examples)
    - Parameter descriptions
    - Return format
    """
    # Implementation
    return formatted_string_result  # Always return strings, not dicts
```

---

## Integration Points

### LangGraph + Gemini Setup
- Framework: `langgraph` for StateGraph (explicit control flow)
- LLM: `ChatGoogleGenerativeAI` from `langchain-google-genai`
- Model: `gemini-2.0-flash` (latest, most capable)
- Temperature: 0.0 for factual, 0.3 for creative
- Streaming: Disabled by default
- Tools: Bound to LLM with `.bind_tools()` method

### LangSmith Integration
- Tracing is **automatic** when `LANGCHAIN_TRACING_V2=true`
- Use `@traceable` decorator for custom function tracing
- Project names separate dev/prod: `bi-agent-dev` vs `bi-agent-prod`

### MLflow Tracking (Phase 3+)
- Tracks experiment runs for prompt A/B testing
- Log parameters: model, temperature, prompt version
- Log metrics: RAGAS scores, latency, token usage
- Artifacts: prompts, sample outputs
- Access UI at `http://localhost:5000`

### Docker Compose Services (Phase 3+)
- `app`: Main BI agent (FastAPI on :8000)
- `prometheus`: Metrics collection (:9090)
- `grafana`: Dashboards (:3000)
- `mlflow`: Experiment tracking (:5000)

---

## Common Pitfalls to Avoid

1. **Don't add indexing/ChromaDB before Phase 5**: The MVP works without it. Validate value first.
2. **Don't use collection-specific tools**: Use generic `discover_files()` + `read_collection()` pattern.
3. **Don't skip LangSmith setup**: It's 5 minutes that saves hours of debugging.
4. **Don't parse logs manually**: Use structured logging from day 1.
5. **Don't assume data schema**: JSON files may have nested structures.
6. **Don't ignore the project structure**: All code must follow `PROJECT_STRUCTURE.md`.
7. **⚠️ DO NOT AUTO-GENERATE DOCUMENTATION**: Only create `.md` files when explicitly requested.

---

## Key Files to Reference

- `PROJECT_STRUCTURE.md` - Complete blueprint of structure + all conventions
- `PROJECT_STATUS.md` - Current state + what's next
- `STRUCTURE_QUICK_REFERENCE.md` - Quick reference matrix for searching
- `README.md` - User-facing documentation
- `agent/tools.py` - Tool implementation patterns
- `utils/logging_config.py` - Structured logging setup
- `.github/copilot-instructions.md` - This file (Copilot guidelines)

---

## Testing Expectations

- Unit tests: 85%+ coverage target
- Integration tests: Test tool chains, not individual tools
- E2E tests: Full query → response cycles with real data
- Evaluation: RAGAS scores > 0.7 for faithfulness, > 0.8 for relevancy
- Performance: < 5s latency for Copilot-like, < 200ms for hybrid
- **All tests must pass before committing**

---

## ⚠️ IMPORTANT: Always activate venv before running commands

### Quick Reference Commands

```powershell
# Activate virtual environment (ALWAYS DO THIS FIRST)
.\venv\Scripts\Activate.ps1

# Run agent CLI
python main.py
python main.py "Your question here"
python main.py --interactive

# Run comprehensive tests
python test_fase1_5.py

# Run API server (Fase 2+)
python api.py

# Test API endpoints
python test_api.py

# Run unit tests
pytest tests/unit/ -v

# Run all tests with coverage
pytest tests/ -v --cov=agent --cov=utils

# View logs (last 10 lines)
Get-Content logs\app.log | Select-Object -Last 10

# View structured JSON logs
Get-Content logs\app.log | ConvertFrom-Json | Select-Object timestamp, message, latency | Format-Table

# Check test results
Get-Content logs\fase1.5_test_results.json | ConvertFrom-Json | Format-List

# Start monitoring stack (Phase 3+)
docker-compose up -d

# View metrics
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# MLflow: http://localhost:5000

# Run RAGAS evaluation
python evaluation/ragas_evaluator.py

# Install/update dependencies
pip install -r requirements-base.txt --upgrade

# Deactivate venv (when done)
deactivate
```

### Common Command Patterns

**Single Query**:
```powershell
.\venv\Scripts\Activate.ps1
python main.py "Your question here"
deactivate
```

**Multiple Queries with Logging**:
```powershell
.\venv\Scripts\Activate.ps1
python test_fase1_5.py
deactivate
```

**Start API Server**:
```powershell
.\venv\Scripts\Activate.ps1
python api.py
# Keep this terminal open, open new terminal for tests
```

**Test API (in separate terminal)**:
```powershell
.\venv\Scripts\Activate.ps1
python test_api.py
deactivate
```
