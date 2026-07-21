# LinkedIn Post Idea Agent

Mines what's actually trending in coaching communities on Reddit and turns it into LinkedIn
hook ideas written in Jane Doe's voice. Every idea traces back to a real post with real
engagement — no invented thought leadership.

---

## How to Run

```bash
cd /home/sneharup/outbound/linkedin-post-idea
claude
```

Then type any of:
```
find ideas
give me hooks
what's trending
run linkedin-post-idea
```

That's it. The agent runs the full pipeline automatically and saves output to `output/YYYY-MM-DD.md`.

---

## What Happens Under the Hood

The agent is an orchestrator with 3 subagents. Each run goes through 4 steps:

### Step 1 — Fetcher subagent
Calls `scripts/fetch_reddit.py` via Bash against Reddit's public JSON API (no API key needed).
Pulls hot/trending posts from 5 coaching subreddits, scores them by engagement, filters out
any posts already used (via `output/used-posts.log`), then selects 3 posts that cover distinct
themes. Writes a full ideas brief to `scratch/ideas.md`.

### Step 2 — Main agent drafts 9 hooks
Reads `scratch/ideas.md` (3 real Reddit posts with context). Writes 3 hooks per post:
- **Contrarian** — challenges a belief coaches hold
- **Identity** — speaks to the role conflict ("you became a coach to X, not to Y")
- **Insight/Observation** — pattern noticed across coaches, ends with a colon to pull them in

All hooks are written in Jane Doe's voice per `context/linkedin-voice.md`. Drafts saved to
`scratch/hooks-draft.md`.

### Step 3 — Critic subagent
Reads `scratch/hooks-draft.md` in isolation (no Reddit data in context). Scores all 9 hooks
on 6 dimensions, runs hard-block checks (banned words, em dashes, "Acme", engagement bait),
and returns **PUBLISH / REVISE / HOLD**. If REVISE, main agent fixes flagged hooks and
re-submits once. If HOLD, the run stops and you're shown the critique.

### Step 3b — Writer subagent (on demand)

After the run, pick any hook and say "write post for 2B" (or "expand 1C", "use 3A", etc.).
The writer subagent:
1. Looks up the source Reddit post for that hook from `scratch/ideas.md`
2. Fetches the top comments from the thread via `scripts/fetch_comments.py`
3. Mines the comments for the specific detail that makes the post feel observed, not invented
4. Writes the full 100–180 word LinkedIn post: hook → bridge → body → close
5. Saves to `output/posts/YYYY-MM-DD-[hook-id].md`

The Reddit comments are raw material — they're never quoted directly. They supply the concrete
detail (unexpected insight, specific number, exact framing) that makes a post land vs. feel generic.

### Step 4 — Save and log
Approved hooks saved to `output/YYYY-MM-DD.md`. The 3 source post URLs appended to
`output/used-posts.log` so they're never surfaced again.

---

## Subreddits

Hardcoded in `scripts/fetch_reddit.py`. Current list:

| Subreddit | Why included |
|---|---|
| r/lifecoaching | Core ICP — coaches posting about their practice directly |
| r/coaching | Practitioner-focused, higher-quality signal per post |
| r/Solopreneur | Broad but high engagement; tool/workflow pain is common |
| r/smallbusiness | Active; pricing and client management threads weekly |
| r/freelance | Adjacent ICP pain — same admin and client management friction |

To add or remove subreddits, edit the `SUBREDDITS` list at the top of `scripts/fetch_reddit.py`.

---

## Output Files

| File | What it is |
|---|---|
| `output/YYYY-MM-DD.md` | Final hook set — 3 ideas, 9 hooks, critic verdict |
| `output/posts/YYYY-MM-DD-[id].md` | Full LinkedIn post for a chosen hook — ready to copy-paste |
| `output/used-posts.log` | One permalink per line — posts never to be surfaced again |
| `output/feedback-log.md` | Your feedback on which hooks you used/ignored/tweaked |
| `scratch/ideas.md` | Fetcher's ideas brief — overwritten each run |
| `scratch/hooks-draft.md` | Draft hooks for critic — overwritten each run |

Same-day reruns overwrite the output file. Scratch files are ephemeral.

---

## Logging Feedback (Important)

After each run, log which hooks you used, ignored, or tweaked in `output/feedback-log.md`.
One row per hook you have an opinion on — you don't need to log all 9, just the ones worth noting.

