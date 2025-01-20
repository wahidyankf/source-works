# Sourcerer

[![Unit Tests](https://github.com/wahidyankf/sourcerer/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/wahidyankf/sourcerer/actions/workflows/test.yml)

A Python-based tool for merging PDF files with automatic table of contents generation. Designed to help researchers and students organize their research papers and documents.

## Features

- Merge multiple PDF files into a single document
- Automatically generate a table of contents
- Create a title page with customizable metadata
- Handle special characters in filenames
- Preserve original PDF content and formatting
- Support for long filenames with proper wrapping
- Automatic page numbering

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wahidyankf/sourcerer.git
   cd sourcerer
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

You can use Sourcerer through Poetry to merge PDF files:

### Basic Usage

```bash
# Merge PDFs in a directory with default output name (merged_pdfs.pdf)
poetry run python cli.py --merge-pdf -dir /path/to/pdfs

# Merge PDFs with a custom output filename
poetry run python cli.py --merge-pdf -dir /path/to/pdfs -n custom_output.pdf
```

### Command Line Options

- `--merge-pdf`: Activate PDF merging functionality
- `-dir, --directory`: Path to directory containing PDF files to merge
- `-n, --name`: Optional output filename (default: merged_pdfs.pdf)

### Example

1. Place your PDF files in a directory:
   ```
   research_papers/
   ├── paper1.pdf
   ├── paper2.pdf
   └── paper3.pdf
   ```

2. Run Sourcerer:
   ```bash
   poetry run python cli.py --merge-pdf -dir ./research_papers -n research_collection.pdf
   ```

3. The output will be a single PDF file (`research_collection.pdf`) containing:
   - A title page
   - A table of contents with page numbers
   - All your PDFs merged in sequence with preserved formatting

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Poetry (Python package manager)
- Node.js 20 or higher (for development tools)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/wahidyankf/sourcerer.git
   cd sourcerer
   ```

2. Install dependencies:
   ```bash
   npm install    # Install development tools
   npm run install    # Install Python dependencies via Poetry
   ```

### Development Commands

- `npm run format` - Format code using Black and isort
- `npm test` - Run tests and type checking
- `npm run watch` - Watch for changes and run tests automatically

### Testing

The project uses pytest for testing. Run the test suite with:

```bash
npm test
```

Tests cover various aspects including:

- PDF merging functionality
- Table of contents generation
- Title page creation
- Special character handling
- File naming and path management

## Continuous Integration

The project uses GitHub Actions for continuous integration, which:

- Runs on Ubuntu latest
- Tests with Python 3.12
- Checks code formatting
- Runs the test suite
- Provides test results as artifacts

## License

[MIT License](LICENSE)

## Author

Wahidyan Kresna Fridayoka <wahidyankf@gmail.com>
