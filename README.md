# linkslibrary skill

A personal link archiving skill for OpenClaw. Triggered automatically whenever a URL appears in a message, it fetches the page title, categorizes the link, and appends it to a local markdown library.

## Library file

```
<workspace>/linkslibrary/linkslibrary.md
```

Created automatically on first use. Never overwritten if it already exists.

## Library format

```markdown
## Development
* 2026-04-10 14:33 - [React Native Expo Documentation](https://docs.expo.dev/)

## Fun Stuff

## Homelab
* 2026-04-26 16:31 - [I over-engineered my home lab on purpose, and it's the best decision I've made](https://www.xda-developers.com/...)

## IA

## Second Brain

## Unknown
* 2026-04-10 14:33 - [Duck Duck Go](https://duckduckgo.com)
```

- **Categories** → `## ` H2 headers, always alpha-sorted
- **Entries** → bullet points with timestamp + markdown link, time-sorted (newest at bottom)
- **Timestamps** → local time (Europe/Madrid), 24h format `YYYY-MM-DD HH:MM`
- **Title** → fetched from the page; omitted if unavailable

## Default categories

Development, Fun Stuff, Homelab, IA, Second Brain, Unknown

New categories are created automatically when you specify one that doesn't exist yet. `Unknown` is always present as a fallback.

## How to use

Just send a URL — no command needed:

```
https://example.com
```

Optionally hint the category in the same message:

```
homelab: https://example.com
```

Multiple URLs in one message are all processed and confirmed in a single reply.

## Confirmation format

```
✅ Saved [Title](url) → **Category**
```

One line per URL. Duplicate URLs are noted with ⚠️ and skipped.

## Rules

- **Never modifies existing entries** — append-only
- **One entry per URL** — duplicates are detected and skipped
- **No questions asked** — best-effort categorization, review `Unknown` later

## Files

```
skills/linkslibrary/
├── SKILL.md           ← skill definition + workflow instructions
├── README.md          ← this file
└── scripts/
    └── add_link.py    ← handles file I/O (create, parse, append, deduplicate)
```

### add_link.py usage

```bash
python3 scripts/add_link.py \
  --url "https://example.com" \
  --title "Page Title"        \   # optional
  --category "Homelab"        \   # optional, default: Unknown
  --timestamp "2026-04-26 16:31"  # optional, default: now
  --file "/path/to/linkslibrary.md"
```

Output: `OK:<category>` or `SKIP:duplicate`
