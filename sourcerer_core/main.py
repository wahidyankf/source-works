#!/usr/bin/env python3
"""
Source Works PDF Merger Command Line Interface

This module serves as the main entry point for the Source Works PDF merger tool.
It provides a command-line interface for merging multiple PDF files into a single
document with automatic table of contents generation.

The module uses argparse to handle command-line arguments and provides a user-friendly
interface for specifying input directory and output filename options.

Example Usage:
    # Merge PDFs in a directory with default output name
    python -m sw_core merge -dir /path/to/pdfs

    # Merge PDFs with custom output name
    python -m sw_core merge -dir /path/to/pdfs -n custom_output.pdf

Command Line Arguments:
    --merge-pdf: Flag to activate PDF merging functionality
    -dir, --directory: Path to directory containing PDF files to merge
    -n, --name: Optional output filename (default: merged_pdfs.pdf)

Implementation Notes:
    - Uses pathlib.Path for robust cross-platform path handling
    - Converts relative paths to absolute paths
    - Performs extensive input validation before processing
    - Delegates actual PDF merging to the domains.pdf module
"""

import argparse
from pathlib import Path

from sourcerer_core import domains


def main() -> None:
    """
    Main entry point for the PDF merger command-line interface.

    This function:
    1. Sets up the argument parser with all available options
    2. Validates the provided arguments
    3. Processes the input directory
    4. Initiates the PDF merging process

    Returns:
        None

    Error Handling:
        - Checks for missing required arguments
        - Validates directory existence and type
        - Provides user-friendly error messages
    """
    # Initialize argument parser with program description
    parser = argparse.ArgumentParser(
        description="Source Works PDF Merger Tool - Merge multiple PDFs with automatic TOC generation"
    )

    # Define command-line arguments
    parser.add_argument(
        "--merge-pdf",
        action="store_true",
        help="Activate PDF merging functionality"
    )
    parser.add_argument(
        "-dir", "--directory",
        type=str,
        help="Directory containing PDF files to merge"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default="merged_pdfs.pdf",
        help="Output filename (default: merged_pdfs.pdf)"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Handle PDF merging command
    if args.merge_pdf:
        # Validate directory argument
        if not args.directory:
            print("Error: Please specify a directory using -dir or --directory")
            return

        # Convert directory path to absolute path
        # This ensures consistent path handling regardless of how the path was specified
        directory = Path(args.directory).resolve()

        # Validate directory existence and type
        if not directory.exists():
            print(f"Error: Directory does not exist: {directory}")
            return

        if not directory.is_dir():
            print(f"Error: Not a directory: {directory}")
            return

        # Initiate PDF merging process
        # The actual merging is delegated to the domains.pdf module
        # which handles all PDF-specific operations
        domains.pdf.merge(directory, args.name)


# Standard Python idiom to ensure main() is only called if this script is run directly
if __name__ == "__main__":
    main()
