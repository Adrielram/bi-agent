# AI Sales Assistant - BI Agent MVP

## ⚠️ IMPORTANT: Documentation Policy

**DO NOT automatically generate documentation files.** Only create `.md` files when explicitly requested by the user.

This includes:
- ❌ Status files (`FINAL_STATUS.md`, `PHASE_STATUS.md`, etc.)
- ❌ Migration guides (`MIGRATION_COMPLETE.md`, etc.)
- ❌ Summary documents (`CAMBIOS_*.md`, etc.)
- ❌ Verification reports
- ❌ Any other `.md` files not explicitly requested

**ONLY create documentation when:**
- User says "create a guide...", "document this...", "write a .md file..."
- User specifically names a file to create
- It's part of the core project structure (already exists)

**Goal**: Keep root directory clean, organized, and clutter-free. No auto-generated documentation.

---

## Project Overview
This is a **Business Intelligence agent** MVP built with LangChain and Google Gemini that enables natural language queries over consulting company data (projects, consultants, clients, case studies, proposals). The project follows a **hybrid evolution pattern**: starting simple (Copilot-like approach) with zero setup, then optionally evolving to indexed search for production scale.

## Architecture Philosophy

### Evolutionary Approach (Phases 1-5)
- **Phases 1-4 (Core MVP)**: Copilot-Like architecture with on-demand file reading
  - Zero startup time, 2-5s query latency
  - Generic tools: `discover_files()`, `read_collection()`, `search_by_text()`
  - Sufficient for demo/portfolio (< 500 queries/day, datasets < 1MB)
  
- **Phase 5 (Optional)**: Hybrid System with indexed search
  - 15-20s startup for indexing, 50-200ms query latency (20x faster)
  - Adds ChromaDB + semantic search via sentence-transformers
  - Only implement if needed for production scale

### Key Design Patterns
1. **Observability from Day 1**: LangSmith tracing, structured JSON logging, Prometheus metrics configured before first query
2. **Format-Agnostic Tools**: Generic file discovery & search tools that work with ANY data structure (JSON, CSV, text, nested objects, etc.)
3. **No Domain Coupling**: Tools don't assume fixed schemas - agent dynamically handles any data format
4. **ReAct Pattern**: Agent uses reasoning-action cycles with Google Gemini 1.5 Flash for cost-effective inference
5. **Guardrails**: Input validation (SQL/prompt injection) and output validation (PII detection) via Guardrails AI

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

REMEMBER DATA CAN BE IN ANY FORMAT. NOT NECESSARILY JSONS OR STRUCTURED LIKE 'proyectos.json', 'consultores.json', ETC. `empresa_docs/` IS JUST AN EXAMPLE.

### ⚠️ ChromaDB & Semantic Search (Phase 5+ ONLY)
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
- **DO NOT** run `jupyter notebook` or similar - this is a CLI/API agent
- Use `python agent/bi_agent.py` or similar entry point
- Every query automatically traces to LangSmith UI (https://smith.langchain.com/)
- Check `logs/app.log` for structured JSON logs (parse with `jq` on Unix-like systems)

### Monitoring Stack
- **LangSmith**: Deep LLM observability, trace every agent step, view tool calls and reasoning
- **Prometheus**: Time-series metrics on `/metrics` endpoint, track latency, error rates, tool usage
- **Grafana**: Visual dashboards (runs on :3000), pre-configured for BI agent metrics
- **RAGAS**: Automated evaluation of faithfulness, relevancy, precision (runs in `evaluation/` module)

## Project-Specific Conventions

### File Organization
```
agent/          - Core agent logic (tools, prompts, agent class)
utils/          - Helpers (logging_config, metrics, data_loader)
evaluation/     - RAGAS evaluation suite
monitoring/     - Prometheus + Grafana configs
docs/           - Implementation guides (IMPLEMENTACION_*.md)
empresa_docs/   - Business data (NEVER modify programmatically)
```

### Naming Conventions
- Use Spanish for business domain: `consultores`, `proyectos`, `clientes`
- Use English for technical code: `BiAgent`, `MLflowTracker`, `tool_usage_counter`
- Tools are verbs: `discover_files()`, `read_collection()`, `search_by_text()`
- Metrics use snake_case: `bi_agent_query_duration_seconds`, `tool_usage_counter`

### Logging Standards
All logs must be **structured JSON** with these required fields:
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

Use the `StructuredLogger` class from `utils/logging_config.py`, not raw `logging` module.

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

## Integration Points

### LangChain + Gemini Setup
- Use `ChatGoogleGenerativeAI` from `langchain-google-genai`
- Model: `gemini-2.0-flash` (latest, most capable model)
- Temperature: 0.0 for factual queries, 0.3 for creative synthesis
- Streaming: Disabled by default for evaluation consistency

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

## Common Pitfalls to Avoid

1. **Don't add indexing/ChromaDB before Phase 5**: The MVP works without it. Validate value first.
2. **Don't use collection-specific tools**: Use generic `discover_files()` + `read_collection()` pattern for scalability.
3. **Don't skip LangSmith setup**: It's 5 minutes that saves hours of debugging later.
4. **Don't parse logs manually**: Use structured logging from day 1, query with `jq` or log aggregators.
5. **Don't assume data schema**: JSON files may have nested structures - always inspect before writing filters.
6. **Don't run Jupyter**: This is a ReAct agent, not a notebook analysis project.
7. **⚠️ DO NOT AUTO-GENERATE DOCUMENTATION**: Only create `.md` files when explicitly requested by user with commands like "document this" or "create a guide". Do NOT create summary files, status files, migration guides, or any documentation proactively. Keep the root directory clean and organized.

## Key Files to Reference

- `IMPLEMENTACION_HIBRIDA.md` - Complete 18-day implementation guide with code examples
- `IMPLEMENTACION_POR_FASES.md` - Alternative implementation roadmap
- `CHANGELOG_HYBRID.md` - Architecture evolution decisions and rationale
- `README.md` - User-facing documentation with architecture diagrams
- `agent/tools.py` - Tool implementations (reference for patterns)
- `utils/logging_config.py` - Structured logging setup
- `evaluation/ragas_evaluator.py` - RAGAS evaluation patterns

## Testing Expectations

- Unit tests: 85%+ coverage target
- Integration tests: Test tool chains, not individual tools
- E2E tests: Full query → response cycles with real data
- Evaluation: RAGAS scores > 0.7 for faithfulness, > 0.8 for relevancy
- Performance: < 5s latency for Copilot-like, < 200ms for hybrid

## Quick Reference Commands

```powershell
# Run agent CLI
python cli.py

# Run tests
pytest tests/ -v --cov=agent --cov=utils

# View logs (requires jq or similar)
Get-Content logs\app.log | Select-Object -Last 10

# Start monitoring stack (Phase 3+)
docker-compose up -d

# View metrics
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# MLflow: http://localhost:5000

# Run RAGAS evaluation
python evaluation/ragas_evaluator.py
```
