# 🔄 Guía de Migración: LangChain ReAct → LangGraph

**Objetivo**: Actualizar IMPLEMENTACION_HIBRIDA.md para usar LangGraph en lugar de LangChain

**Cambios Principales**:

1. **Framework**: LangChain ReAct → LangGraph StateGraph
2. **Arquitectura**: Cadena implícita → Grafo explícito
3. **Memoria**: Manual → Tipada (TypedDict)
4. **Reintentos**: Manuales → Automáticos
5. **Routing**: Genérico → Condicional basado en estado
6. **Performance**: 2-5s → 2-5s (igual) + paralelización posible

---

## 🔑 Cambios Clave

### Antes (LangChain ReAct)

```python
from langchain.agents import create_react_agent, AgentExecutor

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": query})
```

**Problemas**:
- ❌ Cadena implícita (invisible en el código)
- ❌ Memoria manual o global
- ❌ Reintentos manuales
- ❌ Routing limitado

### Después (LangGraph StateGraph)

```python
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    """Estado explícito con memoria"""
    input: str
    messages: List[BaseMessage]
    filtered_data: Optional[List]
    current_analysis: Optional[Dict]
    phase: str
    status: str

workflow = StateGraph(AgentState)
workflow.add_node("reasoning", reasoning_func)
workflow.add_node("tool_execution", tool_func)
workflow.add_conditional_edges("reasoning", route_function)
graph = workflow.compile()
result = graph.invoke(initial_state)
```

**Beneficios**:
- ✅ Grafo **explícito** en el código
- ✅ Memoria **tipada** (TypedDict)
- ✅ Reintentos **automáticos**
- ✅ Routing **condicional** arbitrario

---

## 📊 Traducción de Conceptos

| LangChain | LangGraph | Descripción |
|-----------|-----------|-------------|
| `create_react_agent()` | `StateGraph()` | Define el flujo |
| `AgentExecutor` | `workflow.compile()` | Compila el grafo |
| `tools` | `workflow.add_node()` | Agrega nodos (thinking, action, etc) |
| Memory manual | `AgentState (TypedDict)` | Estado compartido tipado |
| Retry manual | Conditional edge | Routing automático a retry node |
| `prompt.format()` | `state["messages"]` | Contexto acumulativo |

---

## 🏗️ Arquitectura LangGraph

```
Estado (TypedDict)
    ↓
Nodo: reasoning
    ↓ (conditional)
    ├→ Nodo: tool_execution
    │   ↓ (conditional)
    │   ├→ retry (si falla)
    │   └→ reasoning (con nuevos datos)
    │
    └→ Nodo: result_handling
        ↓
        END
```

---

## 🔧 Implementación Paso a Paso

### 1. Definir AgentState

```python
from typing import TypedDict, List, Optional, Dict, Any
from langchain.schema import BaseMessage

class AgentState(TypedDict):
    """Estado compartido (MEMORIA CONVERSACIONAL)"""
    
    # Entrada actual
    input: str
    
    # Histórico de conversación
    messages: List[BaseMessage]
    
    # MEMORIA ACUMULADA
    filtered_data: Optional[List[Dict[str, Any]]]
    current_analysis: Optional[Dict[str, Any]]
    selected_items: Optional[List[str]]
    
    # Metadata del flujo
    phase: str  # "search" | "analyze" | "filtering"
    tool_used: Optional[str]
    retry_count: int
    status: str  # "thinking" | "executing" | "error" | "success"
```

### 2. Definir Nodos

```python
def reasoning_node(state: AgentState) -> dict:
    """LLM razona qué hacer (usa memoria del estado)"""
    
    # Construir prompt con memoria
    context = ""
    if state["filtered_data"]:
        context += f"Datos previos: {len(state['filtered_data'])} items\n"
    if state["current_analysis"]:
        context += f"Análisis anterior: {state['current_analysis']}\n"
    
    prompt = f"{context}\nUsuario pregunta: {state['input']}"
    
    response = llm.invoke(prompt)
    
    # Retornar update del estado
    return {
        "messages": state["messages"] + [response],
        "status": "thinking"
    }

def tool_execution_node(state: AgentState) -> dict:
    """Ejecutar herramienta con reintentos automáticos"""
    
    last_message = state["messages"][-1].content
    tool_name = extract_tool_name(last_message)
    
    try:
        tool = tools[tool_name]
        result = tool.invoke({})
        
        return {
            "filtered_data": result,
            "current_analysis": result,
            "tool_used": tool_name,
            "retry_count": 0,
            "status": "success"
        }
    except Exception as e:
        # Si falla, conditional edge enviará a retry
        return {
            "retry_count": state["retry_count"] + 1,
            "status": "error",
            "tool_used": tool_name
        }

def result_handling_node(state: AgentState) -> dict:
    """Formatear respuesta final"""
    
    response = build_response(state["current_analysis"])
    
    return {
        "messages": state["messages"] + [AIMessage(content=response)],
        "status": "complete",
        "phase": "completion"
    }
```

### 3. Definir Routing Condicional

