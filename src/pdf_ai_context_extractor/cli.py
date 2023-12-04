"""Command-line interface for PDF extractor."""
import argparse
import sys
from pathlib import Path
from .core import PDFTableExtractor
from .parsers import PARSERS

def main():
    parser = argparse.ArgumentParser(
        description='PDF AI Context Extractor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('input', type=Path, help='PDF file or directory')
    parser.add_argument('-o', '--output', type=Path, help='Output directory')
    parser.add_argument('-f', '--format', choices=['csv', 'md', 'both'],
                       default='csv', help='Output format')
    parser.add_argument('-p', '--pattern', default='*.pdf',
                       help='Glob pattern for files')
    parser.add_argument('--parser', choices=list(PARSERS.keys()),
                       help='Custom parser')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Suppress output')

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: {args.input} does not exist")
        sys.exit(1)

    output_dir = args.output or args.input.parent / 'extracted'
    extractor = PDFTableExtractor(verbose=not args.quiet)

    if args.input.is_file():
        df, method = extractor.extract_tables(args.input)
        if df is not None:
            if args.format in ('csv', 'both'):
                df.to_csv(output_dir / f"{args.input.stem}.csv", index=False)
            if args.format in ('md', 'both'):
                extractor.save_as_markdown(df, output_dir / f"{args.input.stem}.md")
    else:
        extractor.process_directory(args.input, output_dir, args.pattern)

if __name__ == "__main__":
    main()
