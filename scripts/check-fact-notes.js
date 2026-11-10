#!/usr/bin/env node

/**
 * @module check-fact-notes
 * @description Fails when a fact-bearing skill does not carry a provenance note
 * pointing at docs/CERTIFICATION-FACTS.md, when the note carries a stale
 * verification date, when the link target does not resolve, or when the note is
 * not placed right after the skill's Decision Frame.
 *
 * The note is provenance, not a runtime dependency: skills are installed as
 * directories, so docs/ does not travel with them. The wording must therefore
 * describe a snapshot rather than promise a readable file.
 *
 * @example
 * node scripts/check-fact-notes.js
 */

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = join(ROOT, "skills");
const FACTS_PATH = join(ROOT, "docs", "CERTIFICATION-FACTS.md");
const FACTS_LINK = "../../docs/CERTIFICATION-FACTS.md";

// Skills whose numbers must be traceable to the fact sheet, and the sentence
// variant each one must use. Certification skills are persona-only: they carry
// no exam numbers, so they are deliberately absent from this list. Only
// standards still publish versions that must stay traceable.
const EXPECTED = {
  "mitre-attack": "standar",
  "nist-800-53": "standar",
};

const VARIANTS = {
  sertifikasi: "Angka ujian di skill ini",
  standar: "Versi dan angka framework di skill ini",
};

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function readFactDate() {
  if (!existsSync(FACTS_PATH)) {
    fail(`fact sheet not found at ${FACTS_PATH}`);
    return "";
  }

  const content = readFileSync(FACTS_PATH, "utf8");
  const match = content.match(/\*\*Terakhir diverifikasi:\*\*\s*(\d{4}-\d{2}-\d{2})/);

  if (!match) {
    fail("fact sheet has no `**Terakhir diverifikasi:** YYYY-MM-DD` line");
    return "";
  }

  return match[1];
}

function checkSkill(name, variant, factDate) {
  const skillPath = join(SKILLS_DIR, name, "SKILL.md");

  if (!existsSync(skillPath)) {
    fail(`${name}: SKILL.md not found`);
    return;
  }

  const lines = readFileSync(skillPath, "utf8").split(/\r?\n/);
  const noteIndexes = [];

  for (let i = 0; i < lines.length; i += 1) {
    if (lines[i].includes("CERTIFICATION-FACTS.md")) {
      noteIndexes.push(i);
    }
  }

  if (noteIndexes.length === 0) {
    fail(`${name}: no provenance note pointing at docs/CERTIFICATION-FACTS.md`);
    return;
  }

  if (noteIndexes.length > 1) {
    fail(`${name}: ${noteIndexes.length} provenance notes, expected exactly 1`);
    return;
  }

  const noteIndex = noteIndexes[0];
  const note = lines[noteIndex];

  if (!note.trimStart().startsWith(">")) {
    fail(`${name}: provenance note must be a blockquote`);
  }

  if (!note.includes(VARIANTS[variant])) {
    fail(`${name}: note must use the "${variant}" wording ("${VARIANTS[variant]}...")`);
  }

  if (!note.includes(FACTS_LINK)) {
    fail(`${name}: note must link to ${FACTS_LINK}`);
  }

  if (factDate && !note.includes(factDate)) {
    fail(`${name}: note is dated differently from the fact sheet (expected ${factDate})`);
  }

  const linkMatch = note.match(/\]\(([^)]+CERTIFICATION-FACTS\.md)\)/);
  if (!linkMatch) {
    fail(`${name}: note has no markdown link to the fact sheet`);
  } else {
    const target = resolve(join(SKILLS_DIR, name), linkMatch[1]);
    if (!existsSync(target)) {
      fail(`${name}: link target does not resolve (${linkMatch[1]})`);
    }
  }

  const frameIndex = lines.findIndex((line) => /^## Decision Frame\s*$/.test(line));
  if (frameIndex === -1) {
    fail(`${name}: no "## Decision Frame" section to anchor the note`);
    return;
  }

  let nextSection = lines.length;
  for (let i = frameIndex + 1; i < lines.length; i += 1) {
    if (/^## /.test(lines[i])) {
      nextSection = i;
      break;
    }
  }

  if (noteIndex < frameIndex || noteIndex > nextSection) {
    fail(`${name}: provenance note must sit between "## Decision Frame" and the next H2`);
  }
}

function main() {
  const factDate = readFactDate();

  const known = new Set(Object.keys(EXPECTED));
  const present = readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => existsSync(join(SKILLS_DIR, name, "SKILL.md")));

  for (const name of Object.keys(EXPECTED)) {
    if (!present.includes(name)) {
      fail(`${name}: registered as fact-bearing but the skill does not exist`);
    }
  }

  for (const name of present) {
    if (!known.has(name)) {
      const content = readFileSync(join(SKILLS_DIR, name, "SKILL.md"), "utf8");
      if (content.includes("CERTIFICATION-FACTS.md")) {
        fail(`${name}: links to the fact sheet but is not registered in this checker`);
      }
    }
  }

  for (const [name, variant] of Object.entries(EXPECTED)) {
    checkSkill(name, variant, factDate);
  }

  if (process.exitCode) {
    console.error("\nFact notes: FAILED");
    return;
  }

  console.log(
    `OK: ${Object.keys(EXPECTED).length} fact-bearing skill(s) carry a current, resolvable provenance note (fact sheet ${factDate}).`
  );
}

main();