```markdown
| Date | Hook ID | Type | Theme | Subreddit | Verdict | Note |
|---|---|---|---|---|---|---|
| 2026-05-12 | 2B | Identity | Identity | r/coaching | used | Posted as-is, strong engagement |
| 2026-05-12 | 1A | Contrarian | Pricing | r/smallbusiness | tweaked | Changed opening, too formal |
| 2026-05-12 | 3C | Insight | Workflow | r/freelance | ignored | Too generic for coaching audience |
```

Verdict options: `used` / `tweaked` / `ignored` / `performed` (got engagement) / `flopped` (posted, no engagement)

---

## Writing the Full Post

After the run, pick any hook by ID and ask for the full post:

```
write post for 2B
expand 1C
use 3A
turn 2B into a post
```

The writer subagent fetches the original Reddit thread comments, mines them for the specific
detail that makes the post feel real, and writes the complete 100–180 word LinkedIn post.
Saved to `output/posts/YYYY-MM-DD-[hook-id].md` — ready to copy-paste or lightly edit.

**Post structure:**
- Hook (your chosen hook, verbatim or lightly tightened)
- Bridge (1–2 lines connecting to the specific insight)
- Body (2–4 lines with concrete detail from the thread)
- Close (quiet observation or question — never engagement bait)

---

## HITL Improvement Loop

After 3+ feedback entries, trigger the analyst:

```
analyze feedback
run analyst
what's working
improve the system
```

The analyst reads the feedback log, applies an n≥3 evidence threshold, and returns **staged
recommendations** — proposed diffs to `context/linkedin-voice.md`, hook type priority changes,
subreddit quality signals. Nothing is written until you explicitly approve. The system improves
over time based on what you actually use.

Example improvements the analyst can surface:
- "Identity hooks from pricing posts are used 4:1 vs Contrarian — recommend making Identity the primary type for that theme"
- "r/freelance posts score well but produce hooks you consistently mark 'too generic' — recommend removing from subreddit list"
- "ICP phrase 'discovery call' is appearing in used hooks more than 'admin' — add to voice file's preferred language"

---

## Fetch Script Options

Run directly if you want to inspect the raw Reddit data before the agent sees it:

```bash
# Default: hot posts, past week
python3 scripts/fetch_reddit.py

# Top posts, past month (fallback when weekly pool is exhausted)
python3 scripts/fetch_reddit.py --mode top --timeframe month --limit 15

# Day's trending posts (for a faster refresh)
python3 scripts/fetch_reddit.py --mode hot --timeframe day --limit 10
```

Output is JSON. Posts are pre-scored and pre-filtered against `output/used-posts.log`.

---

## Voice Rules (Quick Reference)

Full rules in `context/linkedin-voice.md`. Key constraints:

- No product name ("Acme") in any hook — hooks are content, not ads
- No banned words: leverage, optimize, streamline, ecosystem, synergy, game-changer, unpack, authentic, journey... (full list in voice file)
- No em dashes, no semicolons
- Max 1 exclamation point across the entire output file
- No engagement bait ("Comment YES", "Tag a coach", "Drop a 🔥 if...")
- Always contractions: don't, you're, it's, here's
- Specific over vague: "7 hours a week" beats "hours", "Calendly + Stripe + Zoom" beats "multiple tools"

---

## File Structure

```
linkedin-post-idea/
├── CLAUDE.md                        # Orchestrator — runs the 4-step workflow
├── README.md                        # This file
├── scripts/
│   └── fetch_reddit.py              # Reddit JSON API fetcher + scorer + deduplicator
├── context/
│   └── linkedin-voice.md            # Jane Doe's voice rules, ICP pain language, banned words
├── .claude/
│   ├── settings.json                # CLAUDE.md write-protection + tool permissions
│   └── agents/
│       ├── fetcher.md               # Runs fetch script, selects 3 ideas, writes scratch/ideas.md
│       ├── critic.md                # Scores 9 hooks, returns PUBLISH/REVISE/HOLD
│       ├── writer.md                # Fetches comments, writes full post, saves to output/posts/
│       └── analyst.md               # HITL improvement loop — reads feedback, proposes changes
├── scratch/
│   ├── ideas.md                     # Fetcher output — overwritten each run
│   └── hooks-draft.md               # Draft hooks for critic — overwritten each run
└── output/
    ├── YYYY-MM-DD.md                # Final approved hook sets
    ├── posts/                       # Full LinkedIn posts, one file per hook chosen
    │   └── YYYY-MM-DD-[hook-id].md
    ├── used-posts.log               # Deduplication — posts never surfaced again
    └── feedback-log.md              # Your feedback — feeds the HITL analyst
```
