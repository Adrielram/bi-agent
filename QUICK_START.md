#  Quick Start - Inicio Rápido

**Configuración en menos de 5 minutos** | Tres formas de empezar

---

##  3 Opciones Rápidas

### Opción 1: CLI (Más rápido - 3 minutos)

**Requisitos**: Python 3.11+, Google API Key, LangSmith API Key (opcional)

```powershell
# 1. Clonar
git clone https://github.com/tuusuario/bi-agent-mvp.git
cd bi-agent-mvp

# 2. Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-base.txt

# 3. Configurar
Copy-Item .env.example .env
# Editar .env: GOOGLE_API_KEY, LANGCHAIN_API_KEY

# 4. Ejecutar
python main.py
```

** Ejemplo de queries:**
```
> Qué datos tienes disponibles?
> Busca Python
> Muéstrame todos los consultores
```

---

### Opción 2: Docker (Infraestructura completa)

**Requisitos**: Docker + Docker Compose

#### Para MVP (Fase 1-4):
```powershell
docker-compose up -d
```

**Servicios disponibles:**
-  API REST: http://localhost:8001/docs
-  Prometheus: http://localhost:9090
-  Grafana: http://localhost:3000 (admin/admin)

#### Para Fase 5+ (Indexación opcional):
```powershell
docker-compose -f docker-compose.hybrid.yml up -d
```

**Servicios adicionales:**
-  ChromaDB (búsqueda semántica)
-  MLflow: http://localhost:5000

---

### Opción 3: API REST (Para integración)

```powershell
# Iniciar servidor
python main.py --server

# Hacer requests
curl -X POST "http://localhost:8001/query?user_input=Qué%20datos%20tienes"

# Ver documentación interactiva
# http://localhost:8001/docs
```

---

##  Variables de Entorno (.env)

Copia `.env.example` y actualiza con tus credenciales:

```bash
#  REQUERIDO
GOOGLE_API_KEY=tu_clave_de_google_aqui
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_PROJECT=bi-agent-mvp

#  OPCIONAL (Fase 5+)
ENABLE_HYBRID=false  # Cambiar a true para indexación
ENABLE_MLFLOW=false
ENABLE_RAGAS_EVALUATION=false
ENABLE_GUARDRAILS=false
```

** Obtener credenciales:**
- **Google API Key**: https://makersuite.google.com/app/apikey
- **LangSmith API Key**: https://smith.langchain.com/  Settings  API Keys

---

##  Dependencias

### Para MVP Copilot-Like ( Recomendado - Fase 1-4)

```powershell
pip install -r requirements-base.txt
```

**Características:**
-  Instalación 3x más rápida (2-3 min)
-  Latencia: 2-5 segundos
-  Perfecto para demo/portfolio
-  Zero setup time

### Para Fase 5+ con Indexación ( Opcional)

```powershell
pip install -r requirements-hybrid.txt
```

**Características:**
-  Latencia: 50-200ms (20x más rápido)
-  Incluye ChromaDB + semantic search
-  Startup time: 15-20s para indexar
-  Para producción con alto tráfico

**Cuál debo usar?**  
 Empieza con `requirements-base.txt`. Solo cambia a hybrid si necesitas:
- Queries < 500ms
- Dataset > 1MB
- Búsqueda semántica

---

##  Verificar que todo funciona

```powershell
# Test 1: Herramientas básicas
python -c "from agent.tools import discover_files; print(discover_files.invoke({}))"

# Test 2: Agente funcionando
python main.py
# Intenta: "Qué datos tienes disponibles?"

# Test 3: Servicios de monitoreo (si usas Docker)
# - Prometheus: http://localhost:9090/targets
# - Grafana: http://localhost:3000
# - LangSmith: https://smith.langchain.com/
```

** Salida esperada en Test 1:**
```
Encontré 5 archivos disponibles:
- proyectos.json
- consultores.json
- clientes.json
...
```

---

##  Próximos Pasos

1. ** Leer documentación completa**: Ver [`IMPLEMENTACION_HIBRIDA.md`](IMPLEMENTACION_HIBRIDA.md)
2. ** Explorar herramientas**: Ver [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
3. ** Ejecutar tests**: `pytest tests/ -v --cov=agent`
4. ** Agregar tus datos**: Coloca archivos JSON/CSV en `empresa_docs/`

---

##  Troubleshooting

###  Error: "ModuleNotFoundError: No module named 'langchain'"

```powershell
# Solución: Reinstalar dependencias
pip install -r requirements-base.txt --upgrade
```

###  Error: "GOOGLE_API_KEY not set"

```powershell
# Solución: Editar archivo .env
notepad .env
# Asegurate de agregar: GOOGLE_API_KEY=tu_clave_aqui
```

###  Error: "Port 8001 already in use"

```powershell
# Solución 1: Cambiar puerto en docker-compose.yml
# Buscar: "8001:8000" y cambiar a "8002:8000"

# Solución 2: Matar proceso existente
netstat -ano | findstr :8001
# Luego: taskkill /PID <numero_pid> /F
```

###  Advertencia: "ChromaDB not initialized"

```powershell
# Esto es NORMAL en Fases 1-4
# ChromaDB es Fase 5+ (opcional)
# Las búsquedas por texto funcionan sin ChromaDB
```

** Tip**: Si usas Fase 1-4 (MVP), ignora advertencias de ChromaDB.

---

##  Documentación Completa

| Archivo | Descripción |
|---------|-------------|
| **[README.md](README.md)** | Visión general del proyecto |
| **[IMPLEMENTACION_HIBRIDA.md](IMPLEMENTACION_HIBRIDA.md)** | Guía completa de 18 días ( recomendado) |
| **[IMPLEMENTACION_POR_FASES.md](IMPLEMENTACION_POR_FASES.md)** | Roadmap alternativo |
| **[.github/copilot-instructions.md](.github/copilot-instructions.md)** | Instrucciones para AI agents |

---

##  Soporte y Comunidad

-  **Documentación**: Ver archivos `.md` en el repositorio
-  **Reportar bugs**: [GitHub Issues](https://github.com/tuusuario/bi-agent-mvp/issues)
-  **Discusiones**: [GitHub Discussions](https://github.com/tuusuario/bi-agent-mvp/discussions)
-  **Dale una estrella** si te fue útil

---

<div align="center">

** Hecho con  y LangChain! **

[ Volver arriba](#-quick-start---inicio-rápido)

</div>
