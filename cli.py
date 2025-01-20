#!/usr/bin/env python3
"""
Source Works PDF Merger Command Line Interface Entry Point

This module serves as the primary entry point for the Source Works PDF merger tool
when installed as a command-line application. It provides a thin wrapper around
the main application logic defined in sw_core.main.

The module follows the common Python pattern of providing a simple CLI entry point
that delegates to the actual implementation. This separation allows the core
functionality to be imported and used programmatically while still providing
a convenient command-line interface.

Usage:
    $ python cli.py merge -dir /path/to/pdfs
    $ python cli.py merge -dir /path/to/pdfs -n output.pdf

Installation:
    When the package is installed via pip, this script becomes available as
    a command-line tool. The shebang line ensures it can be executed directly
    on Unix-like systems.

Implementation Notes:
    - Uses the standard Python idiom for script execution
    - Delegates all functionality to sw_core.main
    - Maintains clean separation between CLI entry point and core logic
"""

from sw_core.main import main

# Standard Python idiom to ensure the script only runs when executed directly
if __name__ == "__main__":
    main()
