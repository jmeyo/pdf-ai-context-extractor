"""Core PDF table extraction logic."""
import sys
from pathlib import Path
import pandas as pd

try:
    import tabula
except ImportError:
    print("ERROR: tabula-py not installed")
    sys.exit(1)

class PDFTableExtractor:
    """Multi-strategy PDF table extractor."""

    def __init__(self, verbose=True):
        self.verbose = verbose

    def extract_tables(self, pdf_path):
        """Extract tables from PDF."""
        if self.verbose:
            print(f"Processing: {pdf_path}")

        methods = ['lattice', 'stream', 'guess']
        best_result = None
        best_method = None
        max_rows = 0

        for method in methods:
            try:
                if method == 'lattice':
                    tables = tabula.read_pdf(str(pdf_path), pages='all', lattice=True)
                elif method == 'stream':
                    tables = tabula.read_pdf(str(pdf_path), pages='all', stream=True)
                else:
                    tables = tabula.read_pdf(str(pdf_path), pages='all', guess=True)

                if tables:
                    combined = pd.concat(tables, ignore_index=True)
                    if len(combined) > max_rows:
                        max_rows = len(combined)
                        best_result = combined
                        best_method = method
            except Exception:
                continue

        return best_result, best_method

    def save_as_markdown(self, df, output_path):
        """Save DataFrame as Markdown table."""
        md_content = f"# Extracted from {output_path.stem}\n\n"
        md_content += df.to_markdown(index=False)
        md_content += f"\n\n---\n*Extracted: {pd.Timestamp.now()}*\n"
        output_path.write_text(md_content, encoding='utf-8')

    def process_directory(self, input_dir, output_dir, pattern="*.pdf"):
        """Process all PDF files in a directory."""
        pdf_files = sorted(Path(input_dir).glob(pattern))

        if not pdf_files:
            print(f"No PDF files found in {input_dir}")
            return

        print(f"Found {len(pdf_files)} PDF files")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for pdf_path in pdf_files:
            df, method = self.extract_tables(pdf_path)
            if df is not None:
                output_path = Path(output_dir) / pdf_path.stem
                df.to_csv(output_path.with_suffix('.csv'), index=False)
                print(f"  Processed: {pdf_path.name}")
