#!/usr/bin/env python3
"""Add a link entry to linkslibrary.md.

Usage:
    add_link.py --url URL [--title TITLE] [--category CATEGORY]
                [--timestamp TS] --file FILE

Output (stdout):
    OK:<category>     - link added successfully
    SKIP:duplicate    - URL already exists in the library
"""
import argparse
from datetime import datetime
from pathlib import Path

DEFAULT_CATEGORIES = ["Development", "Fun Stuff", "Homelab", "IA", "Second Brain", "Unknown"]


def parse_library(text: str) -> dict:
    """Parse markdown into {category: [entry_lines]} preserving discovery order."""
    cats: dict = {}
    current = None
    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith("## "):
            current = stripped[3:].strip()
            if current not in cats:
                cats[current] = []
        elif current is not None and stripped.startswith("* "):
            cats[current].append(stripped)
    return cats


def render_library(cats: dict) -> str:
    """Render categories (alpha-sorted) back to markdown."""
    lines = []
    for cat in sorted(cats.keys()):
        lines.append(f"## {cat}")
        for entry in cats[cat]:
            lines.append(entry)
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def init_library() -> str:
    """Generate a default empty library with standard categories."""
    lines = []
    for cat in sorted(DEFAULT_CATEGORIES):
        lines.append(f"## {cat}")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Add a link to linkslibrary.md")
    ap.add_argument("--url", required=True, help="URL to add")
    ap.add_argument("--title", default="", help="Page title (optional)")
    ap.add_argument("--category", default="Unknown", help="Target category")
    ap.add_argument("--timestamp", default="", help="Timestamp YYYY-MM-DD HH:MM (default: now)")
    ap.add_argument("--file", required=True, help="Path to linkslibrary.md")
    args = ap.parse_args()

    fpath = Path(args.file)
    fpath.parent.mkdir(parents=True, exist_ok=True)

    # Read existing file or create fresh one
    if fpath.exists():
        text = fpath.read_text(encoding="utf-8")
    else:
        text = init_library()

    cats = parse_library(text)

    # Ensure "Unknown" always exists
    if "Unknown" not in cats:
        cats["Unknown"] = []

    # Deduplication: skip if URL already present in any entry
    all_entries = "\n".join(e for entries in cats.values() for e in entries)
    if args.url in all_entries:
        print("SKIP:duplicate")
        return

    # Resolve category: case-insensitive match against existing categories
    cat = args.category.strip() or "Unknown"
    existing_map = {c.lower(): c for c in cats}
    cat = existing_map.get(cat.lower(), cat)
    if cat not in cats:
        cats[cat] = []

    # Timestamp: provided or current local time
    ts = args.timestamp.strip() or datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build entry line (entries are time-sorted; newest appended at bottom)
    title = args.title.strip()
    if title:
        entry = f"* {ts} - [{title}]({args.url})"
    else:
        entry = f"* {ts} - {args.url}"

    cats[cat].append(entry)
    fpath.write_text(render_library(cats), encoding="utf-8")
    print(f"OK:{cat}")


if __name__ == "__main__":
    main()
