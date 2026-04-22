---
name: linkslibrary
description: Automatically categorize and save links from user messages into a markdown library. Use when a user posts a message containing a URL/link. The skill extracts URLs from the message, fetches page titles, and classifies them into categories from workspace/linkslibrary/links.md (## headings). Links are appended to their category section with timestamp in this exact format - YYYY-MM-DD HH:MM — URL - Page Title - with unclassifiable links going to the ## Unknown section.
metadata: { "openclaw": { "always": true } }
---

# Link Library

Automatically categorize and save links from messages into a curated markdown library.

## Workflow

When a user posts a message containing URL(s), this skill triggers to:

1. **Extract URLs** from the message
2. **Fetch page titles** for each URL
3. **Parse categories** from `workspace/linkslibrary/links.md` (all ## headings)
4. **Classify** each URL+title into the best matching category
5. **Append** to `links.md` in the correct section with timestamp

## Category Matching Logic

Categories are matched by simple keyword matching:
- Convert category name to lowercase
- Check if it appears in the URL (domain/path) or page title
- If no match, or matches multiple, default to `## Unknown`

Examples:
- `## Development` matches `https://docs.python.org/library/...` or "Python Development Guide"
- `## Homelab` matches `https://unraid.com/` or "Home Server Setup"
- `## Fun Stuff` matches `https://kottke.org` or "Interesting Links"

## Execution

Use the categorization script for each URL found in the user's message:

```bash
python3 scripts/categorize_link.py <url> [links.md_path]
```

Default `links.md_path` is `workspace/linkslibrary/links.md`.

The script handles:
- Duplicate detection: skips URLs already saved in links.md
- Fetching page titles (with proper User-Agent)
- Creating the links.md file if it doesn't exist
- Adding the ## Unknown section if missing
- Appending entries to the correct category section
- Outputting JSON result with classification details

## Required Dependencies

The script requires:
- `beautifulsoup4` - HTML parsing for title extraction
- `requests` - HTTP client for fetching pages

Install with:
```bash
pip install beautifulsoup4 requests
```

## Output Format

Each link entry is saved as:
```- YYYY-MM-DD HH:MM — URL - Page Title```

Example:
```- 2026-04-21 22:45 — https://docs.expo.dev/ - React Native Expo Documentation```

## Error Handling

If title fetching fails (timeout, network error, invalid URL), the URL itself is used as the title. The script continues processing other URLs and reports errors to stderr.