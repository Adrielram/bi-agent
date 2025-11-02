"""
Herramientas semánticas para Agente BI (Fase 5+: Hybrid System - OPCIONAL)

NOTA: Este archivo es SOLO para Fase 5 (Post-MVP)
Require ChromaDB + sentence-transformers

Para usar estas herramientas:
1. Descomentar chromadb en requirements-hybrid.txt
2. Ejecutar: pip install -r requirements-hybrid.txt
3. Ejecutar: python scripts/setup_chromadb.py
4. Importar en agent/bi_agent.py con ENABLE_HYBRID=true
"""

from langchain.tools import tool
from typing import Optional
from pathlib import Path

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️  ChromaDB no disponible. Esta es Fase 5+ (opcional).")
    print("Para activar: pip install -r requirements-hybrid.txt")


EMPRESA_DOCS_PATH = Path(__file__).parent.parent / "empresa_docs"


@tool
def semantic_search(query: str, top_k: int = 5) -> str:
    """
    Búsqueda semántica avanzada usando embeddings (Fase 5+ OPCIONAL).
    
    Parámetros:
    - query: Pregunta o concepto a buscar (ej: "¿Qué consultores saben de machine learning?")
    - top_k: Número de resultados (default: 5)
    
    NOTA: Requiere ChromaDB inicializado
    
    Uso: Búsquedas conceptuales y semánticas
    Ejemplos:
    - semantic_search("consultores con experiencia en IA")
    - semantic_search("proyectos exitosos en 2024")
    
    Retorna: Resultados relevantes ordenados por similitud
    """
    if not CHROMADB_AVAILABLE:
        return (
            "❌ ChromaDB no está disponible (Fase 5+).\n"
            "Para habilitar:\n"
            "1. pip install -r requirements-hybrid.txt\n"
            "2. python scripts/setup_chromadb.py\n"
            "3. Establece ENABLE_HYBRID=true en .env"
        )
    
    try:
        # Conectar a ChromaDB
        client = chromadb.Client()
        collection = client.get_collection("empresa_datos")
        
        # Realizar búsqueda
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results["documents"] or not results["documents"][0]:
            return f"No semantic matches found for: {query}"
        
        # Formatear resultados
        formatted = []
        for i, doc in enumerate(results["documents"][0], 1):
            distance = results["distances"][0][i-1] if "distances" in results else "N/A"
            formatted.append(f"{i}. {doc}\n   (similarity: {distance:.3f})")
        
        return "\n".join(formatted)
    
    except Exception as e:
        return (
            f"Error en búsqueda semántica: {str(e)}\n"
            "Asegúrate de que ChromaDB fue inicializado con: python scripts/setup_chromadb.py"
        )


@tool
def semantic_similarity(text1: str, text2: str) -> str:
    """
    Compara similitud semántica entre dos textos.
    
    NOTA: Fase 5+ (Opcional, requiere ChromaDB)
    
    Parámetros:
    - text1: Primer texto
    - text2: Segundo texto
    
    Retorna: Puntuación de similitud 0-1
    """
    if not CHROMADB_AVAILABLE:
        return "❌ ChromaDB no disponible (Fase 5+). Ver instrucciones en semantic_search()."
    
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding1 = model.encode(text1)
        embedding2 = model.encode(text2)
        
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(
            [embedding1],
            [embedding2]
        )[0][0]
        
        return f"Similarity score: {similarity:.4f} (0=different, 1=identical)"
    
    except Exception as e:
        return f"Error: {str(e)}"
