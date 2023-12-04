#!/bin/bash
# Quick setup script for PDF AI Context Extractor development

set -e

echo "════════════════════════════════════════════════════════════════════"
echo "   PDF AI CONTEXT EXTRACTOR - Quick Setup"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check Java
if ! command -v java &> /dev/null; then
    echo "⚠️  Java not found. tabula-py requires Java Runtime Environment"
    echo "   Install with:"
    echo "   - Ubuntu/Debian: sudo apt install default-jre"
    echo "   - macOS: brew install java"
    exit 1
fi

echo "✓ Java found: $(java -version 2>&1 | head -n 1)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install package in development mode
echo "Installing package in development mode..."
pip install -e ".[dev]"

# Install reportlab for sample generation
echo "Installing reportlab for test samples..."
pip install reportlab

# Generate test samples
echo ""
echo "Generating anonymized test PDFs..."
python tests/generate_samples.py

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run examples: python examples/run_examples.py"
echo "  3. Run tests: pytest"
echo ""
echo "To use the tool:"
echo "  pdf-extract path/to/document.pdf"
echo ""
echo "See README.md for full documentation"
echo ""
