"""
Task 5: System Monitor
======================
Logs CPU, RAM, and Disk usage at a configurable interval to a persistent
log file and the console.

Dependencies:
    pip install psutil

Usage:
    python system_monitor.py              # logs every 60 seconds (default)
    python system_monitor.py 10           # logs every 10 seconds
"""

import os
import sys
import time
from datetime import datetime

import psutil

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
LOG_DIR     = os.path.join(BASE_DIR, "logs")
LOG_FILE    = os.path.join(LOG_DIR, "system_monitor.log")
DEFAULT_INTERVAL = 60   # seconds

# Cross-platform root disk path
DISK_PATH = "C:\\" if sys.platform.startswith("win") else "/"


# ---------------------------------------------------------------------------
# Metric Collection
# ---------------------------------------------------------------------------
def collect_metrics() -> dict:
    """Read current CPU, RAM, and Disk statistics via psutil."""
    # cpu_percent(interval=1) blocks for 1 second to measure accurately
    cpu   = psutil.cpu_percent(interval=1)
    mem   = psutil.virtual_memory()
    disk  = psutil.disk_usage(DISK_PATH)

    return {
        "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_pct":        cpu,
        "ram_used_gb":    round(mem.used  / (1024 ** 3), 2),
        "ram_total_gb":   round(mem.total / (1024 ** 3), 2),
        "ram_pct":        mem.percent,
        "disk_used_gb":   round(disk.used  / (1024 ** 3), 2),
        "disk_total_gb":  round(disk.total / (1024 ** 3), 2),
        "disk_pct":       disk.percent,
    }


# ---------------------------------------------------------------------------
# Log Entry Formatting
# ---------------------------------------------------------------------------
def format_entry(m: dict) -> str:
    """Return a single formatted log line from a metrics dict."""
    return (
        f"[{m['timestamp']}]  "
        f"CPU: {m['cpu_pct']:5.1f}%  |  "
        f"RAM: {m['ram_used_gb']:.2f}GB / {m['ram_total_gb']:.2f}GB "
        f"({m['ram_pct']:.1f}%)  |  "
        f"Disk: {m['disk_used_gb']:.2f}GB / {m['disk_total_gb']:.2f}GB "
        f"({m['disk_pct']:.1f}%)"
    )


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------
def run_monitor(interval: int) -> None:
    """Collect and log metrics every *interval* seconds until Ctrl+C."""
    os.makedirs(LOG_DIR, exist_ok=True)

    print("=" * 70)
    print("  System Monitor — started")
    print(f"  Interval : every {interval} second(s)")
    print(f"  Log file : {LOG_FILE}")
    print("  Press Ctrl+C to stop.")
    print("=" * 70 + "\n")

    session_count = 0

    try:
        while True:
            metrics = collect_metrics()
            entry   = format_entry(metrics)

            # Append to log file
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry + "\n")

            # Print to console
            print(entry)
            session_count += 1

            # Wait for the next cycle
            # (cpu_percent already waited 1 s, so subtract that)
            remaining = max(0, interval - 1)
            time.sleep(remaining)

    except KeyboardInterrupt:
        print(f"\n[STOPPED]  Session entries logged: {session_count}")
        print(f"           Log file: {LOG_FILE}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INTERVAL
        if interval < 1:
            raise ValueError
    except ValueError:
        print(f"[ERROR] Interval must be a positive integer (seconds). "
              f"Using default: {DEFAULT_INTERVAL}s.")
        interval = DEFAULT_INTERVAL

    run_monitor(interval)
