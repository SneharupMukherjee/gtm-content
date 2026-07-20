# CLAUDE.md — GTM Content

Persistent context layer for this repo. Claude Code reads it at the start of every
session. This is the **summary**; deep context lives in `context/`.

---

## What This Repo Does

GTM Content is the **demand + authority** layer: content built to rank on Google *and* get
cited by answer engines (ChatGPT, Claude, Perplexity, AI Overviews). It researches keywords
and AI prompts, plans a content architecture, writes product-led pages, builds AI-readable
charts, audits for truth before publishing, and turns community pain into LinkedIn hooks.

## Skill Taxonomy

- **capabilities/** — `research-keywords`, `geo-content-research`, `create-geo-charts`, `reddit-opportunity-research`
- **composites/** — `geo-content-planning`, `write-seo-geo-content`, `audit-content`, `linkedin-post-ideas`
- **playbooks/** — `geo-content-pipeline`

```
Read skills/playbooks/geo-content-pipeline/SKILL.md and build the content pipeline for [brand.com]
```

## Context Files

- `context/linkedin-voice.md` — voice for LinkedIn content
- Add: brand DNA (from gtm-intelligence `brand-research`), which most skills read as input

## Conventions

- Structured outputs use fixed CSV schemas (`*.schema.md` inside each skill)
- Outputs land in `outputs/` (content under `outputs/content/`)
- Never commit scraped raw data or `*.csv` outside `examples/`
- Validate skills: `node scripts/validate-skills.js`

## This Week

- [ ] Run `research-keywords` + `geo-content-research` for the target brand
