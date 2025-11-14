"""
Herramientas optimizadas para Agente BI - VERSIÓN FINAL
3 tools minimalistas que cubren todos los casos de uso

Patrón: git grep multi-file + progressive reading
"""

from langchain.tools import tool
from typing import Optional, Dict, Any, List
from pathlib import Path
import json
import subprocess
import os

EMPRESA_DOCS_PATH = Path(__file__).parent.parent / "empresa_docs"

# ============================================
# LÍMITES DE SEGURIDAD
# ============================================

MAX_LINES_PER_CALL = 200
MAX_PREVIEW_LENGTH = 150
MAX_SEARCH_RESULTS = 20
EXPENSIVE_LINE_THRESHOLD = 400


# ============================================
# TOOL 1: discover_files (EXPLORACIÓN INICIAL)
# ============================================

@tool
def discover_files() -> str:
    """
    📁 Lista archivos disponibles con metadata básica.
    
    Returns:
        Lista de archivos con nombre, tipo, tamaño en líneas
    
    Example:
        discover_files()
        → "consultores.json (json, 1250 lines)
           proyectos.json (json, 3400 lines)
           ..."
    
    USA ESTO PRIMERO para ver qué archivos hay disponibles.
    """
    if not EMPRESA_DOCS_PATH.exists():
        return "❌ Directory 'empresa_docs/' not found"
    
    files = list(EMPRESA_DOCS_PATH.glob("*"))
    if not files:
        return "❌ No files found in empresa_docs/"
    
    file_list = []
    
    for file in sorted(files):
        if not file.is_file():
            continue
        
        try:
            # Count lines fast
            with open(file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            
            # Detect type from extension
            ext = file.suffix.lstrip('.').lower()
            type_map = {
                'json': 'json', 'csv': 'csv', 'md': 'markdown',
                'txt': 'text', 'log': 'log', 'py': 'code', 'js': 'code'
            }
            file_type = type_map.get(ext, 'unknown')
            
            # Size category
            if line_count < 100:
                size = "tiny"
            elif line_count < 500:
                size = "small"
            elif line_count < 2000:
                size = "medium"
            elif line_count < 10000:
                size = "large"
            else:
                size = "huge"
            
            file_list.append({
                "name": file.name,
                "type": file_type,
                "lines": line_count,
                "size": size
            })
        except Exception as e:
            file_list.append({
                "name": file.name,
                "type": "error",
                "lines": 0,
                "size": "unknown"
            })
    
    # Format output
    output = "📂 Available files in empresa_docs/:\n\n"
    
    for f in file_list:
        icon = {"json": "📊", "markdown": "📝", "text": "📄", "code": "💻", "log": "📋"}.get(f['type'], "📄")
        output += f"{icon} {f['name']}\n"
        output += f"   Type: {f['type']}, Lines: {f['lines']}, Size: {f['size']}\n\n"
    
    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    output += "💡 Next steps:\n"
    output += "   • search(pattern) - Search across ALL files\n"
    output += "   • read_lines(filename, start, count) - Read specific file\n"
    
    return output


# ============================================
# TOOL 2: search (MULTI-FILE SEARCH - git grep)
# ============================================

@tool
def search(pattern: str, filename: Optional[str] = None, case_sensitive: bool = False) -> str:
    """
    🔍 BÚSQUEDA ULTRA-RÁPIDA con git grep (busca en TODOS los archivos).
    
    Esta es la herramienta MÁS IMPORTANTE. Úsala SIEMPRE que busques algo.
    
    Args:
        pattern: Texto a buscar (ej: "React", "2024", "Juan Pérez")
        filename: (Opcional) Limitar búsqueda a un archivo específico
        case_sensitive: False por defecto (búsqueda case-insensitive)
    
    Returns:
        JSON agrupado por archivo con:
        - Total de matches por archivo
        - Line numbers
        - Previews de los primeros matches
        - Sugerencias de qué leer después
    
    Examples:
        search("React")
        → Busca "React" en TODOS los archivos, retorna matches agrupados por archivo
        
        search("React", filename="consultores.json")
        → Busca solo en consultores.json
        
        search("CONS-012")
        → Encuentra en qué archivos se menciona este ID
    
    IMPORTANTE:
    - Esta tool es GRATIS (no consume tokens del contenido)
    - Retorna SOLO metadata (line numbers + previews cortos)
    - git grep escanea archivos gigantes en milisegundos
    - Usa esto ANTES de read_lines() para saber QUÉ leer
    
    PATRÓN RECOMENDADO:
    1. search("keyword") → Ve en qué archivos aparece
    2. read_lines(filename, around_line, count) → Lee contexto completo
    """
    
    try:
        # Verificar si estamos en un repo git
        is_git_repo = (EMPRESA_DOCS_PATH.parent / ".git").exists()
        
        if is_git_repo:
            # OPCIÓN 1: git grep (ULTRA RÁPIDO)
            cmd = ["git", "grep", "-n"]  # -n = line numbers
            
            if not case_sensitive:
                cmd.append("-i")  # case insensitive
            
            cmd.append(pattern)
            
            # Si se especifica filename, limitar búsqueda
            if filename:
                search_path = f"empresa_docs/{filename}"
            else:
                search_path = "empresa_docs/"
            
            cmd.append(search_path)
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=EMPRESA_DOCS_PATH.parent,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return _parse_git_grep_output(result.stdout, pattern, filename)
                elif result.returncode == 1:
                    # No matches found
                    return json.dumps({
                        "matches": 0,
                        "pattern": pattern,
                        "message": f"No matches found for '{pattern}'" + (f" in {filename}" if filename else " in any file")
                    }, indent=2)
                else:
                    # Error - fall back to Python grep
                    pass
                    
            except subprocess.TimeoutExpired:
                return json.dumps({"error": "Search timeout (>10s) - try narrowing search"})
            except Exception:
                pass  # Fall back to Python grep
        
        # OPCIÓN 2: Python grep (fallback si no hay git)
        return _python_grep(pattern, filename, case_sensitive)
        
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})


