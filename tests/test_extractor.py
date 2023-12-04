"""Tests for PDF extractor."""
import pytest
from pathlib import Path
from pdf_ai_context_extractor import PDFTableExtractor

def test_extractor_initialization():
    """Test extractor can be initialized."""
    extractor = PDFTableExtractor(verbose=False)
    assert extractor is not None

def test_extractor_verbose_mode():
    """Test verbose mode setting."""
    extractor = PDFTableExtractor(verbose=True)
    assert extractor.verbose is True
