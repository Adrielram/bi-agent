# 🗺️ Mapa de Estructura del Proyecto (Quick Reference)

Usa este documento como referencia rápida. Para detalles completos, ver `PROJECT_STRUCTURE.md`.

---

## 🎯 ¿Dónde Va Mi Código?

### Si quiero modificar el **agente** → `agent/bi_agent.py`
```python
# ReAct agent orchestrator - Gemini 2.0 Flash
from agent.bi_agent import BiAgent
```

### Si quiero agregar una **herramienta** → `agent/tools.py`
```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """Clear description."""
    return result
```

### Si quiero crear un **endpoint API** → `api/routes/[name].py` (Fase 2+)
```python
from fastapi import APIRouter
router = APIRouter(prefix="/api/v1")

@router.post("/my-endpoint")
async def my_endpoint():
    return {"result": "..."}
```

### Si quiero agregar **seguridad** → `security/[validator].py` (Fase 1.5+)
```python
# security/input_validator.py
def validate_input(query: str) -> bool:
    """Detect SQL injection, prompt injection, etc."""
    return is_safe
```

### Si quiero escribir **tests** → `tests/[unit|integration]/test_[module].py`
```python
# tests/unit/test_agent.py
def test_agent_responds():
    # Test aquí

# tests/integration/test_agent_flow.py
def test_end_to_end_query():
    # E2E test aquí
```

### Si quiero agregar **monitoreo** → `monitoring/prometheus_config.py` (Fase 2+)
```python
from prometheus_client import Counter, Histogram
queries_total = Counter("bi_agent_queries_total", "...")
```

### Si quiero agregar **evaluación** → `evaluation/ragas_evaluator.py` (Fase 3+)
```python
# evaluation/ragas_evaluator.py
from ragas import evaluate
scores = evaluate(dataset, metrics)
```

### Si quiero agregar **logging** → Usar `StructuredLogger` de `utils/logging_config.py`
```python
from utils.logging_config import StructuredLogger
logger = StructuredLogger(__name__)

logger.info("Query executed", extra={
    "user_input": query,
    "latency": 2.34,
    "status": "success"
})
```

---

## 📂 Vista Jerárquica (Simplified)

```
bi-agent/
│
├─ agent/                    🧠 CORE AGENT (Fase 1)
│  ├─ bi_agent.py            Orchestrator
│  ├─ tools.py               Generic tools
│  └─ tools_semantic.py      Semantic search (Fase 5+)
│
├─ api/                      🌐 REST API (Fase 2+)
│  ├─ main.py
│  ├─ routes/                ├─ health.py
│  │                         ├─ query.py
│  │                         └─ admin.py
│  ├─ models/                ├─ request.py
│  │                         └─ response.py
│  └─ middleware/            ├─ auth.py
│                            ├─ rate_limit.py
│                            └─ error_handler.py
│
├─ security/                 🛡️ VALIDATION (Fase 1.5+)
│  ├─ input_validator.py
│  ├─ output_validator.py
│  └─ guardrails_config.py
│
├─ evaluation/               📊 RAGAS (Fase 3+)
│  ├─ ragas_evaluator.py
│  ├─ test_cases.json
│  └─ results/
│
├─ monitoring/               📈 PROMETHEUS (Fase 2+)
│  ├─ prometheus_config.py
│  └─ grafana/
│
├─ mlflow/                   🔬 EXPERIMENTS (Fase 3+)
│  └─ tracker.py
│
├─ utils/                    ⚙️ SHARED
│  ├─ logging_config.py      JSON logging
│  ├─ config.py              Configuration
│  └─ metrics.py             Prometheus setup
│
├─ tests/                    ✅ TESTING
│  ├─ unit/                  test_agent.py, test_tools.py
│  ├─ integration/           test_agent_flow.py, test_api_integration.py
│  ├─ fixtures/              sample_queries.json, mock_responses.json
│  └─ conftest.py
│
├─ empresa_docs/             💼 DATA (READ-ONLY)
│  ├─ proyectos.json
│  ├─ consultores.json
│  ├─ clientes.json
│  ├─ casos_estudio.json
│  └─ ...
│
├─ data/                     📦 PROCESSING
│  ├─ chromadb/              ChromaDB index (Fase 5+)
│  └─ processed/
│
├─ config/                   ⚙️ CONFIGURATION
│  ├─ .env                   SECRETO
│  ├─ .env.example           PÚBLICO
│  ├─ docker-compose.yml
│  └─ prometheus.yml
│
├─ scripts/                  🤖 AUTOMATION
│  ├─ setup_chromadb.py      (Fase 5+)
│  └─ run_evaluation.py      (Fase 3+)
│
├─ docs/                     📖 DOCUMENTATION
│  ├─ IMPLEMENTACION_HIBRIDA.md
│  ├─ API_REFERENCE.md       (Fase 2+)
│  ├─ MONITORING_GUIDE.md    (Fase 2+)
│  ├─ SECURITY_GUIDELINES.md (Fase 1.5+)
│  └─ EVALUATION_GUIDE.md    (Fase 3+)
│
├─ logs/                     📝 OUTPUT
│  ├─ app.log                Structured JSON
│  └─ results/
│
└─ .github/                  🔄 CI/CD
   └─ workflows/             (Fase 4+)
      ├─ test.yml
      ├─ lint.yml
      └─ deploy.yml
```

