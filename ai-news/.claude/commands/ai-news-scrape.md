---
description: Scrape the configured AI-news RSS feeds and (re)build this week's weekly-ai-news-summary.md
---

Use the Agent tool with `subagent_type: "ai-news-scraper"` to refresh the weekly AI news digest at `C:\Users\Josh\code\weekly-ai-news-summary.md`.

Pass it this task: "Rebuild weekly-ai-news-summary.md for the current week following your standard process."

Extra instructions from the user, if any: $ARGUMENTS

After the agent finishes, relay its summary to the user (item counts per section, date range, any exclusions) — do not paste the whole file into chat.
