#!/usr/bin/env python
"""
Structured Logging Configuration for BI Agent
JSON logs for observability + LangSmith integration
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Any


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, "user_input"):
            log_data["user_input"] = record.user_input[:100]  # First 100 chars
        if hasattr(record, "latency"):
            log_data["latency_seconds"] = record.latency
        if hasattr(record, "status"):
            log_data["status"] = record.status
        if hasattr(record, "token_count"):
            log_data["tokens"] = record.token_count
        if hasattr(record, "tool_name"):
            log_data["tool"] = record.tool_name
        
        # Include exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(
    name: str = "bi_agent",
    log_file: Optional[str] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configure structured logging with both file and console output
    
    Args:
        name: Logger name (typically __name__)
        log_file: Path to log file (default: logs/app.log)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Default log file
    if log_file is None:
        log_file = "logs/app.log"
    
    # Create logs directory if needed
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # File handler - JSON format
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_formatter = StructuredFormatter()
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler - Pretty format for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_query(
    logger: logging.Logger,
    user_input: str,
    status: str = "started",
    latency: Optional[float] = None,
    token_count: Optional[int] = None
) -> None:
    """
    Log a query with structured fields
    
    Args:
        logger: Logger instance
        user_input: User's query
        status: Query status (started, completed, error)
        latency: Query latency in seconds
        token_count: Total tokens used
    """
    
    extra = {
        "user_input": user_input,
        "status": status
    }
    
    if latency is not None:
        extra["latency"] = latency
    if token_count is not None:
        extra["token_count"] = token_count
    
    level = logging.ERROR if status == "error" else logging.INFO
    logger.log(level, f"Query [{status}]: {user_input[:50]}...", extra=extra)


def log_tool_call(
    logger: logging.Logger,
    tool_name: str,
    input_data: str,
    status: str = "completed",
    latency: Optional[float] = None,
    output_size: Optional[int] = None
) -> None:
    """
    Log a tool invocation
    
    Args:
        logger: Logger instance
        tool_name: Name of the tool
        input_data: Input to the tool
        status: Tool status
        latency: Tool execution time
        output_size: Size of output
    """
    
    extra = {
        "tool_name": tool_name,
        "status": status
    }
    
    if latency is not None:
        extra["latency"] = latency
    
    logger.info(
        f"Tool [{tool_name}] {status}: {input_data[:50]}...",
        extra=extra
    )


# Module-level logger for easy import
logger = setup_logging("bi_agent")


if __name__ == "__main__":
    # Test logging
    test_logger = setup_logging("test_logger")
    
    test_logger.info("Test info message")
    test_logger.warning("Test warning message")
    test_logger.error("Test error message")
    
    # Test structured query logging
    log_query(
        test_logger,
        "Busca Python",
        status="completed",
        latency=2.34,
        token_count=150
    )
    
    # Test tool logging
    log_tool_call(
        test_logger,
        "search_by_text",
        "Python",
        status="completed",
        latency=0.45
    )
    
    print("\n[SUCCESS] Logging configured correctly")
    print("[*] Check logs/app.log for JSON output")
