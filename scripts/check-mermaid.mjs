#!/usr/bin/env node
// Renders every Mermaid block in every Markdown file with mermaid-cli (mmdc)
// and fails on syntax errors, naming the file and block.
//
// Usage: node scripts/check-mermaid.mjs [files or directories]
// Requires: npm ci (installs @mermaid-js/mermaid-cli, which bundles Chromium)

import { readdirSync, readFileSync, mkdtempSync, rmSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { tmpdir } from "node:os";
import { execFileSync } from "node:child_process";

const ROOT = join(import.meta.dirname, "..");
const SKIP_DIRS = new Set([".git", "node_modules", "_site", "site-src"]);
const BLOCK_RE = /(^|\n)```mermaid[^\n]*\n([\s\S]*?)\n```/g;

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

const files = targetsFrom(process.argv);
const workDir = mkdtempSync(join(tmpdir(), "mermaid-check-"));
const puppeteerConfig = join(ROOT, "scripts", "puppeteer-config.json");
const failures = [];
let blocks = 0;

for (const file of files) {
  const rel = relative(ROOT, file);
  const text = readFileSync(file, "utf8");
  let match;
  const lineStarts = [0];
  for (let i = 0; i < text.length; i++) if (text[i] === "\n") lineStarts.push(i + 1);

  while ((match = BLOCK_RE.exec(text)) !== null) {
    blocks++;
    const blockIndex = blocks;
    const blockNo = [...text.slice(0, match.index).matchAll(BLOCK_RE)].length + 1;
    const startLine = lineStarts.filter((p) => p <= match.index).length;
    const mmd = join(workDir, `block-${blockIndex}.mmd`);
    const svg = join(workDir, `block-${blockIndex}.svg`);
    const { writeFileSync } = await import("node:fs");
    writeFileSync(mmd, match[2]);

    try {
      execFileSync(
        join(ROOT, "node_modules", ".bin", "mmdc"),
        ["-i", mmd, "-o", svg, "-p", puppeteerConfig, "-b", "transparent", "--quiet"],
        { stdio: "pipe", cwd: ROOT },
      );
    } catch (err) {
      const stderr = (err.stderr ? err.stderr.toString() : err.message)
        .split("\n")
        .filter((l) => l.trim() !== "")
        .slice(-8)
        .join("\n");
      failures.push({ rel, blockNo, startLine, stderr });
    }
  }
}

rmSync(workDir, { recursive: true, force: true });

if (failures.length > 0) {
  console.error(`Mermaid check failed: ${failures.length} of ${blocks} blocks did not render`);
  for (const f of failures) {
    console.error("");
    console.error(`  ${f.rel}: mermaid block ${f.blockNo} (around line ${f.startLine})`);
    for (const line of f.stderr.split("\n")) console.error(`    ${line}`);
  }
  process.exit(1);
}

console.log(`Mermaid check passed: ${blocks} blocks across ${files.length} files rendered`);
