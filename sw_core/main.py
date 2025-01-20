#!/usr/bin/env python3

import argparse
from pathlib import Path

from sw_core import pdf


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF Merger Tool")
    parser.add_argument("--merge-pdf", action="store_true",
                        help="Merge PDF files")
    parser.add_argument(
        "-dir", "--directory", type=str, help="Directory containing PDF files"
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="merged_pdfs.pdf",
        help="Output filename (default: merged_pdfs.pdf)",
    )

    args = parser.parse_args()

    if args.merge_pdf:
        if not args.directory:
            print("Error: Please specify a directory using -dir or --directory")
            return

        # Convert directory to absolute path if it's relative
        directory = Path(args.directory).resolve()

        if not directory.exists():
            print(f"Error: Directory does not exist: {directory}")
            return

        if not directory.is_dir():
            print(f"Error: Not a directory: {directory}")
            return

        pdf.merge_pdfs(directory, args.name)


if __name__ == "__main__":
    main()
