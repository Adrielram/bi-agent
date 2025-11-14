# Plan de Reemplazo de Herramientas para Agente BI

## Objetivo

Reemplazar las herramientas actuales del agente BI con las 3 herramientas optimizadas definidas en `docs/NEW_TOOLS.md`, manteniendo la compatibilidad con el sistema existente y mejorando el desempeño general.

## Herramientas Actuales vs. Nuevas

### Herramientas Actuales (desde `agent/tools.py`)
1. `discover_files()` - Descubre archivos disponibles en `empresa_docs/`
2. `read_collection()` - Lee colecciones completas (JSON, CSV, etc.)
3. `search_by_text()` - Búsqueda exacta de texto

### Nuevas Herramientas Optimizadas (desde `docs/NEW_TOOLS.md`)
1. `discover_files()` - Lista archivos con metadata básica (renombrada, funcionalidad mejorada)
2. `search()` - Búsqueda ultra-rápida con git grep (reemplaza `search_by_text`)
3. `read_lines()` - Lee líneas de un archivo con lectura progresiva (reemplaza `read_collection`)

## Archivos a Modificar

1. `agent/tools.py` - Reemplazar herramientas actuales con las nuevas
2. `agent/bi_agent.py` - Actualizar importaciones y enlace de herramientas
3. `tests/` - Actualizar pruebas unitarias e integración
4. `docs/` - Actualizar documentación si es necesario

## Plan Detallado

### Paso 1: Análisis del Código Actual
- [x] Analizar `agent/tools.py` - estructura actual
- [x] Analizar `agent/bi_agent.py` - cómo se usan las herramientas
- [x] Analizar `agent/tools_semantic.py` - herramientas semánticas (Fase 5+)

### Paso 2: Preparación de las Nuevas Herramientas
- [ ] Copiar código de herramientas optimizadas desde `docs/NEW_TOOLS.md` a `agent/tools.py`
- [ ] Asegurar que las nuevas herramientas mantienen la compatibilidad con LangChain
- [ ] Verificar que las constantes de seguridad se mantienen

### Paso 3: Actualización del Agente
- [ ] Actualizar importaciones en `agent/bi_agent.py` para usar las nuevas herramientas
- [ ] Actualizar enlace de herramientas en el LLM
- [ ] Asegurar que el flujo de LangGraph se mantiene intacto
- [ ] Mantener la funcionalidad de memoria por sesión

### Paso 4: Actualización de Pruebas
- [ ] Actualizar pruebas unitarias para las nuevas herramientas
- [ ] Adaptar pruebas de integración
- [ ] Verificar que el agente responde correctamente con las nuevas herramientas

### Paso 5: Documentación y Validación
- [ ] Actualizar documentación de herramientas si es necesario
- [ ] Probar manualmente las nuevas funcionalidades
- [ ] Verificar que no se rompen funcionalidades existentes

## Consideraciones Técnicas

### Seguridad
- Las nuevas herramientas incluyen límites de seguridad:
  - `MAX_LINES_PER_CALL = 200`
  - `MAX_PREVIEW_LENGTH = 150`
  - `MAX_SEARCH_RESULTS = 20`
  - `EXPENSIVE_LINE_THRESHOLD = 400`

### Compatibilidad
- El nombre de la herramienta `discover_files()` se mantiene para compatibilidad
- La firma de la herramienta `discover_files()` cambia de retorno de string a string con formato diferente
- Las herramientas `read_collection()` y `search_by_text()` serán reemplazadas por `read_lines()` y `search()` respectivamente

### Estrategia de Transición
1. Preservar la funcionalidad existente tanto como sea posible
2. Aprovechar las mejoras de rendimiento de las nuevas herramientas
3. Mantener el mismo patrón de LangGraph
4. Asegurar que la experiencia del usuario se mejora o se mantiene

## Casos de Prueba Clave

1. Consulta "¿Qué datos tienes?" → debería usar `discover_files()`
2. Búsqueda de información específica → debería usar `search()` seguido de `read_lines()`
3. Lectura de colecciones completas → debería usar `read_lines()` en chunks si el archivo es grande
4. Consultas complejas con memoria de sesión → debe continuar funcionando igual

## Posibles Riesgos

1. Cambios en el formato de salida de las herramientas pueden afectar la interpretación del LLM
2. Dependencia de `git grep` puede no funcionar en todos los entornos (fallback Python)
3. Diferentes firmas de herramientas podrían necesitar ajustes en prompts

## Verificación Post-Implementación

1. Confirmar que todas las pruebas pasan
2. Probar manualmente casos de uso comunes
3. Verificar que el agente puede:
   - Descubrir archivos disponibles
   - Realizar búsquedas efectivas
   - Leer contenido de archivos
   - Mantener la memoria de sesión
4. Validar que los tiempos de respuesta mejoran como se espera

## Rollback Plan

En caso de problemas críticos:
1. Restaurar `agent/tools.py` desde backup
2. Revertir cambios en `agent/bi_agent.py`
3. Volver a dependencias anteriores si es necesario