#!/usr/bin/env node
// Style check for CONTRIBUTING.md rules.
// Fails on em dashes, spaced en dashes, emojis and old product names outside
// an allow-list. Official Microsoft link titles are always allowed, and lines
// that explain a rename (for example "formerly Azure AD") are allowed, because
// CONTRIBUTING.md says to mention old names once when it helps.
//
// Usage: node scripts/check-style.mjs [files or directories]

import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join, relative } from "node:path";

const ROOT = join(import.meta.dirname, "..");

// Characters CONTRIBUTING.md bans in prose.
const BANNED_CHARS = [
  { name: "em dash", re: /\u2014/ },
  { name: "spaced en dash (write it with commas or brackets instead)", re: / \u2013 |\u2013 / },
];

// Emoji and pictograph ranges. Deliberately broad; if it ever flags a
// legitimate character, add the line to scripts/style-allowlist.txt.
const EMOJI_RE =
  /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{2705}\u{274C}\u{26A0}\u{1F1E6}-\u{1F1FF}]/u;

// Old product names. Fine to mention once, with context, per CONTRIBUTING.md.
const BANNED_TERMS = [
  { term: "Azure AD", re: /\bAzure AD\b/ },
  { term: "Azure Active Directory", re: /\bAzure Active Directory\b/ },
  { term: "Azure Sentinel", re: /\bAzure Sentinel\b/ },
  { term: "Microsoft 365 Defender", re: /\bMicrosoft 365 Defender\b/ },
  { term: "Office 365 Advanced Threat Protection", re: /\bOffice 365 Advanced Threat Protection\b/i },
  { term: "Office 365 ATP", re: /\bOffice 365 ATP\b/ },
  { term: "Azure ATP", re: /\bAzure ATP\b/ },
  { term: "MDATP", re: /\bMDATP\b/ },
  { term: "MCAS", re: /\bMCAS\b/ },
  { term: "Azure AI Foundry", re: /\bAzure AI Foundry\b/ },
];

// A line that explains a rename may use the old name once.
const RENAME_CONTEXT =
  /formerly|renamed|old name|was called|replaced|superseded|previously known|deprecated|retired|legacy/i;

// A line that links an official Microsoft source may quote its exact title,
// even when the title still uses an old name.
const OFFICIAL_TITLE =
  /learn\.microsoft\.com|techcommunity\.microsoft\.com|github\.com\/Azure\/Azure-Sentinel|azure\.microsoft\.com|microsoft\.github\.io/;

const SKIP_DIRS = new Set([
  ".git",
  "node_modules",
  "_site",
  "site-src",
  ".github",
  "scripts",
]);

function loadAllowlist() {
  const entries = [];
  const file = join(ROOT, "scripts", "style-allowlist.txt");
  if (existsSync(file)) {
    for (const raw of readFileSync(file, "utf8").split("\n")) {
      const line = raw.trim();
      if (line === "" || line.startsWith("#")) continue;
      entries.push({ re: new RegExp(line), raw: line });
    }
  }
  return entries;
}

function walkMarkdown(dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      walkMarkdown(join(dir, entry.name), out);
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      out.push(join(dir, entry.name));
    }
  }
  return out;
}

function targetsFrom(argv) {
  const args = argv.slice(2);
  if (args.length === 0) return walkMarkdown(ROOT);
  const out = [];
  for (const arg of args.map((a) => join(ROOT, a))) {
    if (statSync(arg).isDirectory()) walkMarkdown(arg, out);
    else if (arg.endsWith(".md")) out.push(arg);
  }
  return out;
}

const allowlist = loadAllowlist();
const files = targetsFrom(process.argv);
const errors = [];

for (const file of files) {
  const rel = relative(ROOT, file);
  const text = readFileSync(file, "utf8");
  const lines = text.split("\n");
  lines.forEach((line, i) => {
    const where = `${rel}:${i + 1}`;

    const allowed =
      RENAME_CONTEXT.test(line) ||
      OFFICIAL_TITLE.test(line) ||
      allowlist.some((a) => a.re.test(line) || a.re.test(`${rel}:${line}`));
    if (allowed) return;

    for (const { name, re } of BANNED_CHARS) {
      if (re.test(line)) {
        errors.push(`${where}: banned character: ${name}`);
        return;
      }
    }
    if (EMOJI_RE.test(line)) {
      errors.push(`${where}: banned character: emoji`);
      return;
    }
    for (const { term, re } of BANNED_TERMS) {
      if (re.test(line)) {
        errors.push(`${where}: old product name "${term}": ${line.trim().slice(0, 100)}`);
        return;
      }
    }
  });
}

if (errors.length > 0) {
  console.error(`Style check failed: ${errors.length} issue${errors.length === 1 ? "" : "s"}`);
  for (const e of errors) console.error(`  ${e}`);
  console.error("");
  console.error("CONTRIBUTING.md bans em dashes, emojis and old product names.");
  console.error("Rename to the current product, add rename context, or quote the official");
  console.error("title on a linked line. Genuine exceptions go in scripts/style-allowlist.txt.");
  process.exit(1);
}

console.log(`Style check passed: ${files.length} files`);
