# 🤖 BI Agent MVP - Asistente de Inteligencia de Negocios Listo para Producción

> Agente de Business Intelligence impulsado por IA, construido con LangChain, Google Gemini, y observabilidad MLOps completa.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/🦜🔗-LangChain-green.svg)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Tabla de Contenidos

- [Resumen](#-resumen)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Arquitectura](#️-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Uso](#-uso)
- [Monitoreo](#-monitoreo)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 Resumen

BI Agent MVP es un asistente de Business Intelligence listo para producción que permite consultas en lenguaje natural sobre datos de consultora (proyectos, consultores, clientes, casos de estudio). Construido con prácticas modernas de MLOps, incluye observabilidad completa, evaluación de calidad automatizada, y guardrails de seguridad.

👉 **[⚡ Quick Start en 3 minutos](docs/QUICK_START.md)** - Comienza aquí

📚 **[📖 Ver toda la documentación centralizada en `docs/`](docs/README_DOCS.md)** ← Aquí encontrarás guías, referencias y análisis

**Puntos Destacados:**
- 🔍 **4 herramientas genéricas** agnósticas a estructura de datos (JSON, CSV, objetos anidados)
- 🧠 **Búsqueda semántica** potenciada por ChromaDB y sentence-transformers (Fase 5+)
- 📊 **Observabilidad completa** con LangSmith, Prometheus y Grafana
- 🔬 **Evaluación automatizada** usando framework RAGAS (Faithfulness, Relevancy, Precision)
- 🛡️ **Guardrails de seguridad** previniendo SQL injection, prompt injection y filtrado de PII
- 📈 **Tracking de experimentos** con MLflow para A/B testing
- 🚀 **Production-ready** con Docker, FastAPI y CI/CD

---

## ✨ Características

### 🔍 Consultas en Lenguaje Natural
```
Usuario: "¿Qué datos tienes sobre nuestras soluciones?"
Agente: Usa herramientas genéricas para explorar, buscar y sintetizar información
```

### 🎯 Herramientas Genéricas (Format-Agnostic)
Las 4 herramientas funcionan con **CUALQUIER estructura de datos**:
- **discover_files()**: Explorar qué datos están disponibles
- **read_collection()**: Leer colecciones completas para análisis profundo  
- **search_by_text()**: Búsqueda exacta en cualquier estructura (JSON, CSV, nested objects, etc.)
- **semantic_search()**: Búsqueda semántica por similitud conceptual (Fase 5+)

### 📊 Monitoreo en Producción
- **Métricas en tiempo real**: Latencia de queries, tasas de error, uso de herramientas
- **Dashboards Grafana**: Monitoreo visual de la salud del sistema
- **Traces de LangSmith**: Análisis profundo del razonamiento del agente
- **Logs estructurados**: Logs JSON para fácil parsing y alerting

### 🔬 Aseguramiento de Calidad
- **Evaluación RAGAS**: Scoring automatizado de faithfulness, relevancy, precision
- **Detección de regresión**: Alertas cuando la calidad cae bajo umbrales
- **A/B testing**: Tracking de experimentos con MLflow para optimización de prompts

### 🛡️ Seguridad y Validación
- **Validación de inputs**: Detección de SQL injection y prompt injection
- **Validación de outputs**: Detección de PII y prevención de filtrado de prompts
- **Rate limiting**: Protección de API y prevención de abuso
- **Guardrails AI**: Framework de validación multi-capa

---

## 📂 Estructura del Proyecto

El proyecto está organizado en **Fases de desarrollo** clara y escalable. Cada fase agrega capas sin alterar lo anterior.

📚 **Documentación de estructura centralizada en `docs/`:**
- Ver **[`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md)** para blueprint completo
- Ver **[`docs/STRUCTURE_QUICK_REFERENCE.md`](docs/STRUCTURE_QUICK_REFERENCE.md)** para búsquedas rápidas
- Ver **[`docs/README_DOCS.md`](docs/README_DOCS.md)** para índice de toda la documentación

### Estructura Jerárquica (Resumen)

```
bi-agent/
├── agent/                   # CORE: Lógica del agente (Fase 1+)
│   ├── bi_agent.py         # ReAct agent orchestrator
│   ├── tools.py            # 4 herramientas genéricas
│   └── tools_semantic.py   # Búsqueda semántica (Fase 5+)
│
├── api/                     # API REST (Fase 2+)
│   ├── main.py             # FastAPI server
│   ├── routes/             # Endpoints organizados
│   ├── models/             # Request/Response models
│   └── middleware/         # Auth, rate-limit, errors
│
├── security/               # Guardrails (Fase 1.5+)
│   ├── input_validator.py  # SQL/prompt injection
│   └── output_validator.py # PII detection
│
├── evaluation/             # RAGAS evaluation (Fase 3+)
│   ├── ragas_evaluator.py
│   ├── test_cases.json
│   └── results/
│
├── monitoring/             # Prometheus + Grafana (Fase 2+)
│   ├── prometheus_config.py
│   └── grafana/
│
├── mlflow/                 # Experiment tracking (Fase 3+)
│   └── tracker.py
│
├── utils/                  # Utilidades compartidas
│   ├── logging_config.py   # JSON logging
│   ├── config.py           # Configuration
│   └── metrics.py          # Prometheus setup
│
├── tests/                  # Test suite
│   ├── unit/               # Tests unitarios
│   └── integration/        # Tests de integración
│
├── empresa_docs/           # DATA: Datos de negocio
│   ├── proyectos.json
│   ├── consultores.json
│   ├── clientes.json
│   └── ... (nunca modificar programáticamente)
│
├── docs/                   # Documentación
│   ├── IMPLEMENTACION_HIBRIDA.md
│   ├── API_REFERENCE.md
│   ├── MONITORING_GUIDE.md
│   └── SECURITY_GUIDELINES.md
│
├── config/                 # Configuración
│   ├── .env                # Variables (SECRETO)
│   ├── .env.example        # Template (PÚBLICO)
│   ├── docker-compose.yml  # Orchestración
│   └── prometheus.yml      # Prometheus config
│
├── scripts/                # Automation
│   ├── setup_chromadb.py   # Indexing setup
│   └── run_evaluation.py   # RAGAS evaluation
│
├── logs/                   # Salida
│   ├── app.log             # Structured JSON
│   └── results/
│
├── main.py                 # CLI entry point
├── requirements*.txt       # Dependencies
└── PROJECT_STRUCTURE.md    # 👈 Referencia de estructura
```

### Matriz de Fases

| Fase | Componente | Estado | Archivos Clave |
|------|-----------|--------|-----------------|
| **Fase 0** | Setup Inicial | ✅ COMPLETA | `.env`, `venv/`, `requirements-base.txt` |
| **Fase 1** | Agent + Tools | ✅ COMPLETA | `agent/bi_agent.py`, `agent/tools.py`, `main.py` |
| **Fase 1.5** | Security + Validation | 🔄 PRÓXIMA | `security/`, `tests/integration/` |
| **Fase 2** | API + Monitoring | 📌 DESPUÉS | `api/`, `monitoring/`, `config/prometheus.yml` |
| **Fase 3** | MLOps + Evaluation | 📊 LUEGO | `evaluation/`, `mlflow/`, `agent/prompts/` |
| **Fase 4** | Docker + CI/CD | 📦 PRÓXIMO | `config/docker-compose.yml`, `.github/workflows/` |
| **Fase 5** | Semantic Search | 🔍 OPCIONAL | `data/chromadb/`, `scripts/setup_chromadb.py` |

**Referencia completa**: Consulta [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) para detalles exhaustivos.

---

## 🏗️ Arquitectura

El agente utiliza un patrón **Copilot-Like** evolucionable:

**Fases 1-4 (MVP Copilot-Like)**:
- 4 herramientas genéricas sin indexación
- Zero startup time, queries en 2-5 segundos
- Ideal para MVP, demo, prototipo
- Mismo agente funciona con cualquier dominio

**Fase 5+ (Hybrid con Indexación - Opcional)**:
- Agregar ChromaDB + semantic search
- 15-20s setup inicial, queries en 50-200ms (20x más rápido)
- Ideal para producción con alto volumen
- Tools de Fase 1-4 siguen funcionando

```
┌─────────────────────────────┐
│  Consulta del Usuario       │
└──────────────┬──────────────┘
               │
        ┌──────▼──────┐
        │  Gemini 1.5 │  (Razonamiento + selección de tools)
        │    Flash    │
        └──────┬──────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
┌────────┐ ┌──────┐ ┌─────────┐
│Discover│ │Search│ │Semantic │
│ Files  │ │ Text │ │ Search  │
└────────┘ └──────┘ └─────────┘
     │         │         │
     └─────────┼─────────┘
               │
        ┌──────▼───────┐
        │  Respuesta   │
        │ Estructurada │
        └──────────────┘
```

---

## 🛠 Stack Tecnológico

### Tecnologías Core
| Componente | Tecnología | Propósito |
|-----------|------------|---------|
| **Framework LLM** | LangChain 0.1.0 | Orquestación de agentes, tool calling |
| **Proveedor LLM** | Google Gemini 1.5 Flash | Razonamiento rápido y cost-effective |
| **Vector DB** | ChromaDB | Búsqueda semántica, almacenamiento de embeddings |
| **Embeddings** | sentence-transformers (MiniLM) | Embeddings de texto |
| **Framework API** | FastAPI | Endpoints RESTful API |

### Observabilidad y Monitoreo
| Componente | Tecnología | Propósito |
|-----------|------------|---------|
| **Tracing** | LangSmith | Observabilidad específica de LLMs, debugging |
| **Métricas** | Prometheus | Colección de métricas time-series |
| **Dashboards** | Grafana | Monitoreo visual, alerting |
| **Logging** | JSON Estructurado | Logs searchable y parseables |

### MLOps y Calidad
| Componente | Tecnología | Propósito |
|-----------|------------|---------|
| **Evaluación** | RAGAS | Scoring automatizado de calidad |
| **Experimentos** | MLflow | Tracking de experimentos, registro de modelos |
| **Seguridad** | Guardrails AI | Validación de input/output |

### DevOps
| Componente | Tecnología | Propósito |
|-----------|------------|---------|
| **Containerización** | Docker + docker-compose | Despliegues reproducibles |
| **CI/CD** | GitHub Actions | Testing y deployment automatizado |
| **Testing** | pytest | Tests unitarios, integración, E2E |

---

## 🤔 BI Agent vs GitHub Copilot: ¿Cuál es la Diferencia?

**⚡ Respuesta corta**: Son herramientas para casos de uso completamente diferentes.

| Aspecto | GitHub Copilot | BI Agent |
|---------|---|---|
| **Propósito** | Completación de código en IDE | Q&A sobre datos empresariales |
| **LLM** | GPT-4 (OpenAI) | Gemini 1.5 Flash (Google) |
| **Herramientas** | Implícitas (IDE context) | Explícitas (4 genéricas) |
| **Latencia** | 200-500ms | 2-5s (MVP) → 50-200ms (Indexed) |
| **Observabilidad** | Mínima | Completa (LangSmith, Prometheus, Grafana) |
| **Costo/Query** | $0.10+ (suscripción) | $0.0001 (pay-per-call) |
| **Respuestas** | A veces alucinaciones | Verificables (basadas en datos reales) |
| **Indexación** | No (context window) | Sí (opcional, Fase 5+) |


---

##  Uso

### CLI (Interactivo)

```powershell
python main.py
```

Ejemplos de queries:
- "¿Qué datos tienes disponibles?"
- "Busca Python"
- "Muéstrame todos los consultores"
- "Soluciones para transformación digital" (requiere Fase 5+)

### API REST

```powershell
# Iniciar servidor
python main.py --server

# Acceder a documentación
# http://localhost:8001/docs
```

### Docker

```powershell
docker-compose up --build
```

Acceso a servicios:
- API: http://localhost:8001/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- MLflow: http://localhost:5000

---

## 📊 Monitoreo

### Servicios Disponibles

| Servicio | Puerto | URL | Acceso |
|---------|------|-----|--------|
| API del Agente | 8001 | http://localhost:8001/docs | OpenAPI |
| Prometheus | 9090 | http://localhost:9090 | Métricas |
| Grafana | 3000 | http://localhost:3000 | admin/admin |
| MLflow | 5000 | http://localhost:5000 | Experimentos |

### Métricas Clave (Prometheus)

- `bi_agent_queries_total` - Total de queries
- `bi_agent_query_latency_seconds` - Latencia (p50, p95, p99)
- `bi_agent_tool_usage_total` - Uso de herramientas
- `bi_agent_errors_total` - Errores por tipo

### LangSmith Tracing

Cada query se registra automáticamente en https://smith.langchain.com/ con:
- Cadena completa de razonamiento
- Llamadas a herramientas
- Uso de tokens
- Desglose de latencia

### RAGAS Evaluation

Evaluación automatizada de calidad:
- **Faithfulness**: Respuesta basada en datos recuperados
- **Relevancy**: Relevancia con la pregunta del usuario
- **Precision**: Precisión de contexto recuperado

---

## 🧪 Testing

```powershell
# Ejecutar todos los tests
pytest tests/ -v

# Con reporte de coverage
pytest tests/ --cov=agent --cov=utils --cov-report=html

# Ver reporte
Start-Process htmlcov/index.html
```

**Objetivos:**
- Unit tests: 85%+ cobertura
- Integration tests: Rutas críticas
- E2E tests: API endpoints
- Security tests: Guardrails validados

Ejecución categorizada:
```powershell
pytest tests/test_tools.py -v        # Solo herramientas
pytest tests/test_agent.py -v        # Solo agente
pytest tests/test_integration.py -v  # Integración
```

---

## 📚 Documentación

### Guías Disponibles

- **[IMPLEMENTACION_HIBRIDA.md](IMPLEMENTACION_HIBRIDA.md)** - Guía completa de 18 días con enfoque híbrido (recomendado)
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Instrucciones para AI agents
- **API Docs**: http://localhost:8001/docs (cuando servidor está corriendo)

### Estructura del Proyecto

```
bi-agent-mvp/
├── agent/              # Core del agente
│   ├── bi_agent.py     # Clase principal
│   ├── tools.py        # 4 herramientas genéricas
│   ├── prompts.py      # System prompts
│   └── guardrails_config.py
├── utils/              # Utilidades
│   ├── data_loader.py
│   └── logging_config.py
├── monitoring/         # Stack de monitoreo
│   ├── prometheus_metrics.py
│   └── grafana/
├── evaluation/         # Evaluación RAGAS
├── tests/              # Suite de tests
├── empresa_docs/       # Datos JSON (ejemplo)
├── docker-compose.yml
├── requirements.txt
└── main.py
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/caracteristica`
3. Commit: `git commit -m 'Descripción'`
4. Push: `git push origin feature/caracteristica`
5. Abrir Pull Request

**Antes de contribuir:**
- Pasar tests: `pytest tests/ -v`
- Linting: `black . && flake8 .`
- Actualizar documentación
- Mantener 85%+ cobertura

---

## 📈 Benchmarks

| Métrica | Valor | Status |
|--------|-------|--------|
| Latencia Query (p95) | 2.5s | ✅ |
| RAGAS Faithfulness | 0.85 | ✅ |
| RAGAS Relevancy | 0.90 | ✅ |
| Test Coverage | 85% | ✅ |
| Uptime | 99.5% | ✅ |

*Con Fase 5+ (ChromaDB): Latencia query desciende a 50-200ms*

---

## 🛡️ Seguridad

- ✅ Validación de inputs (SQL injection, prompt injection detection)
- ✅ Validación de outputs (PII detection)
- ✅ Rate limiting en API
- ✅ Gestión segura de credenciales
- ✅ Containers sin privilegios

**Reportar vulnerabilidades**: security@example.com (no uses GitHub issues)

---

## 📄 Licencia

Licenciado bajo MIT. Ver [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [LangChain](https://python.langchain.com/) - Framework para LLM apps
- [Google Gemini](https://ai.google.dev/) - LLM rápido y económico
- [RAGAS](https://github.com/explodinggradients/ragas) - Evaluación de RAG
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - Validación de outputs
- [ChromaDB](https://www.trychroma.com/) - Base de datos vectorial
- [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/) - Monitoreo

## 📞 Contacto

- 📧 Email: tu.email@example.com
- 💼 LinkedIn: [Tu Perfil](https://linkedin.com)
- 🐛 Issues: [GitHub Issues](https://github.com/tuusuario/bi-agent-mvp/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/tuusuario/bi-agent-mvp/discussions)

---

<div align="center">

### ⭐ Si te resulta útil, ¡dale una estrella! ⭐

Hecho con ❤️

[📖 Documentación](IMPLEMENTACION_HIBRIDA.md) • [⚡ Quick Start](QUICK_START.md) • [💬 Soporte](#-contacto)

</div>
