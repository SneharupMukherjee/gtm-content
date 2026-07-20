---
name: linkedin-post-ideas
description: >
  Mine what's actually trending in your audience's communities (Reddit + comments), then
  turn real pain points into LinkedIn hook ideas written in a specific person's voice.
  Every idea traces back to a real post with real engagement — no invented thought
  leadership. Auto-loads on "give me LinkedIn post ideas" or "what should I post about".
tags: [content]
---

# LinkedIn Post Ideas

**Tier:** composite
**Duration:** 15–25 minutes
**Output:** `outputs/[YYYY-MM-DD]-linkedin-ideas.md` (+ drafted hooks)

## Quick Start

```
Read skills/composites/linkedin-post-ideas/SKILL.md and give me 5 LinkedIn post ideas for this week
```

## Purpose

Kill the blank page. Instead of inventing "thought leadership", this mines the communities
where your buyers actually complain (via `scripts/fetch_reddit.py` /
`scripts/fetch_comments.py`), finds threads with real engagement, and converts the pain
into hooks in your voice. Ported from the standalone **linkedin-post-idea** agent; the
worked build is in `examples/linkedin-post-idea/`.

## When to Run

- Weekly content planning
- When you need hooks grounded in real demand, not guesses

## Inputs

- Target subreddits / communities
- `context/linkedin-voice.md` — the voice to write in
- (optional) `reddit-opportunity-research` output for deeper community mapping

## Steps

1. **Fetch** — pull trending posts + top comments from the target communities.
2. **Analyze** — rank by engagement + relevance; extract the underlying pain/insight.
3. **Draft hooks** — write LinkedIn openers in-voice; each cites the source thread.
4. **Critique** — cut anything that reads generic or that you can't trace to a real post.

## Output Format

```
# LinkedIn Post Ideas — YYYY-MM-DD
1. Hook: "…"   ← source: [reddit thread] (N upvotes / M comments)
   Angle / why it lands
```

## Chains With

- Upstream: `reddit-opportunity-research`
- Downstream: gtm-outreach `publish-to-buffer` (ship the finished post)
- Voice: `context/linkedin-voice.md`
