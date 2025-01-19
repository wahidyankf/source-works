# Research Assistant

A Python-based tool for merging PDF files with automatic table of contents generation. Designed to help researchers and students organize their research papers and documents.

## Features

- **Automatic Table of Contents**: Generates a clean, professional table of contents with page numbers
- **Title Pages**: Creates title pages for each document with customizable formatting
- **PDF Bookmarks**: Adds navigable bookmarks for easy document traversal
- **Clean Formatting**: Consistent and modern document styling
- **Smart File Handling**:
  - Handles duplicate filenames
  - Preserves original document content
  - Skips non-PDF files automatically
  - Supports special characters in filenames

## Installation

1. Clone the repository:

```bash
git clone https://github.com/wahidyankf/source-works.git
cd source-works
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Usage

The tool can be used via command line:

```bash
# Merge all PDFs in the current directory
poetry run python cli.py merge ./path/to/pdfs output.pdf

# Get help
poetry run python cli.py --help
```

## Development

### Prerequisites

- Python 3.12+
- Poetry for dependency management

### Dependencies

#### Main Dependencies

- PyPDF (^4.0.1) for PDF manipulation
- reportlab (^4.0.8) for PDF generation

#### Development Dependencies

- pytest (^8.0.0) for testing
- black (^24.1.0) for code formatting
- isort (^5.13.2) for import sorting
- mypy (^1.8.0) for type checking
- pytest-watch (^4.2.0) for test watching

### Project Structure

```
source-works/
├── ra_core/           # Core functionality
│   ├── __init__.py
│   └── main.py       # Main PDF merging logic
├── tests/            # Test suite
│   └── test_pdf_merger.py
├── cli.py           # Command line interface
├── create_test_pdfs.py  # Utility for creating test PDFs
├── pyproject.toml   # Project configuration
└── README.md        # Documentation
```

### Testing

The project includes a comprehensive test suite covering:

- Basic functionality
- Edge cases
- Error handling
- File content preservation
- File naming
- Directory cleanup

Run tests with:

```bash
poetry run pytest tests/ -v
```

For continuous test running during development:

```bash
poetry run ptw
```

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy .
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for any new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
