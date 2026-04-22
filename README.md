# Link Library Skill

Automatically categorize and save links from user messages into a curated markdown library.

## What It Does

When you post a message containing URLs, this skill automatically:

1. **Extracts URLs** from your message
2. **Fetches page titles** for each URL
3. **Classifies** them into categories based on your `links.md` file
4. **Appends** entries to the correct category section with timestamps

Links that can't be categorized go into the `## Unknown` section.

## Installation

### OpenClaw Workspace

Copy the skill folder to your workspace:

```bash
# Workspace skills (per-agent)
cp -r linkslibrary ~/.openclaw/workspace/skills/public/

# Or shared skills (all agents on the machine)
cp -r linkslibrary ~/.openclaw/skills/
```

The skill will be available in the next session.

### Dependencies

Install the required Python packages:

```bash
pip install beautifulsoup4 requests
```

## Usage

### Automatic (Recommended)

The skill loads automatically for each session. When you post a message containing URLs, the agent will automatically categorize and save them.

### Manual

You can also invoke the categorization script directly:

```bash
python3 scripts/categorize_link.py <url> [links.md_path]
```

Default `links.md_path` is `workspace/linkslibrary/links.md`.

## Configuration

### Link Library File

Create or edit `workspace/linkslibrary/links.md` and add your categories as markdown headings:

```markdown
## Development
## Homelab
## AI
## Second Brain
## Unknown
```

The `## Unknown` section is required for links that don't match any category.

### Category Matching

Categories are matched by keyword search:
- Category name (lowercased) must appear in the **URL** (domain/path) or **page title**
- If no match, the link goes to `## Unknown`

**Examples:**

| Category | Matches |
|----------|---------|
| `## Development` | `https://docs.python.org/library/...`, "Python Development Guide" |
| `## Homelab` | `https://unraid.com/`, "Home Server Setup" |
| `## AI` | `https://openai.com/`, "Language Models" |

## Output Format

Each link entry is saved as:

```markdown
- YYYY-MM-DD HH:MM — URL - Page Title
```

**Example:**

```markdown
## AI
- 2026-04-21 23:32 — https://www.lennysproductpass.com - Lenny's Product Pass
- 2026-04-21 23:31 — https://github.com/karpathy/llm-wiki - llm-wiki · GitHub
```

## Features

- **Duplicate detection**: Skips URLs already saved in `links.md`
- **Auto-creation**: Creates `links.md` and `## Unknown` section if missing
- **Error handling**: Continues processing if individual links fail
- **User-Agent**: Proper HTTP headers for page fetching

## Error Handling

If title fetching fails (timeout, network error, invalid URL):
- The URL itself is used as the title
- Error is reported to stderr
- Processing continues for other URLs

## Skill Metadata

```yaml
name: linkslibrary
always: true  # Loads for every session
```

The skill automatically loads for each OpenClaw session and will be invoked when URLs are detected in messages.

## Example Workflow

1. **Create categories** in `workspace/linkslibrary/links.md`:

```markdown
## AI
## Development
## Unknown
```

2. **Post a message** with URLs:

> Check out these resources:
> https://docs.openai.com/
> https://github.com/openai/openai-python

3. **Result** in `links.md`:

```markdown
## AI
- 2026-04-22 14:45 — https://docs.openai.com/ - OpenAI Documentation
- 2026-04-22 14:45 — https://github.com/openai/openai-python - openai/openai-python: OpenAI Python library

## Unknown
```

## License

MIT License - feel free to use, modify, and distribute.

## Contributing

Pull requests welcome! Enhancements ideas:
- Better category matching (semantic similarity)
- Automatic category suggestions
- Export to JSON/CSV
- Web UI for browsing links

---

Built for [OpenClaw](https://github.com/openclaw/openclaw).