def _parse_git_grep_output(output: str, pattern: str, target_file: Optional[str]) -> str:
    """Parse git grep output y agrupar por archivo"""
    
    lines = output.strip().split("\n")
    if not lines or lines == ['']:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": f"No matches found for '{pattern}'"
        }, indent=2)
    
    # Agrupar por archivo
    by_file = {}
    
    for line in lines:
        # Format: empresa_docs/file.json:line_num:content
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        
        filepath = parts[0].replace("empresa_docs/", "")
        line_num = int(parts[1]) - 1  # 0-indexed
        content = parts[2]
        
        # Skip very long lines (noise)
        if len(content) > EXPENSIVE_LINE_THRESHOLD:
            continue
        
        if filepath not in by_file:
            by_file[filepath] = []
        
        by_file[filepath].append({
            "line": line_num,
            "preview": content.strip()[:MAX_PREVIEW_LENGTH]
        })
    
    if not by_file:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": "Matches found but all lines were too long (noise filtered)"
        }, indent=2)
    
    # Limitar resultados por archivo
    total_matches = sum(len(matches) for matches in by_file.values())
    
    result = {
        "matches": total_matches,
        "pattern": pattern,
        "files_with_matches": len(by_file),
        "results_by_file": {}
    }
    
    for filepath, matches in sorted(by_file.items()):
        limited_matches = matches[:MAX_SEARCH_RESULTS]
        
        result["results_by_file"][filepath] = {
            "total_matches": len(matches),
            "showing": len(limited_matches),
            "line_numbers": [m["line"] for m in limited_matches],
            "preview_samples": limited_matches[:5]  # Solo primeros 5 previews
        }
        
        if len(matches) > MAX_SEARCH_RESULTS:
            result["results_by_file"][filepath]["note"] = f"Showing first {MAX_SEARCH_RESULTS} of {len(matches)} matches"
    
    # Add suggestions
    if len(by_file) == 1:
        only_file = list(by_file.keys())[0]
        first_line = by_file[only_file][0]["line"]
        result["suggestion"] = f"Use read_lines('{only_file}', start={first_line}, count=50) to see full context"
    else:
        result["suggestion"] = "Multiple files have matches. Use read_lines(filename, start, count) on the most relevant file"
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def _python_grep(pattern: str, filename: Optional[str], case_sensitive: bool) -> str:
    """Fallback: Python-based grep when git is not available"""
    
    pattern_lower = pattern if case_sensitive else pattern.lower()
    by_file = {}
    
    # Determine which files to search
    if filename:
        files = [EMPRESA_DOCS_PATH / filename]
    else:
        files = list(EMPRESA_DOCS_PATH.glob("*"))
    
    for filepath in files:
        if not filepath.is_file():
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    search_line = line if case_sensitive else line.lower()
                    
                    if pattern_lower in search_line:
                        # Skip very long lines
                        if len(line) > EXPENSIVE_LINE_THRESHOLD:
                            continue
                        
                        filename_key = filepath.name
                        if filename_key not in by_file:
                            by_file[filename_key] = []
                        
                        by_file[filename_key].append({
                            "line": i,
                            "preview": line.strip()[:MAX_PREVIEW_LENGTH]
                        })
                        
                        # Limit per file to avoid memory issues
                        if len(by_file[filename_key]) >= MAX_SEARCH_RESULTS * 2:
                            break
        except Exception:
            continue
    
    if not by_file:
        return json.dumps({
            "matches": 0,
            "pattern": pattern,
            "message": f"No matches found for '{pattern}'"
        }, indent=2)
    
    # Format similar to git grep output
    total_matches = sum(len(matches) for matches in by_file.values())
    
    result = {
        "matches": total_matches,
        "pattern": pattern,
        "files_with_matches": len(by_file),
        "results_by_file": {}
    }
    
    for filepath, matches in sorted(by_file.items()):
        limited_matches = matches[:MAX_SEARCH_RESULTS]
        
        result["results_by_file"][filepath] = {
            "total_matches": len(matches),
            "showing": len(limited_matches),
            "line_numbers": [m["line"] for m in limited_matches],
            "preview_samples": limited_matches[:5]
        }
    
    return json.dumps(result, indent=2, ensure_ascii=False)


