from pathlib import Path
import os


def get_unique_filename(directory: Path, base_name: str) -> str:
    """Generate a unique filename in the given directory."""
    if not os.path.exists(directory / base_name):
        return base_name

    base, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(directory / f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"