```python
def route_after_reasoning(state: AgentState) -> str:
    """Después de razonar: ¿ejecutar tool o responder?"""
    
    last_message = state["messages"][-1].content.lower()
    
    if any(tool in last_message for tool in ["search(", "read(", "analyze("]):
        return "tool_execution"
    else:
        return "result_handling"

def route_after_tool_execution(state: AgentState) -> str:
    """Después de tool: ¿reintentar, razonar de nuevo, o completar?"""
    
    if state["status"] == "error" and state["retry_count"] < 3:
        return "retry"  # Reintentar automático
    elif state["status"] == "success":
        return "reasoning"  # Razonar de nuevo con nuevos datos
    else:
        return "result_handling"  # Completar
```

### 4. Construir Grafo

```python
from langgraph.graph import StateGraph, END

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Agregar nodos
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("tool_execution", tool_execution_node)
    workflow.add_node("result_handling", result_handling_node)
    
    # Conditional edges (routing)
    workflow.add_conditional_edges(
        "reasoning",
        route_after_reasoning,
        {
            "tool_execution": "tool_execution",
            "result_handling": "result_handling"
        }
    )
    
    workflow.add_conditional_edges(
        "tool_execution",
        route_after_tool_execution,
        {
            "retry": "tool_execution",        # Loop: reintentar
            "reasoning": "reasoning",         # Loop: razonar con nuevos datos
            "result_handling": "result_handling"  # Salir
        }
    )
    
    workflow.add_edge("result_handling", END)
    
    # Entry point
    workflow.set_entry_point("reasoning")
    
    return workflow.compile()

graph = build_graph()
```

### 5. Ejecutar

```python
class BiAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.graph = build_graph()
    
    def query(self, user_input: str) -> str:
        """IMPORTANTE: Memoria persiste en el estado"""
        
        initial_state = {
            "input": user_input,
            "messages": [],
            "filtered_data": None,
            "current_analysis": None,
            "selected_items": None,
            "phase": "search",
            "tool_used": None,
            "retry_count": 0,
            "status": "thinking"
        }
        
        result = self.graph.invoke(initial_state)
        
        # Extraer respuesta final
        return result["messages"][-1].content

# Uso
agent = BiAgent()
response1 = agent.query("Muéstrame consultores con Python")
response2 = agent.query("¿Cuál tiene más experiencia?")  # ✅ Contexto acumulado si mantenemos el estado
```

---

## 🎯 Cambios en IMPLEMENTACION_HIBRIDA.md

### Título
```markdown
ANTES: # Implementación Híbrida - Agente de BI con Observability desde Día 1
DESPUÉS: # Implementación LangGraph - Agente de BI con Memoria y Observability desde Día 1
```

### Stack
```markdown
ANTES: | **Framework** | LangChain | Día 1 |
DESPUÉS: | **Framework** | **LangGraph** (ReAct + Grafo) | Día 1 |
```

### Timeline
```markdown
ANTES: **Timeline**: 18 días
DESPUÉS: **Timeline**: 20 días (18 + 2 días aprendizaje LangGraph)
```

### Fases
```markdown
ANTES: FASE 1-2: MVP Copilot-Like
DESPUÉS: FASE 1-2: MVP LangGraph con Memoria + Reintentos
```

### Ventajas
```markdown
Agregar a "Aprendizajes Clave":
1. LangGraph > LangChain: Arquitectura + Memoria + Reintentos
2. Grafo explícito = Debugging 10x mejor
3. Estado tipado = Confiabilidad
4. Reintentos automáticos = Robustez
5. Paralelización = Performance
```

### Sección 0.7 (CRÍTICA)
Reemplazar toda la sección con:
- StateGraph en lugar de AgentExecutor
- AgentState TypedDict en lugar de manejo manual de memoria
- Nodos explícitos
- Conditional edges para routing y reintentos
- Ejemplo de grafo visual

---

## ⚡ Cambios Rápidos (Si ya tienes LangChain)

Si ya implementaste con LangChain y quieres migrar:

```python
# ANTES (LangChain)
from langchain.agents import create_react_agent, AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": query})

# DESPUÉS (LangGraph)
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState).compile()
result = graph.invoke(initial_state)
```

**Esfuerzo**: ~4-5 horas de refactoring (si tienes código funcionando)

---

## 📚 Recursos

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [ReAct with LangGraph](https://langchain-ai.github.io/langgraph/how-tos/react-agent/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level_conceptual_index/)

---

## ✅ Checklist de Migración

- [ ] Crear `AgentState (TypedDict)` con memoria
- [ ] Definir nodos (reasoning, tool_execution, result_handling)
- [ ] Definir routing condicional
- [ ] Construir `StateGraph` con nodos y edges
- [ ] Compilar grafo
- [ ] Test: queries complejas con memoria
- [ ] Test: reintentos automáticos
- [ ] Verificar LangSmith traces (deben mostrar grafo)
- [ ] Actualizar documentación
- [ ] Update IMPLEMENTACION_HIBRIDA.md con ejemplos

---

**Status**: Cambios listos para implementar en Fase 1.5

Recomendación: Usar esta guía para reescribir `agent/bi_agent.py` y actualizar `IMPLEMENTACION_HIBRIDA.md`
