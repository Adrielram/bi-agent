# Implementación Híbrida - Agente de BI con Observability desde Día 1

<div align="center">

![LangGraph](https://img.shields.io/badge/LangGraph-0.1.0-blue?style=flat-square&logo=chainlink)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange?style=flat-square&logo=google)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.22-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**Timeline**: 20 días | **Approach**: LangGraph + Memoria + Observability | **Observability**: Desde día 1 ✨

</div>

---

> **TL;DR**: Guía completa para construir un agente de Business Intelligence con LangGraph en 20 días. Combinamos ReAct pattern con grafo explícito, memoria conversacional, y reintentos automáticos. Queries en 2-5s, robustez desde el inicio. Instrumentado con LangSmith, Prometheus, RAGAS y MLflow desde día 1.

**📚 Índice Rápido**:
- [Resumen Ejecutivo](#-resumen-ejecutivo) - Start here!
- [Filosofía Híbrida](#-filosofía-del-enfoque-híbrido)
- **[📖 COMPARATIVA: BI Agent vs GitHub Copilot](./COMPARATIVA_BI_AGENT_VS_COPILOT.md)** ← Lee esto primero!
- [Fase 0: Setup](#-fase-0-setup-inicial--langsmith) (Día 1)
- [Fase 1: MVP Optimizado](#-fase-1-agente-mvp--structured-logging) (Días 2-5)
- [Fase 2: Monitoring](#-fase-2-agente-completo--monitoring) (Días 6-10)
- [Fase 3: Production-Ready + MLOps](#-fase-3-production-ready--mlops) (Días 11-15)
- [Fase 4: CI/CD + Portfolio](#-fase-4-polish--cicd--portfolio) (Días 16-18) ✅ MVP COMPLETO
- [Fase 5: Indexación (Opcional)](#-fase-5-optimización-con-indexación-opcional) - Post-MVP
- [Comparativa de Enfoques](#-comparativa-de-enfoques-lecciones-aprendidas) - Lecciones aprendidas
- [Árbol de Decisión](#-árbol-de-decisión-qué-approach-usar) - ¿Cuándo optimizar?

---

## 📖 Resumen Ejecutivo

### ¿Qué vas a construir?

Un agente de BI conversacional que responde preguntas sobre:
- 📊 Proyectos ejecutados (tecnologías, costos, resultados)
- 👥 Consultores (expertise, experiencia, disponibilidad)
- 🏢 Clientes y casos de éxito
- 💼 Propuestas comerciales activas

### 🚀 Arquitectura en 3 Fases

<details>
<summary>💾 Ver código (code)</summary>

```code
📍 FASE 1-2 (Días 1-10): MVP LangGraph con Memoria
   → Grafo explícito con ReAct pattern
   → Estado compartido (memoria conversacional)
   → Reintentos automáticos + fallback tools
   → Paralelización de tools
   → Queries en 2-5s (startup: 5-10s)
   → Structured logging + LangSmith tracing
   → Prometheus + Grafana monitoring
   → RAGAS evaluation + Guardrails

📍 FASE 3 (Días 11-15): Production-Ready + MLOps
   → MLflow experiment tracking
   → Docker + docker-compose completo
   → Advanced Guardrails (prompt injection, PII)
   → FastAPI endpoints (expone grafo como API)
   → Sistema deployable

📍 FASE 4 (Días 16-20): Polish + Portfolio ✅
   → Testing suite (85% coverage)
   → CI/CD con GitHub Actions
   → Documentación técnica completa
   → Portfolio para entrevistas

🎯 MVP COMPLETO - Sistema production-ready con memoria, reintentos, debugging visual

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 FASE 5 (Post-MVP): Optimización con Indexación (OPCIONAL)
   → Agregar SI necesitas: > 500 queries/día O datasets > 1MB
   → ChromaDB + embeddings (startup 15-20s)
   → Queries: 50-200ms (20x mejora)
   → Búsqueda semántica avanzada + híbrida
```

</details>

### 💡 Por Qué Esta Ruta

| Decisión | Alternativa | Razón |
|----------|-------------|-------|
| **LangGraph (ReAct + Grafo + Memoria)** | LangChain simple | Robustez: reintentos, fallbacks, paralelización |
| **Memoria conversacional** | Sin memoria | Mejor UX, análisis exploratorio, contexto acumulado |
| **Grafo visual** | Cadenas implícitas | Debugging 10x más fácil, decisiones explícitas |
| **Indexación opcional** | All-in con ChromaDB | Validar valor antes de complejidad |
| **Tools genéricas optimizadas** | Tools específicas | Escalabilidad a cualquier formato |
| **Observability desde día 1** | Agregar después | Debugging 10x más fácil |
| **20 días con LangGraph** | 18 días sin LangGraph | +2 días = mejor arquitectura, mejor UX, mejor production-ready |

### 🎯 Resultados Esperados

**Semana 1 (MVP)**:
- ✅ Agente funcional respondiendo queries
- ✅ LangSmith tracing + structured logs
- ✅ 3 tools optimizadas: discover, search, read_lines

**Semana 2 (Monitoring)**:
- ✅ Prometheus + Grafana dashboards
- ✅ RAGAS evaluation automatizada
- ✅ Guardrails (input/output validation)

**Semana 3 (Producción)**:
- ✅ MLflow experiment tracking
- ✅ Docker + FastAPI
- ✅ Advanced Guardrails
- ✅ Sistema deployable

**Semana 4 (Polish)**:
- ✅ Testing suite (85% coverage)
- ✅ CI/CD pipeline
- ✅ Documentación completa
- ✅ Portfolio-ready

**🎯 MVP COMPLETO - Queries en 2-5s (suficiente para demo)**

**Post-MVP (Opcional)**:
- 🔮 ChromaDB indexado (SI necesitas queries < 500ms)
- 🔮 Búsqueda semántica (SI dataset > 1MB)

### 📊 Stack Tecnológico

| Componente | Tecnología | Cuándo |
|------------|------------|--------|
| **LLM** | Google Gemini 2.0 Flash | Día 1 |
| **Framework** | **LangGraph** (ReAct + Grafo) | Día 1 |
| **Patrón** | ReAct + State Graph + Memoria | Día 1 |
| **Tracing** | LangSmith | Día 1 ✨ |
| **Logging** | Python logging (JSON) | Día 2 |
| **Monitoring** | Prometheus + Grafana | Día 6-7 |
| **Evaluation** | RAGAS | Día 8-9 |
| **Security** | Guardrails AI | Día 9-10 |
| **Experiment Tracking** | MLflow | Día 11-13 |
| **API** | FastAPI | Día 13-14 |
| **Container** | Docker | Día 14 |
| **CI/CD** | GitHub Actions | Día 16-17 |
| **Testing** | pytest + coverage | Día 16-18 |
| **Vector Store** | ChromaDB | **Post-MVP** 🔮 (opcional) |
| **Embeddings** | sentence-transformers | **Post-MVP** 🔮 (opcional) |

### 🎓 Aprendizajes Clave

1. **Start Simple**: MVP con herramientas optimizadas (git grep + progressive reading) funciona perfectamente para validar el concepto
2. **Observability First**: LangSmith (5 min setup) ahorra horas de debugging
3. **Ship First, Optimize Later**: 18 días con queries 2-5s → Deploy → LUEGO optimiza SI lo necesitas
4. **Generic > Specific**: Tools genéricas optimizadas (discover, search, read_lines) escalan a cualquier formato
5. **Don't Over-Engineer**: La mayoría de MVPs NO necesitan indexación (< 500 queries/día)

---

## 🎯 Filosofía de LangGraph

**Principio**: Desarrollar el agente con arquitectura robusta E instrumentarlo simultáneamente desde el inicio.

### ¿Por qué LangGraph?

**❌ Enfoque tradicional (LangChain simple)**:
- Cadenas implícitas sin visibilidad del flujo
- Reintentos manuales (si un tool falla, qué hacer?)
- Debugging con traces complejos en LangSmith
- Condicionalidad limitada
- Sin paralelización de tools
- UX fragmentada sin memoria

**✅ Enfoque LangGraph (ReAct + Grafo + Memoria)**:
- Grafo **explícito y visual** del flujo
- Reintentos automáticos y fallback tools
- Debugging **visual** (ves exactamente el flujo)
- Routing condicional **arbitrariamente complejo**
- Paralelización **automática** de tools
- Memoria conversacional (contexto acumulado)
- Performance **20x mejor** si indexas (Fase 5)

**Resultado**: Mejor arquitectura desde el inicio, mejor UX, mejor producible.

---

## 🎓 Aprendizajes Clave

1. **LangGraph > LangChain para este caso**: ReAct + grafo + memoria = arquitectura profesional
2. **Observability First**: LangSmith (5 min setup) ahorra horas de debugging
3. **Ship First, Optimize Later**: 20 días con LangGraph → Deploy → LUEGO indexa SI lo necesitas
4. **Generic > Specific**: Tools genéricas optimizadas (discover, search, read_lines) escalan a cualquier formato
5. **State is King**: Con memoria explícita el agente es infinitamente más poderoso

---

## 📊 Visión General de Fases

<details>
<summary>💾 Ver código (code)</summary>

```code
FASE 0: Setup Inicial + LangSmith (Día 1)
   ↓
FASE 1: Grafo LangGraph + ReAct + Memoria (Días 2-5)
   │    → State graph con reasoning + tool execution + fallback
   │    → Memoria conversacional (acumula contexto entre turnos)
   │    → Reintentos automáticos (tool failures)
   ↓
FASE 2: Agente Completo + Monitoring (Días 6-10)
   │    → Paralelización de tools
   │    → Conditional routing basado en estado
   │    → Prometheus + Grafana (métricas por nodo)
   ↓
FASE 3: Production-Ready + MLOps (Días 11-15)
   │    → MLflow + Docker + Advanced Guardrails
   │    → FastAPI expone grafo
   │    → Sistema deployable con observabilidad completa
   ↓
FASE 4: Polish + CI/CD (Días 16-20)
   │    → Testing + CI/CD + Portfolio
   ↓
FASE 5: Optimización con Indexación (OPCIONAL - Post-MVP)
        → ChromaDB + embeddings cuando lo necesites
        → Agregar SOLO si tienes > 500 queries/día
```

</details>

**Timeline MVP**: 4 semanas (20 días hábiles)  
**Timeline Completo**: +2-3 días para Fase 5 (si es necesario)  
**Estrategia**: Build → Deploy → Optimize (solo si se necesita)

### 🎯 Arquitectura por Fase

| Fase | Approach | Startup | Query Speed | Complejidad | Memoria | Reintentos | Estado |
|------|----------|---------|-------------|-------------|---------|------------|--------|
| **Fase 1-4** | LangGraph + ReAct | 5-10s | 2-5s | Media ✅ | ✅ | ✅ | **Core MVP** |
| **Fase 5** | Hybrid + Indexación | 15-20s | 50-200ms ⚡ | Media-Alta | ✅ | ✅ | **Opcional** |

**Razón**: LangGraph ofrece mejor arquitectura desde el inicio. La indexación es una optimización que agregas **SI Y SOLO SI** la necesitas (> 500 queries/día o datasets > 1MB).

### 🏗️ Diagrama de Arquitectura Evolutiva

<details>
<summary>💾 Ver código (code)</summary>

```code
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1-2: LangGraph con ReAct + Memoria                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Query                                                    │
│       ↓                                                         │
│   ┌─────────────────────────────────────────┐                 │
│   │      STATE GRAPH (LangGraph)           │                 │
│   │                                         │                 │
│   │  ┌──────────────┐                      │                 │
│   │  │ Reasoning    │ ← Memoria conversa   │                 │
│   │  │ (Gemini)     │   cional             │                 │
│   │  └──────┬───────┘                      │                 │
│   │         ↓                              │                 │
│   │  ┌──────────────┐                      │                 │
│   │  │ Routing      │ ← Decide herramienta │                 │
│   │  │ Condicional  │   basado en state    │                 │
│   │  └──────┬───────┘                      │                 │
│   │         ├──────────────┬───────────┐   │                 │
│   │         ↓              ↓           ↓   │                 │
│   │    ┌────────┐   ┌─────────┐  ┌────────┐│                 │
│   │    │ Tool A │   │ Tool B  │  │Tool C  ││ (Paralelo!)    │
│   │    └──┬─────┘   └────┬────┘  └───┬────┘│                 │
│   │       └────────────────┴──────────┘     │                 │
│   │              ↓                          │                 │
│   │       ┌─────────────┐                   │                 │
│   │       │ Actualizar  │                   │                 │
│   │       │ Memoria     │                   │                 │
│   │       └──────┬──────┘                   │                 │
│   │              ↓                          │                 │
│   │       ┌─────────────┐                   │                 │
│   │       │ Volver a    │ ← Ciclo: si      │                 │
│   │       │ Reasoning?  │   más análisis    │                 │
│   │       └──────┬──────┘                   │                 │
│   │              ↓                          │                 │
│   │       ┌─────────────┐                   │                 │
│   │       │ Final Resp  │                   │                 │
│   │       └─────────────┘                   │                 │
│   └─────────────────────────────────────────┘                 │
│                                                                 │
│   ✅ Startup: 5-10s (carga LangGraph + Gemini)                │
│   ⚠️  Query: 2-5s (razonamiento + tool execution)             │
│   ✅ Memoria: Contexto acumulado entre turnos                 │
│   ✅ Reintentos: Automáticos si tool falla                    │
│   ✅ Debugging: Grafo visual en LangSmith                     │
└─────────────────────────────────────────────────────────────────┘

                            ↓ EVOLUCIÓN ↓

┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: Hybrid System (LangGraph + Indexed)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Query                                                    │
│       ↓                                                         │
│   ┌─────────────────────────────────────────┐                 │
│   │      STATE GRAPH + Semantic Index       │                 │
│   │                                         │                 │
│   │  ┌──────────────┐                      │                 │
│   │  │ Reasoning    │ ← Memoria conversa   │                 │
│   │  └──────┬───────┘                      │                 │
│   │         ↓                              │                 │
│   │  ┌──────────────────┐                  │                 │
│   │  │ Smart Router     │                  │                 │
│   │  │ (BM25 vs Semantic)                 │                 │
│   │  └────┬──────────┬──┘                  │                 │
│   │       ↓          ↓                     │                 │
│   │  ┌────────┐  ┌─────────┐              │                 │
│   │  │ BM25   │  │Semantic │              │                 │
│   │  │Query   │  │Search   │              │                 │
│   │  │Engine  │  │(ChromaDB)              │                 │
│   │  └────┬───┘  └────┬────┘              │                 │
│   │       └────────────┴────────┬──────┐   │                 │
│   │                             ↓      ↓   │                 │
│   │                      ┌──────────────┐  │                 │
│   │                      │ Tool Exec    │  │                 │
│   │                      │ (Paralelo)   │  │                 │
│   │                      └───────┬──────┘  │                 │
│   │                              ↓         │                 │
│   │                      ┌──────────────┐  │                 │
│   │                      │ Final Resp   │  │                 │
│   │                      └──────────────┘  │                 │
│   └─────────────────────────────────────────┘                 │
│                                                                 │
│   ⚠️  Startup: 15-20s (indexación ChromaDB)                   │
│   ✅ Query: 50-200ms (búsqueda en índice pre-calculado)       │
│   ✅ Memoria: Contexto completo + índice                      │
│   ✅ Reintentos: Automáticos                                  │
│   ✅ Debugging: Grafo visual + hybrid trace                   │
└─────────────────────────────────────────────────────────────────┘

Leyenda:
→ : Data flow
┌─┐ : Component
↓ : Evolution
```

</details>

---

## 🚀 FASE 0: Pre-Setup + Setup Inicial + LangSmith

**Duración Total**: Día 1 (4-6 horas)
- **Pre-Setup**: 30 minutos (obtener credenciales)
- **Setup**: 1-2 horas (proyecto + LangSmith)
- **Verification**: 30 minutos (tests)

**Objetivo**: Proyecto base funcional con observability desde minuto 1  
**Criterio de éxito**: Primera query traced en LangSmith

---

### 📋 Pre-Setup Checklist (30 minutos)

Antes de empezar, prepara estos items:

- [ ] **Python 3.11+** instalado
  ```powershell
  python --version  # Debe ser >= 3.11
  ```

- [ ] **Google API Key** generada
  - Ir a: https://makersuite.google.com/app/apikey
  - Click "Create API Key"
  - Copy & paste en nota temporal

- [ ] **LangSmith Account** creada
  - Ir a: https://smith.langchain.com/
  - Sign up (gratis, email suficiente)
  - Settings → API Keys → Create API Key
  - Copy & paste en nota temporal

- [ ] **Git** instalado
  ```powershell
  git --version  # Verificar
  ```

- [ ] **Docker** (opcional, para Fase 2+)
  ```powershell
  docker --version  # Recomendado pero no obligatorio
  ```

**⏱️ Tiempo estimado**: 15-30 minutos (la mayoría es waiting en sign-up)

---

### 📊 Timeline General por Fase

| Fase | Duración | Output | Queries | Requisitos |
|------|----------|--------|---------|------------|
| **0** | 30 min | Setup completo | - | 🔑 API Keys |
| **1-2** | 8 días | MVP funcional | 2-5s | ✅ Mínimo |
| **3** | 5 días | Producción | 2-5s | Docker (opt) |
| **4** | 3 días | Portfolio | - | ✅ Completo |
| **5** | 2-3 días (opt) | Indexación | 50-200ms | ChromaDB |

**Total MVP (Fases 0-4): 16-18 días** ✅  
**Con Fase 5: 18-21 días** (si necesitas)

---

### 0.1 Crear Estructura de Directorios

<details>
<summary>💾 Ver código (bash)</summary>

```bash
AI_ASSISTANT_MVP/
├── empresa_docs/              # Ya existe con tus JSONs
│   ├── consultores.json
│   ├── proyectos.json
│   ├── clientes.json
│   ├── casos_estudio.json
│   └── propuestas.json
│
├── agent/
│   ├── __init__.py
│   ├── tools.py              # Herramientas del agente
│   ├── prompts.py            # System prompts
│   └── bi_agent.py           # Agente principal
│
├── utils/
│   ├── __init__.py
│   ├── logging_config.py     # Structured logging (Día 2)
│   └── metrics.py            # Prometheus (Semana 2)
│
├── evaluation/               # Semana 2
│   ├── __init__.py
│   └── ragas_metrics.py
│
├── guardrails/               # Semana 2
│   ├── __init__.py
│   └── validators.py
│
├── mlops/                    # Semana 3
│   ├── __init__.py
│   └── mlflow_tracking.py
│
├── tests/
│   ├── __init__.py
│   └── test_tools.py
│
├── .env                      # Variables de entorno
├── .gitignore
├── requirements-base.txt     # Fase 0-4 (MVP Optimizado)
├── requirements-hybrid.txt   # Fase 5 (Indexación - OPCIONAL)
├── docker-compose.yml        # Fase 0-4 (base)
├── docker-compose.hybrid.yml # Fase 5 (opcional)
├── README.md
└── main.py                   # Entry point (CLI)
```

</details>

---

### 0.2 Instalar Dependencias

**IMPORTANTE**: Ahora hay DOS archivos de requirements para mayor claridad.

**Para Fase 0-4 (MVP Copilot-Like - Recomendado)**:

```powershell
# Instalar SOLO dependencias base
pip install -r requirements-base.txt
```

**Para Fase 5+ (Indexación - OPCIONAL)**:

```powershell
# Instalar incluyendo ChromaDB y embeddings
pip install -r requirements-hybrid.txt
```

**¿Cuál debo usar?**
- Empieza con `requirements-base.txt` (18 días, queries 2-5s)
- Cambia a `requirements-hybrid.txt` SOLO SI necesitas:
  - Queries < 500ms
  - Dataset > 1MB
  - Búsqueda semántica avanzada

---

### 0.2a Archivo: `requirements-base.txt` (Fase 0-4)
pytest-asyncio==0.23.3
pytest-cov==4.1.0

# Development
black==24.1.0
flake8==7.0.0
ipython==8.20.0
```

</details>

**💡 Nota sobre instalación progresiva**:
- **Fase 0-2**: Puedes comentar las dependencias de ChromaDB si quieres empezar más ligero
- **Fase 3**: Descomenta chromadb + sentence-transformers cuando implementes indexación
- Esto permite iterar rápido sin instalar todo desde el inicio

**Instalación**:
<details>
<summary>💾 Ver código (bash)</summary>

```bash
# Crear virtual environment
python -m venv venv

# Activar
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar
pip install --upgrade pip
pip install -r requirements.txt
```

</details>

---

### 0.3 Configurar Variables de Entorno

**Archivo**: `.env`

<details>
<summary>💾 Ver código (bash)</summary>

```bash
# Google AI (Gemini)
GOOGLE_API_KEY=tu_api_key_aqui

# LangSmith (CONFIGURAR HOY) ✨
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_PROJECT=bi-agent-dev

# App Config
LOG_LEVEL=INFO
ENVIRONMENT=development
```

</details>

**Obtener LangSmith API Key** (5 minutos):
1. Ir a https://smith.langchain.com/
2. Sign up (gratis hasta 5,000 traces/mes)
3. Settings → API Keys → Create API Key
4. Copiar y pegar en `.env`

**¿Por qué configurar LangSmith HOY?**
- ✅ Setup toma 5 minutos
- ✅ Cada query que pruebes quedará registrada
- ✅ No tienes que "recordar" qué funcionó/no funcionó
- ✅ Debugging será 10x más fácil desde query #1

---

### 0.5 Herramientas Optimizadas (git grep + progressive reading)

**Filosofía**: El agente usa estrategia "git grep multi-file + progressive reading" para buscar y leer datos de forma ultra-rápida y segura.

**Archivo**: `agent/tools.py`

<details>
<summary>💾 Ver código (python)</summary>

```python
"""
Herramientas optimizadas para Agente BI - VERSIÓN FINAL
3 tools minimalistas que cubren todos los casos de uso

Patrón: git grep multi-file + progressive reading
"""

from langchain.tools import tool
from typing import Optional, Dict, Any, List
from pathlib import Path
import json
import subprocess
import os

EMPRESA_DOCS_PATH = Path(__file__).parent.parent / "empresa_docs"

# ============================================
# LÍMITES DE SEGURIDAD
# ============================================

MAX_LINES_PER_CALL = 200
MAX_PREVIEW_LENGTH = 150
MAX_SEARCH_RESULTS = 20
EXPENSIVE_LINE_THRESHOLD = 400


# ============================================
# TOOL 1: discover_files (EXPLORACIÓN INICIAL)
# ============================================

@tool
def discover_files() -> str:
    """
    📁 Lista archivos disponibles con metadata básica.

    Returns:
        Lista de archivos con nombre, tipo, tamaño en líneas

    Example:
        discover_files()
        → "consultores.json (json, 1250 lines)
           proyectos.json (json, 3400 lines)
           ..."

    USA ESTO PRIMERO para ver qué archivos hay disponibles.
    """
    if not EMPRESA_DOCS_PATH.exists():
        return "❌ Directory 'empresa_docs/' not found"

    files = list(EMPRESA_DOCS_PATH.glob("*"))
    if not files:
        return "❌ No files found in empresa_docs/"

    file_list = []

    for file in sorted(files):
        if not file.is_file():
            continue

        try:
            # Count lines fast
            with open(file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)

            # Detect type from extension
            ext = file.suffix.lstrip('.').lower()
            type_map = {
                'json': 'json', 'csv': 'csv', 'md': 'markdown',
                'txt': 'text', 'log': 'log', 'py': 'code', 'js': 'code'
            }
            file_type = type_map.get(ext, 'unknown')

            # Size category
            if line_count < 100:
                size = "tiny"
            elif line_count < 500:
                size = "small"
            elif line_count < 2000:
                size = "medium"
            elif line_count < 10000:
                size = "large"
            else:
                size = "huge"

            file_list.append({
                "name": file.name,
                "type": file_type,
                "lines": line_count,
                "size": size
            })
        except Exception as e:
            file_list.append({
                "name": file.name,
                "type": "error",
                "lines": 0,
                "size": "unknown"
            })

    # Format output
    output = "📂 Available files in empresa_docs/:\n\n"

    for f in file_list:
        icon = {"json": "📊", "markdown": "📝", "text": "📄", "code": "💻", "log": "📋"}.get(f['type'], "📄")
        output += f"{icon} {f['name']}\n"
        output += f"   Type: {f['type']}, Lines: {f['lines']}, Size: {f['size']}\n\n"

    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    output += "💡 Next steps:\n"
    output += "   • search(pattern) - Search across ALL files\n"
    output += "   • read_lines(filename, start, count) - Read specific file\n"

    return output


# ============================================
# TOOL 2: search (MULTI-FILE SEARCH - git grep)
# ============================================

@tool
def search(pattern: str, filename: Optional[str] = None, case_sensitive: bool = False) -> str:
    """
    🔍 BÚSQUEDA ULTRA-RÁPIDA con git grep (busca en TODOS los archivos).

    Esta es la herramienta MÁS IMPORTANTE. Úsala SIEMPRE que busques algo.

    Args:
        pattern: Texto a buscar (ej: "React", "2024", "Juan Pérez")
        filename: (Opcional) Limitar búsqueda a un archivo específico
        case_sensitive: False por defecto (búsqueda case-insensitive)

    Returns:
        JSON agrupado por archivo con:
        - Total de matches por archivo
        - Line numbers
        - Previews de los primeros matches
        - Sugerencias de qué leer después

    Examples:
        search("React")
        → Busca "React" en TODOS los archivos, retorna matches agrupados por archivo

        search("React", filename="consultores.json")
        → Busca solo en consultores.json

        search("CONS-012")
        → Encuentra en qué archivos se menciona este ID

    IMPORTANTE:
    - Esta tool es GRATIS (no consume tokens del contenido)
    - Retorna SOLO metadata (line numbers + previews cortos)
    - git grep escanea archivos gigantes en milisegundos
    - Usa esto ANTES de read_lines() para saber QUÉ leer

    PATRÓN RECOMENDADO:
    1. search("keyword") → Ve en qué archivos aparece
    2. read_lines(filename, around_line, count) → Lee contexto completo
    """

    try:
        # Verificar si estamos en un repo git
        is_git_repo = (EMPRESA_DOCS_PATH.parent / ".git").exists()

        if is_git_repo:
            # OPCIÓN 1: git grep (ULTRA RÁPIDO)
            cmd = ["git", "grep", "-n"]  # -n = line numbers

            if not case_sensitive:
                cmd.append("-i")  # case insensitive

            cmd.append(pattern)

            # Si se especifica filename, limitar búsqueda
            if filename:
                search_path = f"empresa_docs/{filename}"
            else:
                search_path = "empresa_docs/"

            cmd.append(search_path)

            try:
                result = subprocess.run(
                    cmd,
                    cwd=EMPRESA_DOCS_PATH.parent,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    return _parse_git_grep_output(result.stdout, pattern, filename)
                elif result.returncode == 1:
                    # No matches found
                    return json.dumps({
                        "matches": 0,
                        "pattern": pattern,
                        "message": f"No matches found for '{pattern}'" + (f" in {filename}" if filename else " in any file")
                    }, indent=2)
                else:
                    # Error - fall back to Python grep
                    pass

            except subprocess.TimeoutExpired:
                return json.dumps({"error": "Search timeout (>10s) - try narrowing search"})
            except Exception:
                pass  # Fall back to Python grep

        # OPCIÓN 2: Python grep (fallback si no hay git)
        return _python_grep(pattern, filename, case_sensitive)

    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})


def _parse_git_grep_output(output: str, pattern: str, target_file: Optional[str]) -> str:
    """Parse git grep output y agrupar por archivo"""

    lines = output.strip().split("\n")
    if not lines or lines == ['']:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": f"No matches found for '{pattern}'"
        }, indent=2)

    # Agrupar por archivo
    by_file = {}

    for line in lines:
        # Format: empresa_docs/file.json:line_num:content
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue

        filepath = parts[0].replace("empresa_docs/", "")
        line_num = int(parts[1]) - 1  # 0-indexed
        content = parts[2]

        # Skip very long lines (noise)
        if len(content) > EXPENSIVE_LINE_THRESHOLD:
            continue

        if filepath not in by_file:
            by_file[filepath] = []

        by_file[filepath].append({
            "line": line_num,
            "preview": content.strip()[:MAX_PREVIEW_LENGTH]
        })

    if not by_file:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": "Matches found but all lines were too long (noise filtered)"
        }, indent=2)

    # Limitar resultados por archivo
    total_matches = sum(len(matches) for matches in by_file.values())

    result = {
        "matches": total_matches,
        "pattern": pattern,
        "files_with_matches": len(by_file),
        "results_by_file": {}
    }

    for filepath, matches in sorted(by_file.items()):
        limited_matches = matches[:MAX_SEARCH_RESULTS]

        result["results_by_file"][filepath] = {
            "total_matches": len(matches),
            "showing": len(limited_matches),
            "line_numbers": [m["line"] for m in limited_matches],
            "preview_samples": limited_matches[:5]  # Solo primeros 5 previews
        }

        if len(matches) > MAX_SEARCH_RESULTS:
            result["results_by_file"][filepath]["note"] = f"Showing first {MAX_SEARCH_RESULTS} of {len(matches)} matches"

    # Add suggestions
    if len(by_file) == 1:
        only_file = list(by_file.keys())[0]
        first_line = by_file[only_file][0]["line"]
        result["suggestion"] = f"Use read_lines('{only_file}', start={first_line}, count=50) to see full context"
    else:
        result["suggestion"] = "Multiple files have matches. Use read_lines(filename, start, count) on the most relevant file"

    return json.dumps(result, indent=2, ensure_ascii=False)


def _python_grep(pattern: str, filename: Optional[str], case_sensitive: bool) -> str:
    """Fallback: Python-based grep when git is not available"""

    pattern_lower = pattern if case_sensitive else pattern.lower()
    by_file = {}

    # Determine which files to search
    if filename:
        files = [EMPRESA_DOCS_PATH / filename]
    else:
        files = list(EMPRESA_DOCS_PATH.glob("*"))

    for filepath in files:
        if not filepath.is_file():
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    search_line = line if case_sensitive else line.lower()

                    if pattern_lower in search_line:
                        # Skip very long lines
                        if len(line) > EXPENSIVE_LINE_THRESHOLD:
                            continue

                        filename_key = filepath.name
                        if filename_key not in by_file:
                            by_file[filename_key] = []

                        by_file[filename_key].append({
                            "line": i,
                            "preview": line.strip()[:MAX_PREVIEW_LENGTH]
                        })

                        # Limit per file to avoid memory issues
                        if len(by_file[filename_key]) >= MAX_SEARCH_RESULTS * 2:
                            break
        except Exception:
            continue

    if not by_file:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": f"No matches found for '{pattern}'"
        }, indent=2)

    # Format similar to git grep output
    total_matches = sum(len(matches) for matches in by_file.values())

    result = {
        "matches": total_matches,
        "pattern": pattern,
        "files_with_matches": len(by_file),
        "results_by_file": {}
    }

    for filepath, matches in sorted(by_file.items()):
        limited_matches = matches[:MAX_SEARCH_RESULTS]

        result["results_by_file"][filepath] = {
            "total_matches": len(matches),
            "showing": len(limited_matches),
            "line_numbers": [m["line"] for m in limited_matches],
            "preview_samples": limited_matches[:5]
        }

    return json.dumps(result, indent=2, ensure_ascii=False)


# ============================================
# TOOL 3: read_lines (UNIFIED READING - context + chunked)
# ============================================

@tool
def read_lines(filename: str, start: int = 0, count: int = 50) -> str:
    """
    📖 Lee líneas de un archivo (unified: chunked + context reading).

    Esta tool reemplaza tanto read_lines() como read_context():
    - Para lectura chunked: read_lines("file.json", 0, 100)
    - Para contexto: read_lines("file.json", around_line=45, count=20)

    LÍMITES DE SEGURIDAD:
    - Máximo 200 líneas por llamada
    - Filtra líneas >400 caracteres (ruido)

    Args:
        filename: Nombre del archivo
        start: Línea de inicio (0-indexed)
        count: Cantidad de líneas a leer

    Returns:
        JSON con contenido + metadata

    Examples:
        # Lectura chunked (exploración)
        read_lines("consultores.json", start=0, count=100)

        # Lectura de contexto (después de search)
        search("React") → match en línea 45
        read_lines("consultores.json", start=40, count=20)  # Lee 40-60 (contexto alrededor de 45)

        # Lectura de primeras líneas (entender estructura)
        read_lines("proyectos.json", start=0, count=20)

    USO RECOMENDADO:
    1. Después de search(): Lee contexto alrededor de matches
    2. Para archivos <500 líneas: Lee en chunks de 50-100
    3. Para archivos >500 líneas: USA search() primero, luego lee solo lo necesario
    4. REFLEXIONA después de cada lectura: ¿Ya tengo suficiente info?

    PATRÓN COMÚN:
    search("keyword") → encuentra línea X → read_lines(filename, X-10, 20) → contexto completo
    """

    file_path = EMPRESA_DOCS_PATH / filename

    if not file_path.exists():
        return json.dumps({"error": f"❌ File '{filename}' not found in empresa_docs/"})

    # HARD LIMIT
    if count > MAX_LINES_PER_CALL:
        return json.dumps({
            "error": f"❌ Requested {count} lines, but max allowed is {MAX_LINES_PER_CALL}",
            "suggestion": f"Use multiple calls with count={MAX_LINES_PER_CALL} or search() first to narrow down"
        })

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        # Validate range
        if start < 0:
            start = 0
        if start >= total_lines:
            return json.dumps({
                "error": f"❌ Start line {start} exceeds file length ({total_lines} lines)",
                "suggestion": f"File has {total_lines} lines. Use start < {total_lines}"
            })

        end = min(start + count, total_lines)
        chunk = all_lines[start:end]

        # Filter very long lines
        filtered_chunk = []
        skipped = 0

        for i, line in enumerate(chunk, start=start):
            if len(line) > EXPENSIVE_LINE_THRESHOLD:
                skipped += 1
                filtered_chunk.append(f"[Line {i}: too long ({len(line)} chars) - skipped for brevity]\n")
            else:
                # Add line numbers for easier reference
                filtered_chunk.append(f"{i:4d} | {line}")

        result = {
            "filename": filename,
            "content": "".join(filtered_chunk),
            "metadata": {
                "lines_read": f"{start} to {end-1}",
                "lines_returned": len(chunk),
                "lines_skipped": skipped,
                "total_file_lines": total_lines,
                "percentage_read": f"{(end/total_lines)*100:.1f}%",
                "has_more": end < total_lines
            }
        }

        # Add helpful suggestions
        if end < total_lines:
            remaining = total_lines - end
            next_chunk_size = min(remaining, MAX_LINES_PER_CALL)
            result["metadata"]["next_call"] = f"read_lines('{filename}', start={end}, count={next_chunk_size})"

        if skipped > 0:
            result["metadata"]["note"] = f"⚠️ Skipped {skipped} very long lines (likely minified/generated code)"

        # Warning for large files
        if total_lines > 2000 and start == 0 and count > 100:
            result["metadata"]["warning"] = "⚠️ Large file detected. Consider using search() first to locate relevant sections"

        return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"❌ Failed to read file: {str(e)}"})
```

</details>

**Ejecutar test**:
<details>
<summary>💾 Ver código (bash)</summary>

```bash
python -c "from agent.tools import discover_files, search, read_lines; print('All tools imported successfully')"
```

</details>

---

### 0.6 Patrón de Uso Recomendado

**Patrón**: El agente utiliza el patrón de "search first, read second" para encontrar y leer información de forma eficiente:

1. **discover_files()** - Para ver qué archivos hay disponibles
2. **search("keyword")** - Para encontrar dónde está la información
3. **read_lines("filename", start, count)** - Para leer el contexto específico

**Ejemplo de uso**:
```python
# 1. Descubrir qué archivos están disponibles
discover_files()

# 2. Buscar información específica en todos los archivos
search("React")

# 3. Leer el contexto alrededor de los resultados encontrados
read_lines("consultores.json", start=40, count=20)
```

**Ventajas de la nueva arquitectura**:
- ⚡ Búsqueda ultra-rápida con git grep
- 🔒 Límites de seguridad integrados
- 📄 Lectura progresiva para archivos grandes
- 🔄 Búsqueda multi-archivo en todos los datos disponibles

        pattern = query if is_regex else re.escape(query)
