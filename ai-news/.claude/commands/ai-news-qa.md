---
description: Fact-check a LinkedIn draft against its cited sources and strip AI-writing artifacts (em dashes, rhetorical triplets, etc.)
---

Use the Agent tool with `subagent_type: "ai-news-qa"` to QA a LinkedIn draft.

Target draft (file path, or paste of raw text + source link), if given by the user: $ARGUMENTS

If empty, tell the agent to use the most recently modified file in `linkedin-drafts/`.

Relay the agent's report back to the user in full: corrections made, artifacts removed, any unresolved flags, and the final cleaned text.
