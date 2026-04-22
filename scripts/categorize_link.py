#!/usr/bin/env python3
"""Link categorizer for linkslibrary skill.

This script fetches the title of a URL and appends it to the appropriate
category section in linkslibrary/links.md.
"""

import sys
import re
import json
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path


def extract_urls(text):
    """Extract all URLs from a text message."""
    # Pattern matches http://, https://, and www. URLs
    pattern = r'https?://[^\s<>"\'()]+|www\.[^\s<>"\'()]+'
    urls = re.findall(pattern, text)
    # Normalize www. URLs to https://
    normalized = []
    for url in urls:
        if url.startswith('www.'):
            url = 'https://' + url
        normalized.append(url)
    return normalized


def fetch_page_title(url):
    """Fetch the title of a webpage."""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else url
        # Clean up title (remove extra whitespace)
        title = ' '.join(title.split())
        return title
    except Exception as e:
        print(f"Error fetching title from {url}: {e}", file=sys.stderr)
        return url


def parse_categories(links_md_path):
    """Parse links.md and extract category headings."""
    categories = ['Unknown']  # Unknown is always available

    with open(links_md_path, 'r') as f:
        content = f.read()

    # Find all ## headings
    for match in re.finditer(r'^##\s+(.+)$', content, re.MULTILINE):
        category = match.group(1).strip()
        if category != 'Unknown':  # Avoid duplicates
            categories.append(category)

    return categories


def classify_link(url, title, categories):
    """Classify a URL+title into a category.

    Returns the category name, or 'Unknown' if no match.
    """
    # Convert to lowercase for matching
    url_lower = url.lower()
    title_lower = title.lower()

    # Simple heuristic matching: check if category name appears in URL or title
    for category in categories:
        if category == 'Unknown':
            continue
        category_lower = category.lower()

        if category_lower in url_lower or category_lower in title_lower:
            return category

    return 'Unknown'


def append_to_category(links_md_path, url, title, category):
    """Append a link to the appropriate category section."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    link_entry = f"- {timestamp} — {url} - {title}\n"

    with open(links_md_path, 'r') as f:
        content = f.read()

    # Find the section for the category
    section_pattern = rf'^##\s+{re.escape(category)}\s*$'

    if category == 'Unknown' and not re.search(section_pattern, content, re.MULTILINE):
        # Add Unknown section if it doesn't exist
        content += "\n## Unknown\n"

    # Find where to insert: after the category header, before the next ## or EOF
    match = re.search(section_pattern, content, re.MULTILINE)
    if not match:
        # Section doesn't exist, create it at the end
        content += f"\n## {category}\n{link_entry}"
    else:
        # Insert after the ## line and any following empty lines
        insert_pos = match.end()
        lines = content[insert_pos:].split('\n')

        # Skip empty lines after the header
        skip = 0
        for line in lines:
            if line.strip() == '':
                skip += 1
            else:
                break

        new_content = content[:insert_pos + skip]
        # Add separator if the section already has items
        if skip > 0:
            new_content += link_entry
        else:
            new_content += '\n' + link_entry
        new_content += content[insert_pos + skip:]
        content = new_content

    with open(links_md_path, 'w') as f:
        f.write(content)


def url_exists(links_md_path, url):
    """Check if a URL already exists in links.md."""
    with open(links_md_path, 'r') as f:
        content = f.read()

    # Search for the URL in the link entry format
    # Pattern matches: - YYYY-MM-DD HH:MM — URL - Title
    url_pattern = rf'- \d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}} — {re.escape(url)} '

    return bool(re.search(url_pattern, content))


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: categorize_link.py <url> [links.md_path]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    links_md_path = sys.argv[2] if len(sys.argv) > 2 else 'workspace/linkslibrary/links.md'

    # Resolve path
    workspace_root = Path('/home/openclaw/.openclaw/workspace')
    # If path starts with "workspace/", strip it since we're already in workspace
    if links_md_path.startswith('workspace/'):
        links_md_path = links_md_path[10:]  # "workspace/" is 10 characters
    links_md_full = workspace_root / links_md_path

    # Ensure the directory exists
    links_md_full.parent.mkdir(parents=True, exist_ok=True)

    # Create file if it doesn't exist
    if not links_md_full.exists():
        with open(links_md_full, 'w') as f:
            f.write('## Unknown\n')

    # Fetch title
    title = fetch_page_title(url)

    # Parse categories
    categories = parse_categories(links_md_full)

    # Classify
    category = classify_link(url, title, categories)

    # Check for duplicate
    if url_exists(links_md_full, url):
        print(json.dumps({
            'url': url,
            'title': title,
            'category': category,
            'saved': False,
            'reason': 'duplicate'
        }))
        return

    # Append
    append_to_category(links_md_full, url, title, category)

    # Output result as JSON for easy parsing
    print(json.dumps({
        'url': url,
        'title': title,
        'category': category,
        'saved': True
    }))


if __name__ == '__main__':
    main()