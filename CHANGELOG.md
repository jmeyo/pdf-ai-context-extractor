# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-26

### Added
- Multi-language support for French, German, and English documents
- Automatic locale detection from filename patterns
- Content-based locale detection using keyword analysis
- Locale-aware date parsing (DD/MM/YYYY, DD.MM.YYYY, MM/DD/YYYY)
- Locale-aware amount parsing (different decimal/thousands separators)
- CLI options: `--locale {fr,de,en}` and `--no-auto-detect`
- Python API: `default_locale`, `auto_detect_locale`, `explicit_locale` parameters
- Comprehensive locale detection tests
- Multi-strategy PDF table extraction (lattice, stream, guess)
- Bank statement parser with transaction extraction
- CSV and Markdown output formats
- Batch directory processing
- Command-line interface (`pdf-extract`)
- Python API for programmatic use
- GitHub Actions CI/CD pipeline
- PyPI package configuration
- Comprehensive documentation
- MIT License
- Contributing guidelines

### Locale Support Details
- **French (fr)**: Default locale
  - Date format: DD/MM/YYYY or DD.MM.YYYY
  - Amount format: 1 234,56 € (space thousands, comma decimal)
  - Keywords: solde, crédit, débit, virement, prélèvement, etc.

- **German (de)**:
  - Date format: DD.MM.YYYY
  - Amount format: 1.234,56 € (dot thousands, comma decimal)
  - Keywords: saldo, kredit, lastschrift, überweisung, betrag, etc.

- **English (en)**:
  - Date format: MM/DD/YYYY or YYYY-MM-DD
  - Amount format: 1,234.56 $ (comma thousands, dot decimal)
  - Keywords: balance, credit, debit, transfer, payment, etc.

### Detection Priority
1. Explicit `--locale` parameter
2. Filename patterns (_fr, _de, _en, français, deutsch, english, etc.)
3. Content analysis (keyword matching with confidence threshold)
4. Default locale (French)

## [Unreleased]

### Planned Features
- Additional parsers for invoices, receipts, and forms
- More language support (Spanish, Italian, Portuguese, etc.)
- OCR support for scanned PDFs
- Excel and JSON output formats
- Web UI (Flask/Streamlit)
- Docker image for easy deployment

---

**Note**: This is the initial release of PDF AI Context Extractor. The project was created to provide clean, structured PDF data extraction optimized for AI agent consumption, with a focus on French administrative documents but supporting multiple languages.
