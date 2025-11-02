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

from agent.tools import discover_files, read_collection, search_by_text


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
    
    def test_read_collection_works(self):
        """read_collection should read a JSON file"""
        # Try reading consultores which should exist
        result = read_collection.invoke({"collection_name": "consultores"})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_read_collection_with_invalid_name(self):
        """read_collection should handle invalid collection names gracefully"""
        result = read_collection.invoke({"collection_name": "nonexistent"})
        # Should return error message or empty, not crash
        assert isinstance(result, str)
    
    def test_search_by_text_finds_content(self):
        """search_by_text should find content"""
        # Search for something that should exist in our data
        result = search_by_text.invoke({"query": "Python"})
        assert isinstance(result, str)


class TestToolDescriptions:
    """Test that tools have proper documentation"""
    
    def test_discover_files_has_description(self):
        """discover_files should have a description"""
        assert hasattr(discover_files, "description")
        assert len(discover_files.description) > 0
    
    def test_read_collection_has_description(self):
        """read_collection should have a description"""
        assert hasattr(read_collection, "description")
        assert len(read_collection.description) > 0
    
    def test_search_by_text_has_description(self):
        """search_by_text should have a description"""
        assert hasattr(search_by_text, "description")
        assert len(search_by_text.description) > 0


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
