# 🚀 Quick Start - Inicio Rápido

## ⚡ 3 Opciones Rápidas

### Opción 1️⃣: CLI (1 minuto)

**Requisitos**: Python 3.11+, Google API Key, LangSmith API Key (opcional)

```powershell
# Clonar
git clone https://github.com/tuusuario/bi-agent-mvp.git
cd bi-agent-mvp

# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configurar
Copy-Item .env.example .env
# Editar .env: GOOGLE_API_KEY, LANGCHAIN_API_KEY

# Ejecutar
python main.py
```

**Ejemplo de query:**
```
> ¿Qué datos tienes disponibles?
> Busca Python
> Muéstrame todos los consultores
```

---

### Opción 2️⃣: Docker (1 minuto)

**Requisitos**: Docker + Docker Compose

```powershell
# Setup automático
docker-compose up -d

# Acceder a servicios:
# - API: http://localhost:8001/docs
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
# - MLflow: http://localhost:5000
```

---

### Opción 3️⃣: API REST

```powershell
# Iniciar servidor
python main.py --server

# Hacer requests
curl -X POST "http://localhost:8001/query?user_input=Qué%20datos%20tienes"

# Ver documentación interactiva
# http://localhost:8001/docs
```

---

## 🔑 Variables de Entorno (.env)

Copia `.env.example` y actualiza:

```bash
# Requerido
GOOGLE_API_KEY=tu_clave_de_google_aqui
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_PROJECT=bi-agent-mvp

# Opcional
ENABLE_MLFLOW=true
ENABLE_RAGAS_EVALUATION=true
ENABLE_GUARDRAILS=true
```

**Obtener credenciales:**
- Google API Key: https://makersuite.google.com/app/apikey
- LangSmith API Key: https://smith.langchain.com/ (sign up, Settings → API Keys)

---

## 📊 Verificar que todo funciona

```powershell
# Test 1: Herramientas
python -c "from agent.tools import discover_files; print(discover_files.invoke({}))"

# Test 2: Agente
python main.py  # Intenta una query simple

# Test 3: Monitoreo
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# LangSmith: https://smith.langchain.com/
```

---

## 🎯 Próximos Pasos

1. **Leer documentación completa**: Ver [`IMPLEMENTACION_HIBRIDA.md`](IMPLEMENTACION_HIBRIDA.md)
2. **Explorar herramientas**: Ver `.github/copilot-instructions.md`
3. **Ejecutar tests**: `pytest tests/ -v`
4. **Agregar datos**: Coloca JSON en `empresa_docs/`

---

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'langchain'"
```powershell
pip install -r requirements.txt --upgrade
```

### Error: "GOOGLE_API_KEY not set"
```powershell
# Editar .env
notepad .env
# Asegurate de agregar: GOOGLE_API_KEY=tu_clave_aqui
```

### Error: "Port 8001 already in use"
```powershell
# Cambiar puerto en docker-compose.yml
# O matar proceso: netstat -ano | findstr :8001
```

### Error: "ChromaDB not initialized" (en queries semánticas)
```powershell
# Es normal en Fases 1-4. ChromaDB es Fase 5+ (opcional)
# Las búsquedas exactas funcionan sin ChromaDB
```

---

## 📚 Documentación Completa

- **[README.md](README.md)** - Visión general del proyecto
- **[IMPLEMENTACION_HIBRIDA.md](IMPLEMENTACION_HIBRIDA.md)** - Guía de 18 días (recomendado)
- **[IMPLEMENTACION_POR_FASES.md](IMPLEMENTACION_POR_FASES.md)** - Roadmap alternativo
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Instrucciones para AI agents

---

## 💬 ¿Preguntas?

- Documentación: Ver archivos `.md` arriba
- Issues: [GitHub Issues](https://github.com/tuusuario/bi-agent-mvp/issues)
- Discusiones: [GitHub Discussions](https://github.com/tuusuario/bi-agent-mvp/discussions)

¡Hecho con ❤️!