---

## 📊 Matriz Rápida: Fase → Directorio

| Necesito... | Fase | Directorio | Archivo |
|-----------|------|-----------|---------|
| Agente ReAct | 1 | `agent/` | `bi_agent.py` |
| Herramienta genérica | 1 | `agent/` | `tools.py` |
| Búsqueda semántica | 5 | `agent/` | `tools_semantic.py` |
| Validar input | 1.5 | `security/` | `input_validator.py` |
| Detectar PII | 1.5 | `security/` | `output_validator.py` |
| Endpoint REST | 2 | `api/routes/` | `health.py`, `query.py` |
| Auth API | 2 | `api/middleware/` | `auth.py` |
| Rate limiting | 2 | `api/middleware/` | `rate_limit.py` |
| Métricas Prometheus | 2 | `monitoring/` | `prometheus_config.py` |
| Dashboard Grafana | 2 | `monitoring/` | `grafana/dashboards.json` |
| RAGAS evaluation | 3 | `evaluation/` | `ragas_evaluator.py` |
| MLflow tracking | 3 | `mlflow/` | `tracker.py` |
| Prompt versions | 3 | `agent/prompts/` | `versions/` |
| Docker | 4 | `config/` | `docker-compose.yml` |
| GitHub Actions | 4 | `.github/workflows/` | `test.yml`, `deploy.yml` |
| ChromaDB setup | 5 | `scripts/` | `setup_chromadb.py` |

---

## 🚀 Comandos Comunes (Con venv)

```powershell
# Activar venv PRIMERO
.\venv\Scripts\Activate.ps1

# Ejecutar agente
python main.py
python main.py "Your question here"
python main.py --interactive

# Tests
python -m pytest tests/unit/test_agent.py -v
python -m pytest tests/integration/ -v
python test_fase1_5.py  # Fase 1.5 comprehensive tests

# API (Fase 2+)
python api.py
python test_api.py

# Evaluación (Fase 3+)
python evaluation/ragas_evaluator.py

# Ver logs
Get-Content logs/app.log | ConvertFrom-Json | Format-Table

# Desactivar venv cuando termines
deactivate
```

---

## ✅ Checklist: Antes de Implementar Algo

```
□ 1. ¿En qué Fase? (0-5) → Consultar PROJECT_STRUCTURE.md
□ 2. ¿Dónde va el código? (ver Matriz arriba)
□ 3. ¿Creo tests? (unit + integration)
□ 4. ¿Documenté? (docstrings + type hints)
□ 5. ¿Usé StructuredLogger para logs?
□ 6. ¿Pasaron todos los tests? (100%)
□ 7. ¿Actualicé requirements*.txt?
□ 8. ¿Seguí convenciones? (Spanish para business, English para tech)
□ 9. ¿Documenté en docs/ si es necesario?
□ 10. ¿Pasé venv activation en todos los comandos?
```

---

## 🔗 Enlaces a Documentación

- **Estructura completa**: [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
- **Estado actual**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md)
- **README principal**: [`README.md`](README.md)
- **Quick start**: [`QUICK_START.md`](QUICK_START.md)
- **Arquitectura**: [`IMPLEMENTACION_HIBRIDA.md`](IMPLEMENTACION_HIBRIDA.md)
- **Instrucciones Copilot**: [`.github/copilot-instructions.md`](.github/copilot-instructions.md)

---

## 💡 Tips

1. **Antes de cualquier feature**: Abre `PROJECT_STRUCTURE.md`
2. **¿No recuerdas dónde?**: Usa la Matriz Rápida arriba
3. **¿Necesitas ejemplo?**: Mira la Fase correspondiente en `PROJECT_STRUCTURE.md`
4. **¿Tests?**: Crea `tests/unit/test_[module].py` + `tests/integration/test_[flow].py`
5. **¿Logs?**: Siempre `StructuredLogger` de `utils/logging_config.py`
6. **¿Dependencias?**: Actualiza `requirements*.txt`
7. **¿Documentación?**: Solo crea `.md` cuando se pide explícitamente

---

**Última actualización**: Noviembre 2, 2025

**Estado**: ✅ Fase 1 Completada | 🔄 Fase 1.5 Próxima | 📌 Estructura Definida
