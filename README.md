# Source Works

A Python-based tool for merging PDF files with automatic table of contents generation. Designed to help researchers and students organize their research papers and documents.

## Features

- **Automatic Table of Contents**:
  - Professional layout with page numbers
  - Intelligent text wrapping for long titles
  - Consistent formatting and spacing
  - Dot leaders for visual clarity
- **Title Pages**:
  - Dynamically sized text based on content
  - Centered layout with proper margins
  - Professional typography
- **PDF Processing**:
  - Page numbering throughout document
  - Navigable bookmarks
  - Original content preservation
  - Robust error handling
- **Smart File Handling**:
  - Duplicate filename detection
  - Special character support
  - Non-PDF file filtering
  - Temporary file cleanup

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
# Basic usage - merge all PDFs in a directory
poetry run python cli.py merge -dir /path/to/pdfs

# Specify custom output filename
poetry run python cli.py merge -dir /path/to/pdfs -n output.pdf

# Get help
poetry run python cli.py --help
```

## Development

### Prerequisites

- Python 3.12+
- Poetry for dependency management
- Node.js (for development tools)

### Project Structure

```
source-works/
├── sw_core/                # Core functionality
│   ├── domains/           # Domain-specific modules
│   │   ├── pdf.py        # PDF processing logic
│   │   └── files.py      # File handling utilities
│   └── main.py           # Main application logic
├── tests/                 # Test suite
│   └── test_pdf_merger.py
├── cli.py                # Command line interface
├── pyproject.toml        # Project configuration
├── pyrightconfig.json    # Type checking configuration
└── README.md            # Documentation
```

### Dependencies

#### Main Dependencies

- PyPDF (^4.0.1): PDF manipulation
- reportlab (^4.0.8): PDF generation and styling

#### Development Dependencies

- pytest (^8.0.0): Testing framework
- black (^24.1.0): Code formatting
- isort (^5.13.2): Import sorting
- mypy (^1.8.0): Static type checking
- pytest-watch (^4.2.0): Continuous testing

### Testing

Run the comprehensive test suite:

```bash
# Run all tests
poetry run pytest tests/ -v

# Watch mode for development
poetry run ptw
```

The test suite covers:

- Core PDF merging functionality
- Table of contents generation
- Title page creation
- File handling edge cases
- Error scenarios
- Memory management
- File cleanup

### Code Quality

Maintain code quality with provided tools:

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy .
```

Type checking features:

- Strict mode enabled
- No implicit any types
- Complete function signatures
- Comprehensive type hints
- Third-party library type safety

### Git Hooks

Pre-configured Git hooks using Husky:

- **Pre-push**: Runs test suite
- **Pre-commit**: Runs code formatting

### Continuous Integration

The project uses GitHub Actions for continuous integration:

- **Automated Testing**:
  - Runs on every push to main branch
  - Runs on every pull request
  - Tests both Python and Node.js code
  - Uploads test results as artifacts

- **Environment**:
  - Python 3.12 with Poetry
  - Node.js 20.x with Yarn
  - Ubuntu latest runner

- **Test Artifacts**:
  - Test results
  - Coverage reports
  - Available for 7 days

View the workflow status and test results in the [Actions tab](../../actions) of the repository.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
