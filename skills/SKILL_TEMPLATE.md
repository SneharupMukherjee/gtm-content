---
name: skill-slug
description: >
  One or two sentences. What this skill does, the concrete artifact it produces,
  and when Claude should auto-load it (the phrases a user would type).
tags: [domain]
---

# Skill Title

**Tier:** capability | composite | playbook
**Duration:** X–Y minutes
**Output:** `outputs/[YYYY-MM-DD]-[type]-[name].md`

## Quick Start

```
Read skills/<tier>/<slug>/SKILL.md and <do the thing for> [input]
```

## Purpose

What problem this solves and why it beats doing it by hand. Be specific about the
outcome, not the steps.

## When to Run

- Trigger 1
- Trigger 2

## Inputs

- Required input
- `context/…` files this skill reads

## Steps

### Step 1: …
### Step 2: …

## Output Format

The exact shape of the deliverable. Link to a worked example in `examples/`.

## Chains With

- Upstream: `skills/…` that feeds this
- Downstream: `skills/…` this feeds
