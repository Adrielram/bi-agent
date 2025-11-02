#!/usr/bin/env python
"""
AI Sales Assistant - BI Agent MVP
Main entry point for the application

Usage:
    python main.py "Your query"              # Single query
    python main.py --interactive              # Interactive mode
    python main.py --server                   # Start API server (Phase 3)
"""

import sys
import os

# Add agent module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agent"))

from agent.bi_agent import BIAgent, main as agent_main


if __name__ == "__main__":
    sys.exit(agent_main())
