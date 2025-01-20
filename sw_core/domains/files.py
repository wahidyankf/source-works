"""
File System Operations Module

This module provides utility functions for handling file system operations,
particularly focused on file naming and path management. It includes functions
for generating unique filenames to avoid conflicts when creating new files.

The module is designed to be used as part of the Source Works PDF merging tool,
but its functionality is generic enough to be used in other contexts where
file system operations are needed.
"""

from pathlib import Path
import os


def get_unique_filename(directory: Path, base_name: str) -> str:
    """
    Generate a unique filename in the given directory by appending a counter if necessary.

    This function ensures that the returned filename does not conflict with any existing
    files in the specified directory. If the base_name is already unique, it is returned
    as is. Otherwise, a counter is appended before the file extension until a unique
    name is found.

    Args:
        directory (Path): The directory path where the file will be created.
                         Must be an existing directory.
        base_name (str): The desired base filename, including extension.
                        Example: "document.pdf"

    Returns:
        str: A unique filename that can be safely used in the specified directory.
             If base_name is already unique, returns base_name unchanged.
             Otherwise, returns a name with a counter inserted.
             Example: "document_1.pdf" if "document.pdf" already exists.

    Example:
        >>> from pathlib import Path
        >>> directory = Path("/path/to/dir")
        >>> get_unique_filename(directory, "report.pdf")
        'report.pdf'  # If the file doesn't exist
        >>> get_unique_filename(directory, "report.pdf")
        'report_1.pdf'  # If report.pdf exists
        >>> get_unique_filename(directory, "report.pdf")
        'report_2.pdf'  # If both report.pdf and report_1.pdf exist

    Implementation Notes:
        - Uses os.path.exists() for file existence checks
        - Splits filename into base and extension using os.path.splitext()
        - Counter starts at 1 and increments until a unique name is found
        - Maintains the original file extension
        - Thread-safe for file existence checks, but race conditions possible
          between check and actual file creation
    """
    # First, check if the original filename is available
    if not os.path.exists(directory / base_name):
        return base_name

    # Split the filename into base and extension
    # Example: "document.pdf" -> ("document", ".pdf")
    base, ext = os.path.splitext(base_name)

    # Keep incrementing counter until we find a unique filename
    counter = 1
    while os.path.exists(directory / f"{base}_{counter}{ext}"):
        counter += 1

    # Return the unique filename with counter inserted before extension
    return f"{base}_{counter}{ext}"
