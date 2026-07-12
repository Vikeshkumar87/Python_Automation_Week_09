"""
Task 3: Web Scraper
===================
Fetches the latest news headlines from the BBC News RSS feed and saves
them to a text file.

Dependencies:
    pip install requests

Usage:
    python web_scraper.py
"""

import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
RSS_URL     = "https://feeds.bbci.co.uk/news/rss.xml"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headlines.txt")
MAX_ITEMS   = 20
PREVIEW_N   = 5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ---------------------------------------------------------------------------
# Fetch & Parse
# ---------------------------------------------------------------------------
def fetch_rss(url: str) -> ET.Element:
    """Download the RSS feed and return the parsed XML root element."""
    print(f"Connecting to: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out after 15 seconds.")
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        print(f"[ERROR] HTTP error: {exc}")
        sys.exit(1)

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as exc:
        print(f"[ERROR] Failed to parse XML: {exc}")
        sys.exit(1)

    return root


def parse_headlines(root: ET.Element, max_items: int = MAX_ITEMS) -> list:
    """Extract headline data from RSS <item> elements."""
    items = root.findall(".//item")
    headlines = []

    for item in items[:max_items]:
        def text(tag):
            el = item.find(tag)
            return el.text.strip() if el is not None and el.text else "N/A"

        headlines.append({
            "title":       text("title"),
            "link":        text("link"),
            "pubDate":     text("pubDate"),
            "description": text("description"),
        })

    return headlines


# ---------------------------------------------------------------------------
# Save to File
# ---------------------------------------------------------------------------
def save_headlines(headlines: list, output_file: str) -> None:
    """Write formatted headlines to a text file."""
    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("BBC News — Top Headlines\n")
        f.write(f"Fetched on : {fetch_time}\n")
        f.write(f"Source     : {RSS_URL}\n")
        f.write("=" * 70 + "\n\n")

        for i, h in enumerate(headlines, start=1):
            f.write(f"{i:>2}. {h['title']}\n")
            f.write(f"    Date : {h['pubDate']}\n")
            f.write(f"    URL  : {h['link']}\n")
            if h["description"] != "N/A":
                # Wrap long descriptions at 65 chars
                desc = h["description"]
                f.write(f"    Info : {desc[:130]}{'...' if len(desc) > 130 else ''}\n")
            f.write("\n")

    print(f"\nSaved {len(headlines)} headlines → {output_file}")


# ---------------------------------------------------------------------------
# Console Preview
# ---------------------------------------------------------------------------
def print_preview(headlines: list, n: int = PREVIEW_N) -> None:
    print(f"\n--- Top {n} Headlines (Preview) ---")
    for i, h in enumerate(headlines[:n], start=1):
        print(f"  {i}. {h['title']}")
        print(f"     {h['pubDate']}")
    print()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root      = fetch_rss(RSS_URL)
    headlines = parse_headlines(root)

    if not headlines:
        print("[WARNING] No headlines found in the feed.")
        sys.exit(0)

    print(f"Fetched {len(headlines)} headline(s).")
    save_headlines(headlines, OUTPUT_FILE)
    print_preview(headlines)
