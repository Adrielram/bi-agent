#!/usr/bin/env python
"""
BI Agent - Main Orchestrator with LangGraph
Integrates LangGraph + Google Gemini + LangSmith observability

Architecture:
- StateGraph with explicit nodes (reasoning, tool_execution, result_handling)
- Conversational memory (AgentState persists between turns)
- Automatic retries and conditional routing
- Visual debugging in LangSmith

Usage:
    python agent/bi_agent.py "Your query here"
    python agent/bi_agent.py --interactive
"""

import os
import sys
import time
import json
from typing import TypedDict, List, Optional, Dict, Any, Annotated
from operator import add
from dotenv import load_dotenv

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# LangChain imports (for tools and LLM)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import discover_files, read_collection, search_by_text
from utils.logging_config import logger, log_query, log_tool_call


# Load environment
load_dotenv()


# ============================================
# ESTADO: AgentState con Memoria Conversacional
# ============================================

class AgentState(TypedDict):
    """
    Estado que persiste entre turnos (MEMORIA CONVERSACIONAL).
    LangGraph mantiene este estado automáticamente.
    """
    # Input/Output
    input: str
    output: str
    
    # Histórico conversacional
    messages: Annotated[List[BaseMessage], add]
    
    # MEMORIA ACUMULADA (contexto entre queries)
    filtered_data: Optional[List[Dict[str, Any]]]
    current_analysis: Optional[Dict[str, Any]]
    
    # Metadata del flujo
    intermediate_steps: List[tuple]
    retry_count: int
    tool_call_id: Optional[str]


# ============================================
# BI AGENT CON LANGGRAPH
# ============================================

class BIAgent:
    """
    Business Intelligence Agent powered by LangGraph + Google Gemini
    
    Ventajas vs LangChain:
    ✅ Grafo explícito (ves el flujo de decisiones)
    ✅ Memoria conversacional tipada (AgentState)
    ✅ Reintentos automáticos (si tool falla)
    ✅ Conditional routing basado en estado
    ✅ Debugging visual en LangSmith
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
        self.tools = [discover_files, read_collection, search_by_text]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build LangGraph
        self.graph = self._build_graph()
        
        logger.info("BI Agent (LangGraph) initialized successfully")
    
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
        system_prompt = """Eres un asistente de Business Intelligence para una consultora.

Tu objetivo es ayudar con información sobre:
- Proyectos ejecutados (tecnologías, costos, duraciones)
- Consultores (expertise, experiencia, disponibilidad)
- Clientes y casos de éxito
- Propuestas comerciales

INSTRUCCIONES:
1. SIEMPRE cita fuentes específicas (IDs, nombres)
2. Si no tienes información, dilo claramente - NO inventes
3. Usa las herramientas disponibles para buscar datos
4. Formatea respuestas de manera clara

Herramientas disponibles:
- discover_files: Descubre qué archivos/datos hay disponibles
- read_collection: Lee una colección completa (ej: "consultores", "proyectos")
- search_by_text: Busca texto específico en las colecciones
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
    
    def query(self, user_input: str, thread_id: Optional[str] = None) -> str:
        """
        Execute a query with LangGraph (supports conversational memory).
        
        Args:
            user_input: User's natural language query
            thread_id: Optional thread ID for multi-turn conversations
        
        Returns:
            Agent's response
        """
        
        start_time = time.time()
        
        try:
            # Log query start
            log_query(logger, user_input, status="started")
            
            # Prepare initial state
            initial_state = {
                "input": user_input,
                "output": "",
                "messages": [HumanMessage(content=user_input)],
                "filtered_data": None,
                "current_analysis": None,
                "intermediate_steps": [],
                "retry_count": 0,
                "tool_call_id": None
            }
            
            # Execute graph (LangSmith tracing automático)
            config = {"recursion_limit": 10}
            if thread_id:
                config["configurable"] = {"thread_id": thread_id}
            
            result = self.graph.invoke(initial_state, config=config)
            
            # Calculate latency
            latency = time.time() - start_time
            
            # Extract response from messages
            messages = result.get("messages", [])
            
            # Get last AI message
            response = ""
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and msg.content:
                    response = msg.content
                    break
            
            if not response:
                response = "No response generated"
            
            # Log query completion
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
        """Start an interactive query session"""
        print("\n" + "="*70)
        print("  BI Agent - Interactive Session")
        print("  Type 'exit' to quit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("Query> ").strip()
                
                if user_input.lower() == "exit":
                    print("[*] Exiting...")
                    break
                
                if not user_input:
                    continue
                
                print("\n[*] Processing...\n")
                response = self.query(user_input)
                print(f"Response:\n{response}\n")
                
            except KeyboardInterrupt:
                print("\n[*] Session interrupted")
                break
            except Exception as e:
                print(f"[ERROR] {str(e)}\n")


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
            agent.interactive_session()
        else:
            # Single query from command line
            query = " ".join(sys.argv[1:])
            try:
                response = agent.query(query)
                print(f"\nResponse:\n{response}\n")
            except Exception as e:
                print(f"[ERROR] {e}")
                return 1
    else:
        # Show help
        print("""
BI Agent - Business Intelligence Assistant

Usage:
  python agent/bi_agent.py "Your query here"     # Single query
  python agent/bi_agent.py --interactive         # Interactive mode
  python agent/bi_agent.py --help               # Show this message

Examples:
  python agent/bi_agent.py "What data do you have?"
  python agent/bi_agent.py "List all consultants"
  python agent/bi_agent.py "Search for Python projects"
        """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
