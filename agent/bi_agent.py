#!/usr/bin/env python
"""
BI Agent - Main Orchestrator with LangGraph
Integrates LangGraph + Google Gemini + LangSmith observability

Architecture:
- StateGraph with explicit nodes (reasoning, tool_execution)
- Conversational memory PER SESSION ONLY (in-memory, not persistent)
- Automatic retries and conditional routing
- Visual debugging in LangSmith

Usage:
    python main.py "Your query here"                # Single query (no memory)
    python main.py --interactive                    # Interactive mode (WITH memory)
"""

import os
import sys
import time
from typing import TypedDict, List, Optional, Dict, Any, Annotated
from operator import add
from dotenv import load_dotenv

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# LangChain imports (for tools and LLM)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import discover_files, search, read_lines
from utils.logging_config import logger, log_query, log_tool_call
try:
    from agent.guardrails_config import validate_input, validate_output
    from monitoring.guardrails_metrics import guard_input_blocked_total, guard_output_redacted_total
except Exception:
    # Fall back to local validators if guardrails not available
    from security.input_validator import validate_user_input as validate_input
    from security.output_validator import validate_and_sanitize_output as validate_output


# Load environment
load_dotenv()


# ============================================
# ESTADO: AgentState con Memoria por Sesión
# ============================================

class AgentState(TypedDict):
    """
    Estado conversacional que persiste SOLO durante una sesión interactiva.
    Se descarta cuando termina --interactive.

    Memoria: Acumula mensajes y contexto entre queries de la MISMA sesión.
    """
    input: str  # Current user query
    messages: Annotated[List[BaseMessage], add]  # Accumulated conversation history (memoria)
    filtered_data: Optional[List[Dict[str, Any]]]  # Results from previous filtering operations
    current_analysis: Optional[Dict[str, Any]]  # Results from previous analysis step
    intermediate_steps: List[tuple]  # Tool execution steps (ReAct trace)
    retry_count: int  # Number of retry attempts for current operation
    tool_call_id: Optional[str]  # ID of current tool call (for tracing)


# ============================================
# BI AGENT CON LANGGRAPH + MEMORIA POR SESIÓN
# ============================================

