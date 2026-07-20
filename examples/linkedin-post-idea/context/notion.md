# Notion Integration

## Dashboard

**Page:** Content Agent Dashboard
**URL:** https://www.notion.so/sneharup-mukherjee/Content-Agent-Dashboard-360e273c710780c0a7d0d8669e04e62f

---

## Databases

### Hook Ideas
Stores the 9 hooks generated each run. Team reviews and approves here.

- **Database URL:** https://www.notion.so/c6fbb06c5d524b9a9028060ffb29ce82
- **Data source ID:** `036a5fce-4895-44e9-b965-9990ef3b8bff`

Schema (use exact property names):
| Property | Type | Notes |
|---|---|---|
| `Hook` | title | The hook text |
| `date:Date:start` | date | ISO-8601 e.g. `2026-05-14` |
| `Idea` | text | Angle name e.g. "Discovery Call Tax" |
| `Type` | select | `Contrarian` / `Identity` / `Insight` |
| `Source Post` | text | Post title verbatim |
| `Source URL` | url | Reddit permalink |
| `Subreddit` | select | `r/lifecoaching` / `r/coaching` / `r/smallbusiness` / `r/freelance` / `r/Solopreneur` |
| `Upvotes` | number | Integer |
| `Comments` | number | Integer |
| `Status` | select | Always set to `Draft` on creation |
| `Notes` | text | Leave blank on creation |

### Full Posts
Stores the expanded LinkedIn posts. Team edits and approves here.

- **Database URL:** https://www.notion.so/6095107b5fdb46b18b356778305270a0
- **Data source ID:** `1da33f42-9091-4e3f-99e4-cf0073a7389d`

Schema (use exact property names):
| Property | Type | Notes |
|---|---|---|
| `Title` | title | e.g. "2026-05-14 — 2B Identity" |
| `Post Content` | text | Full post text, plain — no markdown formatting |
| `Status` | select | Always set to `Draft` on creation |
| `date:Date Posted:start` | date | Leave blank on creation |
| `Performance` | select | Leave blank on creation |
| `Notes` | text | Leave blank on creation |
