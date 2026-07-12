"""
Task 2: Folder Watcher
======================
Monitors a folder in real-time and automatically backs up any new file
that appears inside it.

Dependencies:
    pip install watchdog

Usage:
    python watcher.py
    (Drop files into ./watch_folder while the script is running)
"""

import os
import shutil
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ---------------------------------------------------------------------------
# Configuration — change these paths if needed
# ---------------------------------------------------------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
WATCH_FOLDER  = os.path.join(BASE_DIR, "watch_folder")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backup_folder")

# Seconds to wait after a creation event before copying
# (ensures the file is fully written before we touch it)
COPY_DELAY = 1.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def resolve_unique_path(target: Path) -> Path:
    """Return a non-conflicting path by appending a counter if needed."""
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    counter = 1
    while True:
        candidate = target.parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def log(message: str) -> None:
    """Print a timestamped log line."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}]  {message}")


# ---------------------------------------------------------------------------
# Event Handler
# ---------------------------------------------------------------------------
class BackupHandler(FileSystemEventHandler):
    """Copies every newly created file to the backup folder."""

    def on_created(self, event):
        if event.is_directory:
            return  # Ignore folder creation events

        src = Path(event.src_path)

        # Wait briefly to allow the OS to finish writing the file
        time.sleep(COPY_DELAY)

        # Skip if the file was already removed by the time we process it
        if not src.exists():
            log(f"[SKIP] File no longer accessible: {src.name}")
            return

        dst = resolve_unique_path(Path(BACKUP_FOLDER) / src.name)

        try:
            shutil.copy2(str(src), str(dst))
            log(f"[BACKED UP]  {src.name}  →  {dst.name}")
        except OSError as exc:
            log(f"[ERROR] Could not back up {src.name}: {exc}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def start_watcher():
    # Ensure both folders exist
    os.makedirs(WATCH_FOLDER,  exist_ok=True)
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    print("=" * 60)
    print("  Folder Watcher — started")
    print(f"  Watching : {WATCH_FOLDER}")
    print(f"  Backup to: {BACKUP_FOLDER}")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)

    handler  = BackupHandler()
    observer = Observer()
    observer.schedule(handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[STOPPED] Watcher shut down cleanly.")

    observer.join()


if __name__ == "__main__":
    start_watcher()
