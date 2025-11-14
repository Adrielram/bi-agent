#!/usr/bin/env python
"""
Tests for BI Agent - Fase 1
Unit tests for tools and agent functionality
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tools import discover_files, search, read_lines


class TestTools:
    """Test core tools"""

    def test_discover_files_returns_string(self):
        """discover_files should return a string"""
        result = discover_files.invoke({})
        assert isinstance(result, str)

    def test_discover_files_finds_data(self):
        """discover_files should find JSON files"""
        result = discover_files.invoke({})
        assert "json" in result.lower()

    def test_search_works(self):
        """search should find content in files"""
        # Search for something that should exist in our data
        result = search.invoke({"pattern": "Python"})
        assert isinstance(result, str)

    def test_search_with_filename_works(self):
        """search should work with specific filename"""
        result = search.invoke({"pattern": "Python", "filename": "consultores.json"})
        assert isinstance(result, str)

    def test_read_lines_works(self):
        """read_lines should read a file properly"""
        # Try reading first few lines of consultores.json which should exist
        result = read_lines.invoke({"filename": "consultores.json", "start": 0, "count": 10})
        assert isinstance(result, str)
        assert "error" not in result.lower()

    def test_read_lines_with_invalid_name(self):
        """read_lines should handle invalid filename gracefully"""
        result = read_lines.invoke({"filename": "nonexistent.json", "start": 0, "count": 10})
        # Should return error message, not crash
        assert isinstance(result, str)
        assert "error" in result.lower()


class TestToolDescriptions:
    """Test that tools have proper documentation"""

    def test_discover_files_has_description(self):
        """discover_files should have a description"""
        assert hasattr(discover_files, "description")
        assert len(discover_files.description) > 0

    def test_search_has_description(self):
        """search should have a description"""
        assert hasattr(search, "description")
        assert len(search.description) > 0

    def test_read_lines_has_description(self):
        """read_lines should have a description"""
        assert hasattr(read_lines, "description")
        assert len(read_lines.description) > 0


class TestDataAvailability:
    """Test that required data files exist"""
    
    def test_empresa_docs_directory_exists(self):
        """empresa_docs directory should exist"""
        assert Path("empresa_docs").exists()
    
    def test_consultores_json_exists(self):
        """consultores.json should exist"""
        assert Path("empresa_docs/consultores.json").exists()
    
    def test_proyectos_json_exists(self):
        """proyectos.json should exist"""
        assert Path("empresa_docs/proyectos.json").exists()
    
    def test_clientes_json_exists(self):
        """clientes.json should exist"""
        assert Path("empresa_docs/clientes.json").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
