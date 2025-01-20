# Source Works

[![Unit Tests](https://github.com/wahidyankf/source-works/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/wahidyankf/source-works/actions/workflows/test.yml)

A Python-based tool for merging PDF files with automatic table of contents generation. Designed to help researchers and students organize their research papers and documents.

## Features

- Merge multiple PDF files into a single document
- Automatically generate a table of contents
- Create a title page with customizable metadata
- Handle special characters in filenames
- Preserve original PDF content and formatting
- Support for long filenames with proper wrapping
- Automatic page numbering

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Poetry (Python package manager)
- Node.js 20 or higher (for development tools)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/wahidyankf/source-works.git
   cd source-works
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
