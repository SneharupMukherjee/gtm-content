---
name: geo-content-pipeline
description: >
  End-to-end content engine for the answer-engine era: brand → keyword + GEO prompt
  research → content architecture → written pages + charts → pre-publish audit. Chains the
  capability and composite skills into one run. Auto-loads on "build our content pipeline"
  or "plan and write SEO/GEO content for [brand]".
tags: [content]
---

# GEO Content Pipeline

**Tier:** playbook
**Duration:** multi-session
**Output:** `outputs/content/` — keywords.csv, prompts.csv, plan.csv, markdown pages, charts

## Quick Start

```
Read skills/playbooks/geo-content-pipeline/SKILL.md and build the content pipeline for [brand.com]
```

## Purpose

Search is shifting from ranked blue links to answer engines (ChatGPT, Claude, Perplexity,
AI Overviews). Winning there needs direct answers, structure, sources, quotable passages,
and AI-readable charts. This playbook runs the whole chain so each stage's file becomes
context for the next.

## Pipeline

```mermaid
flowchart TD
    RK["research-keywords<br/>→ keywords.csv"]
    GCR["geo-content-research<br/>→ prompts.csv"]
    ROR["reddit-opportunity-research<br/>→ community pain"]
    GCP["geo-content-planning<br/>→ plan.csv (architecture)"]
    WSGC["write-seo-geo-content<br/>→ markdown pages"]
    CGC["create-geo-charts<br/>→ SVG/HTML/JSON-LD"]
    AC["audit-content<br/>→ verified claims + links"]

    RK --> GCP
    GCR --> GCP
    ROR --> GCP
    GCP --> WSGC
    GCP --> CGC
    WSGC --> AC
    CGC --> AC
```

## Process

1. **Research** — `research-keywords` + `geo-content-research` (+ `reddit-opportunity-research`).
2. **Plan** — `geo-content-planning` reads the research and emits `plan.csv` (which pages,
   which clusters, build order).
3. **Produce** — `write-seo-geo-content` for pages, `create-geo-charts` for evidence.
4. **Audit** — `audit-content` verifies every stat, URL, and claim before publishing.
5. **Distribute** — hand finished pieces to gtm-outreach `publish-to-buffer` or the web repo.

## Inputs

- Brand DNA (from gtm-intelligence `brand-research`)
- Target keyword/prompt space

## Chains With

- Uses every capability + composite in this repo
- Upstream: gtm-intelligence `brand-research`
- Downstream: gtm-outreach `publish-to-buffer`, gtm-web-analytics `build-resource-pages`
