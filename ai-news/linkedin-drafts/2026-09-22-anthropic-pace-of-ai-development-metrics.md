---
created: 2026-09-22
sources:
  - https://www.anthropic.com/institute/measuring-pace-of-ai-development
tone: neutral
status: qa-flagged
---

How would you know if AI development inside a frontier lab was accelerating, and whether safety work was keeping pace with capability work? Anthropic's Institute published a proposal <!-- QA: draft states "on September 17" but the source page has no visible dateline or publish date; could not verify this date independently --> for three public-facing metrics meant to answer exactly that, using its own internal data as the first test case. The numbers are worth looking at closely, and so are the limitations Anthropic attaches to each one.

**Metric 1: how much AI R&D is AI-led**

Anthropic built an "R&D Automation Index" that catalogs research tasks and rates automation level from AL0 (no AI involvement) to AL5 (fully autonomous). As of August 2026, Claude "leads" 26% of Anthropic's own AI research work, up from under 1% in February. Leading means Claude can take a high-level prompt and complete most of the task end to end with a human checking the output rather than doing the work. Over 90% of research work is now rated at or above the "collaborates" level, meaning AI does large chunks of the task under close human direction, not just marginal assistance.

Anthropic's own caveats matter here. The ratings depend on a judge model, and when they checked how often that judge agreed with human raters, agreement was only 59%, compared to 35% agreement between two human raters on the same task. That's better than human-human agreement, but it's still far from a clean signal, and it means the 26% figure has real measurement noise baked in. The task basket is also frozen at a point in time, so it won't capture new categories of work as they emerge, and there's no shared methodology across labs, so this number can't be compared to what OpenAI, Google DeepMind, or anyone else is doing internally. It's a self-reported figure, rated by an AI, about that same company's AI.

**Metric 2: oversight of AI agents**

Anthropic reports around 30,000 agents running simultaneously on its primary internal platform. Online monitors reviewed 100% of actions within seconds, blocking 0.002% of them, about 1 in 47,000, out of more than a billion decisions Anthropic analyzed in August. Offline monitors separately reviewed roughly 100,000 transcripts a week and escalated only about 50 of them, roughly 1 to 2 per thousand, to human review.

That 0.002% figure can be read two ways. It could mean the agents are behaving well, or it could mean the monitoring is only catching a narrow slice of what "concerning" looks like. Anthropic leans toward caution on this itself, stating plainly that "at this scale of agent activity, it is hard to be certain we have a complete picture of all possible kinds of behaviors," and noting this monitoring reflects months of experience, not years. Coverage percentage tells you actions were looked at, not that the review was capable of catching genuinely novel failure modes. A near-zero block rate from a system still building its detection taxonomy isn't strong evidence of safety on its own.

**Metric 3: compute allocated to safety**

Anthropic classified one week of compute usage (July 13-20) by whether its "dominant purpose" was safety, reporting about 6% of total AI R&D compute and 12% of AI-driven R&D compute went to safety work.

Anthropic flags several problems with this metric that are worth repeating rather than smoothing over. Compute is "an imperfect proxy" for safety focus because safety research is often labor-intensive rather than compute-intensive, so the percentage can understate real effort. Classification of what counts as safety work is "not black and white," and the underlying labels are described as "best-effort, not verified." The measurement is a single snapshot week, not a trend. And a genuinely useful improvement, a more efficient safety classifier, would mechanically lower the reported percentage without any actual drop in safety effort. That's a metric where the number can move in a direction that looks worse even when nothing bad has happened.

**The verification question**

Anthropic proposes that outside evaluators or even rival labs could eventually verify these numbers, while acknowledging that a judge model checking these systems "could make the same kinds of errors as the model it is checking." That's the honest core problem: every one of these three metrics is currently self-defined, self-measured, and self-reported by the same organization whose pace it's meant to describe. That doesn't make the metrics useless, first attempts at transparency rarely are, but it does mean the numbers describe Anthropic's internal picture of itself before anyone outside the company has been able to check the work.

Source: https://www.anthropic.com/institute/measuring-pace-of-ai-development
