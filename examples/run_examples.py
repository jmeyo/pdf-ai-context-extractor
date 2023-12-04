#!/usr/bin/env python3
"""
Example usage and test runner for PDF AI Context Extractor.

This script demonstrates the tool's capabilities and validates
that extraction works correctly on sample PDFs.
"""

from pathlib import Path
import sys

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pdf_ai_context_extractor import PDFTableExtractor, bank_statement_parser


def run_examples():
    """Run extraction examples on sample PDFs."""

    print("="*80)
    print("PDF AI CONTEXT EXTRACTOR - EXAMPLES")
    print("="*80)
    print()

    # Find sample PDFs
    samples_dir = Path(__file__).parent.parent / "tests" / "samples"

    if not samples_dir.exists():
        print(f"❌ Samples directory not found: {samples_dir}")
        print("   Please create sample PDFs in tests/samples/")
        return False

    pdf_files = list(samples_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDF files found in {samples_dir}")
        print("   Please add sample PDFs to tests/samples/")
        return False

    print(f"✓ Found {len(pdf_files)} sample PDF(s)")
    print()

    # Create output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Example 1: Basic extraction
    print("Example 1: Basic CSV Extraction")
    print("-" * 80)
    extractor = PDFTableExtractor(verbose=True)

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        df, method = extractor.extract_tables(pdf_file)

        if df is not None:
            print(f"✓ Extracted {len(df)} rows using {method} method")
            print(f"  Columns: {', '.join(str(c) for c in df.columns[:5])}")
            if len(df.columns) > 5:
                print(f"  ... and {len(df.columns) - 5} more")

            # Save to CSV
            output_file = output_dir / f"{pdf_file.stem}_basic.csv"
            df.to_csv(output_file, index=False)
            print(f"  Saved to: {output_file}")
        else:
            print(f"✗ Failed to extract")

    print("\n" + "="*80)

    # Example 2: With bank statement parser
    print("\nExample 2: Bank Statement Parser")
    print("-" * 80)

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        df, method = extractor.extract_tables(pdf_file)

        if df is not None:
            # Try applying bank statement parser
            parsed = bank_statement_parser(df, pdf_file.stem)

            if parsed is not None and not parsed.empty:
                print(f"✓ Parsed {len(parsed)} transactions")
                print(f"  Columns: {', '.join(parsed.columns)}")

                # Show sample
                print("\n  Sample transactions:")
                for idx, row in parsed.head(3).iterrows():
                    print(f"    {row['Date Operation']}: {row['Description'][:40]}... {row['Montant']:.2f}")

                # Save parsed
                output_file = output_dir / f"{pdf_file.stem}_parsed.csv"
                parsed.to_csv(output_file, index=False)
                print(f"\n  Saved to: {output_file}")
            else:
                print(f"  ⚠ Parser did not extract transactions (may not be bank statement format)")

    print("\n" + "="*80)

    # Example 3: Markdown output
    print("\nExample 3: Markdown Output for AI Prompts")
    print("-" * 80)

    for pdf_file in pdf_files[:1]:  # Just first file
        print(f"\nProcessing: {pdf_file.name}")
        df, method = extractor.extract_tables(pdf_file)

        if df is not None:
            # Limit to first 5 rows for demo
            sample = df.head(5)

            md_content = f"# Extracted from {pdf_file.stem}\n\n"
            md_content += sample.to_markdown(index=False)

            output_file = output_dir / f"{pdf_file.stem}_sample.md"
            output_file.write_text(md_content)

            print("✓ Created Markdown output:")
            print(md_content)
            print(f"\nSaved to: {output_file}")

    print("\n" + "="*80)
    print("\n✅ Examples complete!")
    print(f"   Output files in: {output_dir}")
    print()

    # Print summary
    extractor.print_summary()

    return True


def validate_installation():
    """Validate that all dependencies are installed."""
    print("Validating installation...")

    try:
        import tabula
        print("  ✓ tabula-py installed")
    except ImportError:
        print("  ✗ tabula-py not installed")
        print("    Install with: pip install tabula-py")
        return False

    try:
        import pandas
        print("  ✓ pandas installed")
    except ImportError:
        print("  ✗ pandas not installed")
        print("    Install with: pip install pandas")
        return False

    # Check Java
    import subprocess
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ Java installed")
        else:
            print("  ⚠ Java check returned non-zero")
    except FileNotFoundError:
        print("  ✗ Java not installed")
        print("    tabula-py requires Java Runtime Environment")
        return False

    print()
    return True


if __name__ == "__main__":
    print()
    if not validate_installation():
        print("\n❌ Installation validation failed")
        print("   Please install missing dependencies")
        sys.exit(1)

    print("✓ All dependencies installed\n")

    success = run_examples()

    sys.exit(0 if success else 1)
