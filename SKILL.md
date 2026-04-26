---
name: linkslibrary
description: Archive and categorize web links sent by the user. Triggers whenever a message contains one or more URLs (http:// or https:// links). Saves links to the personal links library with a timestamp, optional fetched title, and category. Use this skill any time the user sends a URL or a message that includes one or more web links — even when no explicit archiving request is made.
---

# Links Library

## Library File

`<workspace>/linkslibrary/linkslibrary.md`

Resolve `<workspace>` from runtime context (`repo=...`). Currently: `~/.openclaw/workspace/linkslibrary/linkslibrary.md`

## Workflow

For each URL detected in the message, execute these steps in order. Process all URLs before replying.

### 1. Fetch the page title

Use `web_fetch` on the URL. Extract the page `<title>` or the first H1 from the rendered content. If the fetch fails or no title is found, proceed with an empty title — do **not** skip the URL.

### 2. Read existing categories

Parse the `## ` headers from `linkslibrary.md` (skip this read if the file does not exist yet — the script will create it with defaults).

### 3. Determine category

- If the user provided a category in their message, use it (even if it's new).
- Otherwise, use your judgment to match the URL + title against the existing categories. Choose the best fit. If no category clearly fits, use `Unknown`.

### 4. Add the link

Run the script with the resolved arguments:

```bash
python3 <skill_dir>/scripts/add_link.py \
  --url "<URL>" \
  --title "<title or empty>" \
  --category "<category>" \
  --file "<workspace>/linkslibrary/linkslibrary.md"
```

`<skill_dir>` is the directory containing this SKILL.md.

Script output:
- `OK:<category>` — link was added, category shows where it was stored (may differ from input if case-normalized).
- `SKIP:duplicate` — URL already in the library; skip silently or note it in the reply.

### 5. Reply

After processing all URLs, send a **single** confirmation reply in the **same channel** where the message arrived.

Format:
```
✅ Saved [Title](url) → **Category**
✅ Saved [Another Title](url2) → **Category2**
```

- Start every line with `✅`
- One line per URL
- If the title is empty, use just the URL as the link text
- If a URL was a duplicate, include it as: `⚠️ Already saved: <url>`
- Keep the message to one line per link — no extra explanation needed

## Rules

- **Never modify existing entries.** Only append.
- **One entry per URL.** The script handles deduplication.
- **Create the file if absent.** The script initializes it with default categories.
- **Multiple URLs in one message** → process each separately, confirm all in one reply.
- **Do not ask questions.** Make a best-effort categorization and confirm.
- **Local time** is used for timestamps (system clock, Europe/Madrid). The script applies this automatically.