# ============================================
# TOOL 3: read_lines (UNIFIED READING - context + chunked)
# ============================================

@tool
def read_lines(filename: str, start: int = 0, count: int = 50) -> str:
    """
    📖 Lee líneas de un archivo (unified: chunked + context reading).
    
    Esta tool reemplaza tanto read_lines() como read_context():
    - Para lectura chunked: read_lines("file.json", 0, 100)
    - Para contexto: read_lines("file.json", around_line=45, count=20)
    
    LÍMITES DE SEGURIDAD:
    - Máximo 200 líneas por llamada
    - Filtra líneas >400 caracteres (ruido)
    
    Args:
        filename: Nombre del archivo
        start: Línea de inicio (0-indexed)
        count: Cantidad de líneas a leer
    
    Returns:
        JSON con contenido + metadata
    
    Examples:
        # Lectura chunked (exploración)
        read_lines("consultores.json", start=0, count=100)
        
        # Lectura de contexto (después de search)
        search("React") → match en línea 45
        read_lines("consultores.json", start=40, count=20)  # Lee 40-60 (contexto alrededor de 45)
        
        # Lectura de primeras líneas (entender estructura)
        read_lines("proyectos.json", start=0, count=20)
    
    USO RECOMENDADO:
    1. Después de search(): Lee contexto alrededor de matches
    2. Para archivos <500 líneas: Lee en chunks de 50-100
    3. Para archivos >500 líneas: USA search() primero, luego lee solo lo necesario
    4. REFLEXIONA después de cada lectura: ¿Ya tengo suficiente info?
    
    PATRÓN COMÚN:
    search("keyword") → encuentra línea X → read_lines(filename, X-10, 20) → contexto completo
    """
    
    file_path = EMPRESA_DOCS_PATH / filename
    
    if not file_path.exists():
        return json.dumps({"error": f"❌ File '{filename}' not found in empresa_docs/"})
    
    # HARD LIMIT
    if count > MAX_LINES_PER_CALL:
        return json.dumps({
            "error": f"❌ Requested {count} lines, but max allowed is {MAX_LINES_PER_CALL}",
            "suggestion": f"Use multiple calls with count={MAX_LINES_PER_CALL} or search() first to narrow down"
        })
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        total_lines = len(all_lines)
        
        # Validate range
        if start < 0:
            start = 0
        if start >= total_lines:
            return json.dumps({
                "error": f"❌ Start line {start} exceeds file length ({total_lines} lines)",
                "suggestion": f"File has {total_lines} lines. Use start < {total_lines}"
            })
        
        end = min(start + count, total_lines)
        chunk = all_lines[start:end]
        
        # Filter very long lines
        filtered_chunk = []
        skipped = 0
        
        for i, line in enumerate(chunk, start=start):
            if len(line) > EXPENSIVE_LINE_THRESHOLD:
                skipped += 1
                filtered_chunk.append(f"[Line {i}: too long ({len(line)} chars) - skipped for brevity]\n")
            else:
                # Add line numbers for easier reference
                filtered_chunk.append(f"{i:4d} | {line}")
        
        result = {
            "filename": filename,
            "content": "".join(filtered_chunk),
            "metadata": {
                "lines_read": f"{start} to {end-1}",
                "lines_returned": len(chunk),
                "lines_skipped": skipped,
                "total_file_lines": total_lines,
                "percentage_read": f"{(end/total_lines)*100:.1f}%",
                "has_more": end < total_lines
            }
        }
        
        # Add helpful suggestions
        if end < total_lines:
            remaining = total_lines - end
            next_chunk_size = min(remaining, MAX_LINES_PER_CALL)
            result["metadata"]["next_call"] = f"read_lines('{filename}', start={end}, count={next_chunk_size})"
        
        if skipped > 0:
            result["metadata"]["note"] = f"⚠️ Skipped {skipped} very long lines (likely minified/generated code)"
        
        # Warning for large files
        if total_lines > 2000 and start == 0 and count > 100:
            result["metadata"]["warning"] = "⚠️ Large file detected. Consider using search() first to locate relevant sections"
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"❌ Failed to read file: {str(e)}"})