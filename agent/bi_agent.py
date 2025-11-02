#!/usr/bin/env python
"""
BI Agent - Main Orchestrator
Integrates LangChain + Google Gemini + LangSmith observability

Usage:
    python agent/bi_agent.py "Your query here"
    python agent/bi_agent.py --interactive
"""

import os
import sys
import time
from typing import Optional
from dotenv import load_dotenv

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tools import Tool

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import discover_files, read_collection, search_by_text
from utils.logging_config import logger, log_query, log_tool_call


# Load environment
load_dotenv()


class BIAgent:
    """Business Intelligence Agent powered by LangChain + Google Gemini"""
    
    def __init__(self):
        """Initialize the BI Agent"""
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
        self.tools = self._setup_tools()
        
        # Setup agent
        self.agent = self._setup_agent()
        
        logger.info("BI Agent initialized successfully")
    
    def _setup_tools(self) -> list[Tool]:
        """Setup LangChain tools"""
        tools = [
            Tool(
                name="discover_files",
                func=discover_files.invoke,
                description=discover_files.description
            ),
            Tool(
                name="read_collection",
                func=lambda x: read_collection.invoke({"collection_name": x}),
                description=read_collection.description
            ),
            Tool(
                name="search_by_text",
                func=lambda x: search_by_text.invoke({"query": x}),
                description=search_by_text.description
            ),
        ]
        logger.info(f"Configured {len(tools)} tools")
        return tools
    
    def _setup_agent(self) -> AgentExecutor:
        """Setup ReAct agent with LangSmith tracing"""
        from langchain import hub
        
        # Get the standard ReAct prompt from hub
        try:
            prompt = hub.pull("hwchase17/react")
        except Exception:
            # Fallback if hub is not available
            logger.warning("Using fallback prompt (hub not available)")
            from langchain_core.prompts import ChatPromptTemplate
            prompt = ChatPromptTemplate.from_template(
                """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
            )
        
        # Create agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create executor with error handling
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        return executor
    
    def query(self, user_input: str) -> str:
        """
        Execute a query and return the response
        
        Args:
            user_input: User's natural language query
        
        Returns:
            Agent's response
        """
        
        start_time = time.time()
        
        try:
            # Log query start
            log_query(logger, user_input, status="started")
            
            # Execute query
            result = self.agent.invoke({"input": user_input})
            
            # Calculate latency
            latency = time.time() - start_time
            
            # Log query completion
            log_query(
                logger,
                user_input,
                status="completed",
                latency=latency
            )
            
            return result.get("output", "No response generated")
        
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