class BIAgent:
    """
    Business Intelligence Agent powered by LangGraph + Google Gemini

    MEMORIA:
    - Single queries: NO hay memoria (cada query es independiente)
    - Interactive mode: SÍ hay memoria (acumula contexto en la sesión)
    - Al terminar --interactive: memoria se descarta (nueva sesión = nuevo contexto)
    """

    def __init__(self):
        """Initialize the BI Agent with LangGraph"""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not set. "
                "Please add it to .env file or set it as environment variable."
            )

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.api_key,
            temperature=0.0,  # Factual queries
            convert_system_message_to_human=True
        )

        # Setup tools
        self.tools = [discover_files, search, read_lines]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Build LangGraph
        self.graph = self._build_graph()

        # Session state (in-memory, discarded when session ends)
        self.session_messages: List[BaseMessage] = []

        logger.info("BI Agent (LangGraph + Session Memory) initialized successfully")

    @staticmethod
    def get_graph():
        """
        Static method to return the graph definition for LangGraph CLI.
        This is needed by the langgraph.json configuration.
        """
        # Create a minimal instance just for building the graph
        # (the session state won't matter for graph definition)
        instance = BIAgent.__new__(BIAgent)  # Create instance without calling __init__

        # Set minimal required attributes for graph building
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not set. "
                "Please add it to .env file or set it as environment variable."
            )

        instance.api_key = api_key
        instance.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=instance.api_key,
            temperature=0.0,  # Factual queries
            convert_system_message_to_human=True
        )

        instance.tools = [discover_files, search, read_lines]
        instance.llm_with_tools = instance.llm.bind_tools(instance.tools)

        # Build and return the graph
        graph = instance._build_graph()
        return graph

    def _build_graph(self) -> StateGraph:
        """
        Construir StateGraph con nodos y conditional edges.

        Flujo:
        1. reasoning (LLM piensa qué hacer)
        2. conditional edge → tools o END
        3. tools (ejecuta herramientas)
        4. conditional edge → reasoning (loop) o END
        """
        workflow = StateGraph(AgentState)

        # Nodo 1: Reasoning (LLM decide qué hacer)
        workflow.add_node("reasoning", self._reasoning_node)

        # Nodo 2: Tools (ejecuta herramientas con ToolNode)
        tool_node = ToolNode(self.tools)
        workflow.add_node("tools", tool_node)

        # Entry point
        workflow.set_entry_point("reasoning")

        # Conditional edges
        workflow.add_conditional_edges(
            "reasoning",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )

        # Edge: tools → reasoning (loop back for multi-step reasoning)
        workflow.add_edge("tools", "reasoning")

        # Compile graph
        return workflow.compile()

    def _reasoning_node(self, state: AgentState) -> Dict:
        """
        Nodo de razonamiento: LLM decide qué hacer.

        Lee memoria del estado y genera respuesta/tool calls.
        """
        messages = state["messages"]

        # System prompt with context
        system_prompt = """

        Prompt Completo

        Eres un asistente de Business Intelligence especializado en ayudar con propuestas comerciales y búsqueda de socios
        tecnológicos para una consultora de IA y tecnología.

        TU OBJETIVO PRINCIPAL:
        - Analizar solicitudes de socios tecnológicos y proyectos
        - Buscar en nuestra base de datos si tenemos experiencia, proyectos similares y personal capacitado
        - Proporcionar respuestas completas y fundamentadas para respaldar propuestas comerciales

        PASOS DE RAZONAMIENTO:
        1. ANALIZA la solicitud (qué tipo de proyecto, qué tecnologías, qué perfil de personal)
        2. PLANEA tu búsqueda considerando posibles términos relacionados y sinónimos
        3. USA las herramientas en esta secuencia lógica:
            - discover_files: Para explorar qué tipos de datos tenemos disponibles
            - search: Para encontrar términos clave (tecnologías, industrias, roles) en los archivos disponibles
            - read_lines: Para leer detalles completos después de localizar con search
        4. SINTETIZA la información encontrada en todos los archivos relevantes
        5. FORMATEA una respuesta completa que ayude a responder la propuesta comercial

        ESTRATEGIA DE EXPLORACIÓN:
        - Usa discover_files para ver qué archivos están disponibles
        - No asumas estructuras de datos específicas
        - Busca en todos los archivos disponibles sin prejuicios sobre su contenido
        - Usa search para localizar términos relevantes (tecnologías, industrias, roles, herramientas)
        - Usa read_lines para leer datos específicos una vez localizados

        PATRONES DE BÚSQUEDA:
        1. Busca términos clave de la solicitud (ej: "IA", "LinkedIn", "agente", "automatización")
        2. Busca sinónimos y conceptos relacionados (ej: "inteligencia artificial" por "IA")
        3. Busca por industria (ej: si es "FinTech", busca también "banca", "finanzas")
        4. Busca por roles o tecnologías relevantes (ej: "React" → también busca "frontend", "web")
        5. Busca consultores con experiencia en la industria mencionada

        RESPUESTA COMPLETA DEBE INCLUIR:
        - Recursos específicos con experiencia relevante (con nombres, roles o identificadores)
        - Proyectos, casos de estudio o trabajos anteriores similares (con IDs o descripciones)
        - Tecnologías y herramientas que hemos utilizado en proyectos similares
        - Indicar disponibilidad de recursos si es relevante
        - Breve descripción de los resultados o logros de trabajos similares
        - Si no tenemos experiencia directa: menciona experiencia similar o transferible

        MANEJO DE DATOS DESCONOCIDOS:
        - No asumas estructuras de datos específicas
        - Explora los archivos disponibles antes de formar hipótesis
        - Extrae información estructurada de los datos sin importar el formato
        - Combina información de diferentes archivos para crear una respuesta integral
        - Ajusta tu interpretación según el formato que encuentres

        INSTRUCCIONES CRÍTICAS:
        1. NO inventes información - solo lo que las herramientas retornen
        2. Si no hay experiencia directa: menciona experiencia similar o transferible
        3. Cita fuentes específicas (archivo, nombre, ID, o descripción del dato encontrado)
        4. Usa formato claro y profesional en tus respuestas
        5. Prioriza información que respalde la capacidad de ser socio tecnológico

        MANEJO DE CASOS LÍMITE:
        - Si la solicitud es muy general → busca conceptos relacionados en todos los archivos
        - Si no hay coincidencias exactas → busca experiencias transferibles o tecnologías similares
        - Si hay mucha información → resume lo más relevante y menciona qué más podría buscarse
        - Si hay poca información → explica claramente qué se encontró y qué no
        - Si los datos están en diferentes formatos → adapta tu extracción según el formato encontrado
        """

        # Add system message if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages

        # Invoke LLM with tools
        response = self.llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def _should_continue(self, state: AgentState) -> str:
        """
        Routing condicional: decidir si continuar con tools o terminar.
        """
        messages = state["messages"]
        last_message = messages[-1]

        # Si el LLM llamó a tools, continuar
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"

        # Si no hay tool calls, terminar
        return "end"

    def _create_initial_state(self, user_input: str, use_session_memory: bool = False) -> AgentState:
        """
        Create initial state for a query.

        Args:
            user_input: User's query
            use_session_memory: If True, include accumulated session messages
        """
        if use_session_memory:
            # Modo interactivo: agregar nuevo mensaje a historial existente
            messages = self.session_messages + [HumanMessage(content=user_input)]
        else:
            # Modo single query: nuevo estado limpio (sin memoria)
            messages = [HumanMessage(content=user_input)]

        return {
            "input": user_input,
            "messages": messages,
            "filtered_data": None,
            "current_analysis": None,
            "intermediate_steps": [],
            "retry_count": 0,
            "tool_call_id": None
        }

    def _extract_response(self, messages: List[BaseMessage]) -> str:
        """Extract the last AI message as response"""
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        return "No response generated"

    def query(self, user_input: str, use_session_memory: bool = False) -> str:
        """
        Execute a query.

        Args:
            user_input: User's natural language query
            use_session_memory: If True, uses accumulated session messages (interactive mode)
                               If False, starts fresh (single query mode)

        Returns:
            Agent's response
        """

        start_time = time.time()

        try:
            # Validate input with guardrails (Fase 1.5)
            try:
                validated_input = validate_input(user_input)
            except Exception as e:
                logger.warning(f"Input validation failed: {str(e)}")
                log_query(logger, user_input, status="blocked")
                guard_input_blocked_total.inc()
                return f"No puedo procesar esa consulta: {str(e)}"

            log_query(logger, user_input, status="started")

            # Create state (with or without session memory)
            initial_state = self._create_initial_state(user_input, use_session_memory)

            # Execute graph
            config = {"recursion_limit": 20}
            result = self.graph.invoke(initial_state, config=config)

            # Extract response
            latency = time.time() - start_time
            messages = result.get("messages", [])
            response = self._extract_response(messages)

            # Validate & sanitize output before returning
            # Validate and sanitize output with Guardrails (or fallback)
            try:
                validated_response = validate_output(response)
            except Exception:
                validated_response = response
            # If Guardrails flagged modifications, log it
            # (Guardrails raises or returns sanitized output depending on rules)
            # If guardrails sanitized or changed content, increment metric
            if validated_response != response:
                guard_output_redacted_total.inc()
            response = validated_response

            # If using session memory, save all messages for next query
            if use_session_memory:
                self.session_messages = messages

            # Log completion
            log_query(
                logger,
                user_input,
                status="completed",
                latency=latency
            )
            logger.info(f"Response length: {len(response)} characters")

            return response

        except Exception as e:
            latency = time.time() - start_time
            logger.error(f"Query failed: {str(e)}")
            log_query(
                logger,
                user_input,
                status="error",
                latency=latency
            )
            raise

    def interactive_session(self):
        """
        Start an interactive query session WITH MEMORY.

        MEMORIA:
        - Cada query se agrega al historial
        - LLM ve el contexto acumulado
        - Cuando terminas (exit), la sesión se borra

        EJEMPLO:
        Query 1: "¿Cuántos consultores?"
                 → Response: "30 consultores"

        Query 2: "¿Cuántos tienen Python?"
                 → LLM ve Query 1 + Response → Entiende "los 30"
                 → Response: "De los 30, estos 12 tienen Python"

        Query 3: "¿Están disponibles ahora?"
                 → LLM ve Query 1 + 2 + responses → Entiende "los 12 con Python"
                 → Response: "De esos 12, estos 7 están disponibles"
        """
        print("\n" + "="*70)
        print("  BI Agent - Interactive Session WITH MEMORY")
        print("  Type 'exit' to quit (memory discarded after exit)")
        print("="*70 + "\n")

        # Reset session memory for this new interactive session
        self.session_messages = []

        query_count = 0

        while True:
            try:
                user_input = input("Query> ").strip()

                if user_input.lower() == "exit":
                    print(f"[*] Session ended. Total queries: {query_count}")
                    print("[*] Memory discarded (new session will start fresh)\n")
                    self.session_messages = []  # Explicitly clear
                    break

                if not user_input:
                    continue

                query_count += 1
                print("\n[*] Processing...\n")

                # Execute with session memory enabled
                response = self.query(user_input, use_session_memory=True)
                print(f"Response:\n{response}\n")

            except KeyboardInterrupt:
                print("\n[*] Session interrupted")
                self.session_messages = []
                break
            except Exception as e:
                print(f"[ERROR] {str(e)}\n")


