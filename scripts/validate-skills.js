#!/usr/bin/env node
/**
 * Validate every skills/<level>/<slug>/SKILL.md in this repo.
 *
 * Layout (single-domain repo — the repo itself is the GTM domain):
 *   skills/<capabilities|composites|playbooks>/<slug>/SKILL.md
 *
 * Checks:
 *   - level is one of the three abstraction tiers
 *   - <slug> is lowercase-kebab and matches the SKILL.md `name` frontmatter
 *   - slugs are unique across the repo
 *   - required frontmatter present: name, description
 * Adapted from goose-skills/scripts/validate-skills.js (which keys on a
 * <domain>/<level> path; here the domain is implicit in the repo).
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SKILLS = path.join(ROOT, "skills");
const LEVELS = new Set(["capabilities", "composites", "playbooks"]);
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const errors = [];
const slugs = new Map();

function parseFrontmatter(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split("\n")) {
    const kv = line.match(/^([A-Za-z_]+):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].trim();
  }
  return fm;
}

if (!fs.existsSync(SKILLS)) {
  console.error("No skills/ directory found");
  process.exit(1);
}

for (const level of fs.readdirSync(SKILLS)) {
  const levelDir = path.join(SKILLS, level);
  if (!fs.statSync(levelDir).isDirectory()) continue;
  if (!LEVELS.has(level)) {
    errors.push(`Unexpected level dir: skills/${level} (must be capabilities|composites|playbooks)`);
    continue;
  }
  for (const slug of fs.readdirSync(levelDir)) {
    const slugDir = path.join(levelDir, slug);
    if (!fs.statSync(slugDir).isDirectory()) continue;
    const skillPath = path.join(slugDir, "SKILL.md");
    const rel = `skills/${level}/${slug}/SKILL.md`;
    if (!fs.existsSync(skillPath)) {
      errors.push(`Missing SKILL.md: ${rel}`);
      continue;
    }
    if (!KEBAB.test(slug)) errors.push(`Slug not lowercase-kebab: ${rel}`);
    if (slugs.has(slug)) errors.push(`Duplicate slug "${slug}": ${rel} and ${slugs.get(slug)}`);
    slugs.set(slug, rel);

    const fm = parseFrontmatter(fs.readFileSync(skillPath, "utf8"));
    if (!fm) { errors.push(`Missing frontmatter: ${rel}`); continue; }
    if (!fm.name) errors.push(`Missing frontmatter "name": ${rel}`);
    else if (fm.name !== slug) errors.push(`frontmatter name "${fm.name}" != dir "${slug}": ${rel}`);
    if (!fm.description) errors.push(`Missing frontmatter "description": ${rel}`);
  }
}

if (errors.length) {
  console.error("Skill validation failed:");
  for (const e of errors) console.error(`- ${e}`);
  process.exit(1);
}
console.log(`OK — ${slugs.size} skill(s) validated.`);
