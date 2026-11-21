#!/usr/bin/env node
/**
 * Upstream drift detector for the Microsoft security logging guide.
 *
 * Scans every product guide and cross-cutting doc, compares its "Last verified"
 * date against:
 *   1. Broken links reported by lychee (optional --lychee-json)
 *   2. New commits on linked Azure/Azure-Sentinel Solutions folders
 *   3. Newer updated_at / ms.date timestamps on linked Microsoft Learn pages
 *   4. Guides whose "Last verified" date is older than 180 days
 *
 * Exits 0 on success and writes structured Markdown + JSON reports plus
 * GITHUB_OUTPUT variables (has_drift, target_count, target_files).
 */

import { appendFileSync, existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const ROOT = resolve(import.meta.dirname, "..");
const STALE_DAYS = 180;
const CONCURRENCY = 12;
const FETCH_TIMEOUT_MS = 12_000;

const PRODUCT_GROUPS = [
  "identity",
  "endpoint",
  "email-collab",
  "cloud-apps",
  "azure",
  "data-security",
  "business-apps",
  "ai",
  "devops",
  "servers",
  "multi-cloud",
];

const MONTHS = {
  jan: 0,
  feb: 1,
  mar: 2,
  apr: 3,
  may: 4,
  jun: 5,
  jul: 6,
  aug: 7,
  sep: 8,
  oct: 9,
  nov: 10,
  dec: 11,
};

function parseArgs(argv) {
  const opts = {
    maxGuides: 8,
    lycheeJson: null,
    mdOut: null,
    jsonOut: null,
    targetFiles: [],
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--max-guides" && argv[i + 1]) {
      opts.maxGuides = Math.max(1, Number.parseInt(argv[++i], 10) || 8);
    } else if (a === "--lychee-json" && argv[i + 1]) {
      opts.lycheeJson = argv[++i];
    } else if (a === "--md-out" && argv[i + 1]) {
      opts.mdOut = argv[++i];
    } else if (a === "--json-out" && argv[i + 1]) {
      opts.jsonOut = argv[++i];
    } else if (a === "--target-files" && argv[i + 1]) {
      opts.targetFiles = argv[++i]
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    }
  }
  return opts;
}

function listTrackedFiles() {
  const files = [];
  for (const group of PRODUCT_GROUPS) {
    const dir = join(ROOT, group);
    if (!existsSync(dir)) continue;
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const readme = join(dir, entry.name, "README.md");
      if (existsSync(readme)) files.push(relative(ROOT, readme));
    }
  }
  const docsDir = join(ROOT, "docs");
  if (existsSync(docsDir)) {
    for (const entry of readdirSync(docsDir, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith(".md")) {
        files.push(relative(ROOT, join(docsDir, entry.name)));
      }
    }
  }
  return files.sort();
}

function parseVerifiedDate(text) {
  const m = text.match(/Last verified:\s*(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})/i);
  if (!m) return null;
  const day = Number.parseInt(m[1], 10);
  const month = MONTHS[m[2].toLowerCase()];
  const year = Number.parseInt(m[3], 10);
  if (month === undefined) return null;
  return new Date(Date.UTC(year, month, day));
}

function toIsoDate(d) {
  return d ? d.toISOString().slice(0, 10) : null;
}

