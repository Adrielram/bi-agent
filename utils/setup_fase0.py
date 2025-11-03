#!/usr/bin/env python
"""
Fase 0 Setup Script - Verificación de la configuración inicial
Ejecutar: python setup_fase0.py
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv


def print_section(title):
    """Print una sección formateada"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def check_python_version():
    """Verificar versión de Python"""
    print_section("✅ Verificando Python")
    version = sys.version_info
    print(f"  Python: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 11:
        print("  ✅ Versión compatible")
        return True
    else:
        print("  ❌ Se requiere Python 3.11+")
        return False


def check_directory_structure():
    """Verificar estructura de directorios"""
    print_section("✅ Verificando estructura de directorios")
    required_dirs = [
        "agent",
        "utils",
        "tests",
        "logs",
        "data",
        "config",
        "empresa_docs"
    ]
    
    all_present = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (FALTA)")
            all_present = False
    
    return all_present


def check_files():
    """Verificar archivos críticos"""
    print_section("✅ Verificando archivos críticos")
    required_files = {
        ".env.example": "Plantilla de configuración",
        ".env": "Configuración (NO commitar)",
        ".gitignore": "Exclusiones de git",
        ".python-version": "Versión de Python",
        "requirements-base.txt": "Dependencias MVP",
        "requirements-hybrid.txt": "Dependencias Fase 5+",
        "README.md": "Documentación principal",
        "QUICK_START.md": "Guía de inicio rápido",
    }
    
    all_present = True
    for filename, description in required_files.items():
        path = Path(filename)
        if path.exists():
            print(f"  ✅ {filename} - {description}")
        else:
            print(f"  ⚠️  {filename} (FALTA)")
            all_present = False
    
    return all_present


def check_env_variables():
    """Verificar variables de entorno"""
    print_section("✅ Verificando variables de entorno")
    
    load_dotenv()
    
    required = {
        "GOOGLE_API_KEY": "Google Gemini API Key",
        "LANGCHAIN_API_KEY": "LangSmith API Key",
        "LANGCHAIN_PROJECT": "Nombre del proyecto"
    }
    
    all_set = True
    for key, description in required.items():
        value = os.getenv(key)
        if value and value != f"tu_{key.lower()}_aqui":
            print(f"  ✅ {key}")
        else:
            print(f"  ❌ {key} (NO configurado)")
            print(f"     └─ {description}")
            all_set = False
    
    return all_set


def check_dependencies():
    """Verificar dependencias instaladas"""
    print_section("✅ Verificando dependencias instaladas")
    
    required_packages = {
        "langchain": "LangChain framework",
        "langchain_google_genai": "Google Gemini integration",
        "fastapi": "API framework",
        "pydantic": "Data validation",
        "dotenv": "Environment variables",
        "pytest": "Testing framework"
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            # Handle special case for dotenv
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package} (NO instalado)")
            print(f"     └─ {description}")
            all_installed = False
    
    return all_installed


def check_data_structure():
    """Verificar estructura de datos"""
    print_section("✅ Verificando datos disponibles")
    
    data_dir = Path("empresa_docs")
    if data_dir.exists():
        files = list(data_dir.glob("*.json"))
        if files:
            print(f"  ✅ Encontrados {len(files)} archivos de datos:")
            for f in sorted(files):
                size = f.stat().st_size / 1024  # KB
                print(f"     • {f.name} ({size:.1f} KB)")
        else:
            print("  ⚠️  No hay archivos de datos en empresa_docs/")
            print("     └─ Agrega JSON/CSV con tus datos de negocio")
    else:
        print("  ❌ Directorio empresa_docs/ no existe")
    
    return True


def print_summary(results):
    """Imprimir resumen final"""
    print_section("📋 RESUMEN DE VERIFICACIÓN")
    
    checks = [
        ("Python correcto", results.get("python", False)),
        ("Directorios creados", results.get("dirs", False)),
        ("Archivos de configuración", results.get("files", False)),
        ("Variables de entorno", results.get("env", False)),
        ("Dependencias instaladas", results.get("deps", False)),
        ("Datos disponibles", results.get("data", False))
    ]
    
    total = len(checks)
    passed = sum(1 for _, result in checks if result)
    
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
    
    print(f"\nResultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n✨ ¡SETUP COMPLETADO! Listo para Fase 1 ✨")
        return True
    else:
        print("\n⚠️  Se requieren algunas correcciones antes de continuar")
        return False


def main():
    """Ejecutar todas las verificaciones"""
    print("\n")
    print("=" * 70)
    print("  FASE 0 - SETUP VERIFICATION")
    print("=" * 70)
    print()
    print("  AI Sales Assistant MVP - BI Agent Setup Check")
    print("=" * 70 + "\n")
    
    results = {
        "python": check_python_version(),
        "dirs": check_directory_structure(),
        "files": check_files(),
        "env": check_env_variables(),
        "deps": check_dependencies(),
        "data": check_data_structure()
    }
    
    success = print_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
