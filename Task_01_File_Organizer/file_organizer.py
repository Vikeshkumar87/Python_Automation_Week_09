"""
Task 1: File Organizer
======================
Automatically sorts files in a directory into subfolders based on file type.

Usage:
    python file_organizer.py
    (Prompts for a directory path; press Enter to use ./test_files)
"""

import os
import shutil # shutil is used for moving files
from pathlib import Path # Path is used for convenient path manipulations

# ---------------------------------------------------------------------------
# Category → Extension Mapping
# ---------------------------------------------------------------------------
FILE_CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                  ".webp", ".tiff", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".ppt",
                  ".pptx", ".rtf"],
    "Data":      [".csv", ".json", ".xml", ".sql", ".db", ".xlsx",
                  ".xls"],
    "Videos":    [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
                  ".webm"],
    "Audio":     [".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma"],
    "Archives":  [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code":      [".py", ".js", ".ts", ".html", ".css", ".java",
                  ".cpp", ".c", ".h", ".cs", ".go", ".rb", ".php"],
    "Others":    [],   # Catch-all — populated at runtime
}

# get_category function is used to determine the category of a file based on its extension.
def get_category(extension: str) -> str:
    """Return the category name for a given file extension."""
    ext = extension.lower()
    # Check each category's extensions to find a match.
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

# resolve_unique_path function is used to avoid overwriting files by appending a counter to the filename if a file with the same name already exists in the target directory.
def resolve_unique_path(target: Path) -> Path:
    """Append a counter to avoid overwriting an existing file."""
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix 
    # Extract the filename without extension and the extension itself
    counter = 1
    # Loop until we find a unique filename by appending a counter.
    while True:
        candidate = target.parent / f"{stem}_{counter}{suffix}" # Create a new candidate filename with the counter appended
        
        if not candidate.exists():
            return candidate
        counter += 1


def organize_files(directory: str) -> None:
    """Scan *directory* and move each file into a category subfolder."""
    source = Path(directory)

    if not source.exists():
        print(f"[ERROR] Directory not found: {source}")
        return

    if not source.is_dir():
        print(f"[ERROR] Path is not a directory: {source}")
        return

    moved   = 0
    skipped = 0

    print(f"\nOrganizing: {source.resolve()}")
    print("-" * 60)

    for item in list(source.iterdir()):
        # Skip subdirectories (don't recurse into them)
        if item.is_dir():
            skipped += 1
            continue

        category     = get_category(item.suffix)
        target_dir   = source / category
        target_dir.mkdir(exist_ok=True)

        target_path  = resolve_unique_path(target_dir / item.name)
        shutil.move(str(item), str(target_path))

        print(f"  [MOVED] {item.name:<35} →  {category}/")
        moved += 1

    print("-" * 60)
    print(f"  Done!  Moved: {moved} file(s) | Skipped (folders): {skipped}\n")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    default_dir = os.path.join(os.path.dirname(__file__), "test_files")
    user_input  = input(
        "Enter the directory path to organize\n"
        f"(press Enter to use default: {default_dir})\n> "
    ).strip()

    target = user_input if user_input else default_dir
    organize_files(target)
