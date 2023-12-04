# Contributing to PDF AI Context Extractor

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Java version)
- Sample PDF (if possible, anonymized)

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- Example use cases

### Pull Requests

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest
   python examples/run_examples.py
   ```

5. **Format your code**
   ```bash
   black src tests examples
   flake8 src
   ```

6. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pdf-ai-context-extractor.git
cd pdf-ai-context-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Generate test samples
python tests/generate_samples.py

# Run tests
pytest
```

## Code Style

- Follow PEP 8
- Use `black` for formatting (line length: 100)
- Add type hints where possible
- Write docstrings for public functions

## Adding Parsers

To add a new parser:

1. Add your parser function to `src/pdf_ai_context_extractor/parsers.py`:

```python
def your_parser(df: pd.DataFrame, filename: str) -> Optional[pd.DataFrame]:
    """
    Description of what this parser does.

    Args:
        df: Raw extracted DataFrame
        filename: Source filename

    Returns:
        Parsed DataFrame or None
    """
    # Your parsing logic
    return parsed_df
```

2. Register it in the `PARSERS` dictionary:

```python
PARSERS = {
    'bank_statement': bank_statement_parser,
    'your_parser': your_parser,  # Add here
}
```

3. Add tests in `tests/test_parsers.py`

4. Update README.md with usage example

## Testing

- Write tests for new features
- Maintain or improve code coverage
- Test with sample PDFs
- Verify examples still work

## Documentation

Update documentation when you:
- Add new features
- Change existing behavior
- Add new parsers
- Modify the API

## Community

- Be respectful and constructive
- Help others in issues and discussions
- Share your use cases and improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or reach out to the maintainers!