function extractUrls(text) {
  const learn = new Set();
  const sentinelSolutions = new Set();
  const urlRe = /https:\/\/[^\s)>\]"']+/g;
  for (const raw of text.match(urlRe) || []) {
    const clean = raw.replace(/[.,;:]+$/, "").split("#")[0];
    if (clean.startsWith("https://learn.microsoft.com/")) {
      if (!clean.includes("...")) learn.add(clean);
    } else {
      const sm = clean.match(
        /^https:\/\/github\.com\/Azure\/Azure-Sentinel\/(?:tree|blob)\/master\/Solutions\/([^/?#]+)/,
      );
      if (sm) {
        sentinelSolutions.add(decodeURIComponent(sm[1]));
      }
    }
  }
  return {
    learn: [...learn],
    sentinelSolutions: [...sentinelSolutions],
  };
}

function parseLycheeErrors(jsonPath) {
  const byFile = new Map();
  if (!jsonPath || !existsSync(jsonPath)) return byFile;
  try {
    const data = JSON.parse(readFileSync(jsonPath, "utf8"));
    const failMap = data.fail_map || {};
    for (const [filePath, failures] of Object.entries(failMap)) {
      const rel = filePath.replace(/^\.\//, "");
      if (!Array.isArray(failures) || failures.length === 0) continue;
      byFile.set(
        rel,
        failures.map((f) => ({
          url: f.url,
          status: f.status?.text || f.status?.code || "error",
        })),
      );
    }
  } catch (err) {
    console.error(`Warning: failed to parse lychee JSON (${jsonPath}): ${err.message}`);
  }
  return byFile;
}

async function fetchWithTimeout(url, headers = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    return await fetch(url, {
      redirect: "follow",
      signal: controller.signal,
      headers: {
        "User-Agent": "microsoft-security-logging-guide-drift-check/1.0",
        ...headers,
      },
    });
  } finally {
    clearTimeout(timer);
  }
}

async function checkLearnUrl(url) {
  try {
    const res = await fetchWithTimeout(url);
    if (res.status === 404 || res.status === 410) {
      return { url, status: res.status, broken: true, latestDate: null };
    }
    if (!res.ok) {
      return { url, status: res.status, broken: false, latestDate: null };
    }
    const html = await res.text();
    const dates = [];
    for (const metaName of ["ms.date", "updated_at"]) {
      const re = new RegExp(`<meta\\s+name=["']${metaName}["']\\s+content=["']([^"']+)["']`, "i");
      const m = html.match(re);
      if (m) {
        const parsed = new Date(m[1]);
        if (!Number.isNaN(parsed.getTime())) {
          // Normalise to UTC date-only midnight so same-day publishes don't re-trigger.
          dates.push(
            new Date(Date.UTC(parsed.getUTCFullYear(), parsed.getUTCMonth(), parsed.getUTCDate())),
          );
        }
      }
    }
    const latestDate =
      dates.length > 0 ? new Date(Math.max(...dates.map((d) => d.getTime()))) : null;
    return { url, status: res.status, broken: false, latestDate };
  } catch {
    return { url, status: 0, broken: false, latestDate: null };
  }
}

async function checkSentinelSolution(solutionName, sinceDate) {
  const headers = { Accept: "application/vnd.github+json" };
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  // Start strictly on the day AFTER sinceDate to avoid re-flagging same-day commits.
  const nextDay = new Date(sinceDate.getTime() + 24 * 60 * 60 * 1000);
  const pathParam = encodeURIComponent(`Solutions/${solutionName}`);
  const apiUrl = `https://api.github.com/repos/Azure/Azure-Sentinel/commits?path=${pathParam}&since=${nextDay.toISOString()}&per_page=5`;
  try {
    const res = await fetchWithTimeout(apiUrl, headers);
    if (!res.ok) return { solution: solutionName, commits: [] };
    const items = await res.json();
    if (!Array.isArray(items)) return { solution: solutionName, commits: [] };
    return {
      solution: solutionName,
      commits: items.map((c) => ({
        sha: (c.sha || "").slice(0, 7),
        date: (c.commit?.author?.date || "").slice(0, 10),
        message: (c.commit?.message || "").split("\n")[0].slice(0, 120),
      })),
    };
  } catch {
    return { solution: solutionName, commits: [] };
  }
}

async function runPool(items, limit, worker) {
  const results = new Array(items.length);
  let next = 0;
  async function runner() {
    while (next < items.length) {
      const idx = next++;
      results[idx] = await worker(items[idx]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, runner));
  return results;
}

function writeGithubOutput(kv) {
  const outFile = process.env.GITHUB_OUTPUT;
  if (!outFile) return;
  for (const [k, v] of Object.entries(kv)) {
    appendFileSync(outFile, `${k}=${v}\n`, "utf8");
  }
}

async function main() {
  const opts = parseArgs(process.argv);
  const today = new Date();
  const todayUtc = new Date(
    Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()),
  );

  const allFiles = listTrackedFiles();
  const lycheeErrors = parseLycheeErrors(opts.lycheeJson);

  // If caller explicitly pinned target files via workflow_dispatch, inspect only those.
  const filesToScan =
    opts.targetFiles.length > 0
      ? opts.targetFiles.filter((f) => existsSync(join(ROOT, f)))
      : allFiles;

  const fileMeta = filesToScan.map((rel) => {
    const text = readFileSync(join(ROOT, rel), "utf8");
    const verified = parseVerifiedDate(text);
    const urls = extractUrls(text);
    return { rel, verified, ...urls };
  });

  // Deduplicate all Microsoft Learn URLs across tracked files.
  const uniqueLearnUrls = [...new Set(fileMeta.flatMap((f) => f.learn))];
  console.log(
    `Scanning ${fileMeta.length} files (${uniqueLearnUrls.length} unique Microsoft Learn URLs)...`,
  );

  const learnResults = await runPool(uniqueLearnUrls, CONCURRENCY, checkLearnUrl);
  const learnByUrl = new Map(learnResults.map((r) => [r.url, r]));

  // Deduplicate Azure-Sentinel solutions paired with the oldest Last verified date referencing them.
  const solutionOldestDate = new Map();
  for (const f of fileMeta) {
    const baseDate = f.verified || new Date(Date.UTC(2025, 0, 1));
    for (const sol of f.sentinelSolutions) {
      const prev = solutionOldestDate.get(sol);
      if (!prev || baseDate < prev) solutionOldestDate.set(sol, baseDate);
    }
  }
  const solutionEntries = [...solutionOldestDate.entries()];
  const solutionResults = await runPool(solutionEntries, 6, ([sol, dt]) =>
    checkSentinelSolution(sol, dt),
  );
  const commitsBySolution = new Map(solutionResults.map((r) => [r.solution, r.commits]));

  const findings = [];
  for (const f of fileMeta) {
    const verifiedDate = f.verified;
    const verifiedIso = toIsoDate(verifiedDate);
    const brokenLinks = [...(lycheeErrors.get(f.rel) || [])];
    const updatedLearn = [];
    const updatedSolutions = [];
    let staleDays = null;

    if (verifiedDate) {
      const ageDays = Math.floor((todayUtc - verifiedDate) / (24 * 60 * 60 * 1000));
      if (ageDays >= STALE_DAYS) staleDays = ageDays;
    } else {
      staleDays = 999;
    }

    for (const u of f.learn) {
      const r = learnByUrl.get(u);
      if (!r) continue;
      if (r.broken) {
        if (!brokenLinks.some((b) => b.url === u)) {
          brokenLinks.push({ url: u, status: String(r.status) });
        }
      } else if (r.latestDate && verifiedDate && r.latestDate > verifiedDate) {
        updatedLearn.push({ url: u, updated: toIsoDate(r.latestDate) });
      }
    }

    for (const sol of f.sentinelSolutions) {
      const commits = (commitsBySolution.get(sol) || []).filter(
        (c) => !verifiedIso || c.date > verifiedIso,
      );
      if (commits.length > 0) {
        updatedSolutions.push({ solution: sol, commits });
      }
    }

    const forced = opts.targetFiles.length > 0;
    const score =
      brokenLinks.length * 100 +
      updatedSolutions.length * 40 +
      updatedLearn.length * 10 +
      (staleDays !== null ? 5 : 0) +
      (forced ? 1 : 0);

    if (score > 0) {
      findings.push({
        file: f.rel,
        lastVerified: verifiedIso || "missing",
        score,
        brokenLinks,
        updatedSolutions,
        updatedLearn,
        staleDays,
        forced,
      });
    }
  }

  findings.sort((a, b) => b.score - a.score || a.file.localeCompare(b.file));
  const selected = findings.slice(0, opts.maxGuides);
  const deferred = findings.slice(opts.maxGuides);

  const report = {
    generatedAt: today.toISOString(),
    scannedFiles: fileMeta.length,
    uniqueLearnUrls: uniqueLearnUrls.length,
    totalDrifted: findings.length,
    selectedCount: selected.length,
    deferredCount: deferred.length,
    selected,
    deferred: deferred.map((d) => d.file),
  };

  const mdLines = [
    "# Nightly guidance drift report",
    "",
    `- Generated: ${today.toISOString().slice(0, 10)} (UTC)`,
    `- Files scanned: ${fileMeta.length}`,
    `- Unique Microsoft Learn pages checked: ${uniqueLearnUrls.length}`,
    `- Files with detected drift: ${findings.length} (processing top ${selected.length} this run)`,
    "",
  ];

  if (selected.length === 0) {
    mdLines.push("No upstream drift, broken links or stale guides detected.");
  } else {
    mdLines.push("## Files selected for refresh", "");
    for (const item of selected) {
      mdLines.push(`### \`${item.file}\` (Last verified: ${item.lastVerified})`);
      if (item.brokenLinks.length > 0) {
        mdLines.push("- **Broken links:**");
        for (const b of item.brokenLinks) {
          mdLines.push(`  - \`${b.status}\` ${b.url}`);
        }
      }
      if (item.updatedSolutions.length > 0) {
        mdLines.push("- **Azure-Sentinel solution commits since last verified:**");
        for (const s of item.updatedSolutions) {
          for (const c of s.commits) {
            mdLines.push(`  - \`Solutions/${s.solution}\` (${c.date}, \`${c.sha}\`): ${c.message}`);
          }
        }
      }
      if (item.updatedLearn.length > 0) {
        mdLines.push("- **Microsoft Learn pages updated since last verified:**");
        for (const l of item.updatedLearn) {
          mdLines.push(`  - (${l.updated}) ${l.url}`);
        }
      }
      if (item.staleDays !== null) {
        mdLines.push(`- **Stale guide:** ${item.staleDays} days since last verified (>= ${STALE_DAYS} days).`);
      }
      if (
        item.forced &&
        item.brokenLinks.length === 0 &&
        item.updatedSolutions.length === 0 &&
        item.updatedLearn.length === 0 &&
        item.staleDays === null
      ) {
        mdLines.push("- **Manual refresh requested.**");
      }
      mdLines.push("");
    }
    if (deferred.length > 0) {
      mdLines.push(
        `## Deferred to subsequent nightly runs (${deferred.length})`,
        "",
        ...deferred.map((d) => `- \`${d.file}\``),
        "",
      );
    }
  }

  const mdText = mdLines.join("\n") + "\n";

  if (opts.jsonOut) writeFileSync(opts.jsonOut, JSON.stringify(report, null, 2) + "\n", "utf8");
  if (opts.mdOut) writeFileSync(opts.mdOut, mdText, "utf8");

  console.log(mdText);

  writeGithubOutput({
    has_drift: selected.length > 0 ? "true" : "false",
    target_count: String(selected.length),
    target_files: selected.map((s) => s.file).join(","),
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