def create_graph():
    """
    Function to create the graph, specifically for LangGraph CLI.
    This creates the graph only when explicitly called.
    """
    return BIAgent.get_graph()


def get_graph_from_file():
    """
    Standalone function to return the graph, specifically for LangGraph CLI.
    This provides an alternative way for the CLI to access the graph.
    """
    return create_graph()


def main():
    """Main entry point"""

    # Initialize agent
    try:
        agent = BIAgent()
    except ValueError as e:
        logger.error(f"Failed to initialize agent: {e}")
        print(f"[ERROR] {e}")
        return 1

    # Process arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            # Interactive mode WITH memory
            agent.interactive_session()
        else:
            # Single query WITHOUT memory
            query = " ".join(sys.argv[1:])
            try:
                response = agent.query(query, use_session_memory=False)
                print(f"\nResponse:\n{response}\n")
            except Exception as e:
                print(f"[ERROR] {e}")
                return 1
    else:
        # Show help
        print("""
BI Agent - Business Intelligence Assistant with Session Memory

MEMORIA:
- Single query:     python main.py "question"          (NO memory)
- Interactive:      python main.py --interactive       (WITH memory, per-session)

Usage:
  python main.py "Your query here"                     # Single query (no memory)
  python main.py --interactive                         # Interactive mode (WITH memory)
  python main.py --help                               # Show this message

Examples:
  python main.py "What data do you have?"
  python main.py "List all consultants"
  python main.py "Search for Python projects"

Interactive Mode (--interactive) - MEMORY EXAMPLE:
  Query 1: "How many consultants?"
  Response: "30 consultants"

  Query 2: "How many have Python?"
  Response: "Of those 30, 12 have Python"     ← Remembers Query 1

  Query 3: "Show me their availability"
  Response: "Of those 12 with Python, 7 are available"  ← Remembers Query 1-2

  Type 'exit' to end session (memory discarded)
        """)

    return 0


if __name__ == "__main__":
    sys.exit(main())
