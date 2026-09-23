---
description: Draft a LinkedIn post/article based on one or more items from weekly-ai-news-summary.md (or a given URL/topic)
---

The user wants a LinkedIn post/article. Their request: $ARGUMENTS

If that's empty, ask them which item(s) from `weekly-ai-news-summary.md` (or which URL/topic) to write about, and what tone/angle they want (default: neutral).

Otherwise, use the Agent tool with `subagent_type: "ai-news-linkedin-writer"` and pass it the user's request verbatim, plus a reminder to read `C:\Users\Josh\code\weekly-ai-news-summary.md` if the request references an item from it.

Relay the agent's draft back to the user in full once it's done.
