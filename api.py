#!/usr/bin/env python
"""
Fase 2 - FastAPI Server + Prometheus Metrics
Main API server for BI Agent with full monitoring
"""

import os
import time
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import uvicorn

from agent.bi_agent import BIAgent
from utils.logging_config import logger, log_query

# Initialize FastAPI
app = FastAPI(
    title="BI Agent API",
    description="Business Intelligence Agent with Prometheus Monitoring",
    version="1.0.0"
)

# Initialize Agent
try:
    agent = BIAgent()
    logger.info("Agent initialized successfully on startup")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    agent = None

# ============================================================================
# Prometheus Metrics
# ============================================================================

# Counter for total queries
query_counter = Counter(
    'bi_agent_queries_total',
    'Total number of queries processed',
    ['status']
)

# Histogram for query latency
query_latency = Histogram(
    'bi_agent_query_latency_seconds',
    'Query latency in seconds',
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

# Counter for errors
error_counter = Counter(
    'bi_agent_errors_total',
    'Total number of errors',
    ['error_type']
)

# ============================================================================
# Pydantic Models
# ============================================================================

class QueryRequest(BaseModel):
    """Query request model"""
    user_input: str = Field(..., description="User question or query", min_length=1, max_length=1000)
    stream: bool = Field(default=False, description="Whether to stream response")
    timeout: Optional[int] = Field(default=30, description="Query timeout in seconds")


class QueryResponse(BaseModel):
    """Query response model"""
    query: str = Field(..., description="Original query")
    response: str = Field(..., description="Agent response")
    latency_seconds: float = Field(..., description="Query latency")
    timestamp: str = Field(..., description="Query timestamp")
    model: str = Field(default="gemini-2.0-flash", description="LLM model used")
    status: str = Field(default="success", description="Response status")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agent_ready: bool
    timestamp: str
    version: str


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if agent else "unhealthy",
        agent_ready=agent is not None,
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Execute a query on the BI Agent
    
    Example:
        ```
        POST /query
        {
            "user_input": "¿Qué datos tienes disponibles?"
        }
        ```
    """
    if not agent:
        error_counter.labels(error_type="agent_not_ready").inc()
        raise HTTPException(
            status_code=503,
            detail="Agent is not initialized. Check logs."
        )
    
    if not request.user_input or not request.user_input.strip():
        error_counter.labels(error_type="invalid_input").inc()
        raise HTTPException(
            status_code=400,
            detail="user_input cannot be empty"
        )
    
    start_time = time.time()
    
    try:
        # Log the query start
        logger.info(f"API Query received: {request.user_input[:100]}...")
        
        # Execute query
        response_text = agent.query(request.user_input)
        
        # Calculate latency
        latency = time.time() - start_time
        
        # Record metrics
        query_counter.labels(status="success").inc()
        query_latency.observe(latency)
        
        # Log the response
        log_query(logger, request.user_input, latency, "success")
        
        logger.info(f"API Query completed in {latency:.2f}s")
        
        return QueryResponse(
            query=request.user_input,
            response=response_text,
            latency_seconds=latency,
            timestamp=datetime.now().isoformat(),
            model="gemini-2.0-flash",
            status="success"
        )
        
    except Exception as e:
        latency = time.time() - start_time
        
        # Record error metrics
        query_counter.labels(status="error").inc()
        error_counter.labels(error_type=type(e).__name__).inc()
        
        # Log error
        logger.error(f"Query failed: {str(e)}")
        log_query(logger, request.user_input, latency, "error")
        
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return JSONResponse(
        content=generate_latest(REGISTRY).decode("utf8"),
        media_type="text/plain"
    )


@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "name": "BI Agent API",
        "version": "1.0.0",
        "description": "Business Intelligence Agent with Prometheus Monitoring",
        "endpoints": {
            "/health": "Health check",
            "/query": "Execute a query (POST)",
            "/metrics": "Prometheus metrics",
            "/docs": "Swagger UI documentation",
            "/redoc": "ReDoc documentation"
        },
        "gemini_model": "gemini-2.0-flash",
        "features": [
            "LangChain + Google Gemini 2.0",
            "Prometheus metrics",
            "LangSmith tracing",
            "Structured JSON logging",
            "Tool-based reasoning (ReAct pattern)"
        ]
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    error_counter.labels(error_type="unhandled").inc()
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# ============================================================================
# Lifespan Events
# ============================================================================

@app.on_event("startup")
async def startup():
    """Startup event"""
    logger.info("BI Agent API starting up...")
    if agent:
        logger.info("✅ Agent ready for queries")
    else:
        logger.warning("⚠️  Agent not initialized")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event"""
    logger.info("BI Agent API shutting down...")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Get config from environment
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", "8001"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting BI Agent API on {host}:{port}")
    logger.info(f"Docs available at: http://{host}:{port}/docs")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
