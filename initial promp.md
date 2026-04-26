The ideas is to have a skill that collects and categorise links that I send to the assistant (you).
Links should be archived into an md file named linkslibrary.md stored in `linkslibrary/linkslibrary.md`

linkslibrary.md should have a similar structure:

```markdown
## Development 
* 2026-04-10 14:33 - [React Native Expo Documentation](https://docs.expo.dev/)

## Fun Stuff

## Homelab

## IA

## Second Brain

## Unknown
* 2026-04-10 14:33 — [Duck Duck Go](https://duckduckgo.com)
```

In which
* categories are the H2 headers
* entries are bullet points composed by timestamp and a standard markdown link. The title is optional, it could be missing.
* timestamps are 24h based local time
* categories should be alpha-sorted
* links should be time sorted: the latest at the bottom of the category

When a link is received in the chat or telegram, these actions should be performed:
* Read the categories currently available in linkslibrary.md
* Retrieve the link's title - i.e. by downloading the page. If the title cannot be found, just omit it.
* Optionally I can provide the category in the same message as the link, in that case use the category I suggest, i it doesn't exist, ad it to linkslibrary.md - categories are always alpha-sorted
* If I don't provide a category, match the link+title against one of the existing category, if you cannot find a suitable category add it to the "Unknown" category, I'll revise it later.
* Confirm with a confirmation one-line message that the link has been added to linkslibrary.md, including the link with its title and what category has been used. Start the message with a `✅` to make it more visible
* Send this message in the same channel in which I posted the link- chat or telegram or other channel
* Do not ask additional questions.

The skill should:
* Be always active, even after a new session or a restart
* Triggered whenever I post a link to a web resource
* Create linkslibrary.md if it doesn't exist yet, never override an existing linkslibrary.md
* NEVER modify existing entries.
* One entry per URL. If the message contains multiple URLs, process each one and confirm all of them in a single reply.
