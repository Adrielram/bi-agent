"""
Herramientas genéricas para Agente BI (Fase 1-4: Copilot-Like)

Patrón de herramientas agnósticas:
- discover_files(): Descubre archivos en empresa_docs/
- read_collection(): Lee colecciones completas (JSON, CSV, etc.)
- search_by_text(): Búsqueda exacta de texto

Nota: semantic_search() está en tools_semantic.py (Fase 5+)
"""

from langchain.tools import tool
from typing import Optional
from pathlib import Path
import json
import os

EMPRESA_DOCS_PATH = Path(__file__).parent.parent / "empresa_docs"


@tool
def discover_files() -> str:
    """
    Descubre archivos disponibles en empresa_docs/.
    
    Uso: Cuando el usuario pregunta "¿Qué datos tienes?" o similar
    
    Retorna: Lista de archivos con descripción de contenido
    """
    if not EMPRESA_DOCS_PATH.exists():
        return "No directory 'empresa_docs/' found"
    
    files = list(EMPRESA_DOCS_PATH.glob("*"))
    if not files:
        return "No files found in empresa_docs/"
    
    file_list = []
    for file in files:
        file_list.append(f"- {file.name}")
    
    return "Available files:\n" + "\n".join(file_list)


@tool
def read_collection(collection_name: str) -> str:
    """
    Lee una colección completa (JSON, CSV, texto).
    
    Parámetros:
    - collection_name: Nombre del archivo (ej: "consultores.json", "proyectos.json")
    
    Uso: Cuando necesitas datos completos de una colección
    Ejemplo: "Muéstrame todos los consultores" → read_collection("consultores.json")
    
    Retorna: Contenido formateado del archivo
    """
    file_path = EMPRESA_DOCS_PATH / collection_name
    
    if not file_path.exists():
        return f"File '{collection_name}' not found in empresa_docs/"
    
    try:
        if collection_name.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def search_by_text(query: str, collection_name: Optional[str] = None) -> str:
    """
    Búsqueda exacta de texto en colecciones.
    
    Parámetros:
    - query: Término de búsqueda (ej: "Python", "senior", "2024")
    - collection_name: (Opcional) Archivo específico a buscar
    
    Uso: Búsquedas rápidas de palabra clave
    Ejemplos:
    - search_by_text("Python") → busca "Python" en todos los archivos
    - search_by_text("2024", "proyectos.json") → busca en archivo específico
    
    Retorna: Líneas/fragmentos que coinciden
    """
    if collection_name:
        files = [EMPRESA_DOCS_PATH / collection_name]
    else:
        files = list(EMPRESA_DOCS_PATH.glob("*"))
    
    results = []
    query_lower = query.lower()
    
    for file in files:
        if not file.is_file():
            continue
        
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if query_lower in content.lower():
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if query_lower in line.lower():
                            results.append(f"[{file.name}:{i+1}] {line}")
        except Exception as e:
            continue
    
    if not results:
        return f"No matches found for '{query}'"
    
    return "\n".join(results[:10])  # Limita a 10 primeros resultados
