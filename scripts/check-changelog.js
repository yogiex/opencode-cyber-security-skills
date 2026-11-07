#!/usr/bin/env node

/**
 * @module check-changelog
 * @description Fails when a file changed in the working tree or in a commit range
 * is not mentioned in CHANGELOG.md. Every changed path must appear in backticks.
 *
 * @example
 * // Working tree (staged, unstaged, untracked, renames)
 * node scripts/check-changelog.js
 *
 * @example
 * // CI: everything since the base branch
 * node scripts/check-changelog.js --base origin/main
 */

import { spawnSync } from "node:child_process";
import { closeSync, openSync, readFileSync, unlinkSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CHANGELOG_PATH = join(ROOT, "CHANGELOG.md");

// Temp files stay in the repository root: the sandbox denies writes inside
// .git, and a pipe would fail with EPERM. They are filtered out below and
// removed in a finally block.
const TEMP_DIR = ROOT;
const TEMP_PREFIX = ".changelog-tmp-";

// The changelog documents itself; requiring a self-reference adds noise.
const IGNORED = new Set(["CHANGELOG.md"]);

// Git output is redirected to files instead of pipes: under the Windows
// sandbox a child process cannot write to a pipe, which fails with EPERM.
function git(args) {
  const stamp = `${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const stdoutPath = join(TEMP_DIR, `${TEMP_PREFIX}${stamp}.out`);
  const stderrPath = join(TEMP_DIR, `${TEMP_PREFIX}${stamp}.err`);

  const stdoutFd = openSync(stdoutPath, "w");
  const stderrFd = openSync(stderrPath, "w");

  try {
    const result = spawnSync("git", args, {
      cwd: ROOT,
      stdio: ["ignore", stdoutFd, stderrFd],
    });

    if (result.error) {
      throw result.error;
    }

    const output = readFileSync(stdoutPath, "utf8");

    if (result.status !== 0) {
      const reason = readFileSync(stderrPath, "utf8").trim();
      throw new Error(`git ${args.join(" ")} failed: ${reason}`);
    }

    return output;
  } finally {
    closeSync(stdoutFd);
    closeSync(stderrFd);
    for (const file of [stdoutPath, stderrPath]) {
      try {
        unlinkSync(file);
      } catch {
        // Temp file already gone; nothing to clean up.
      }
    }
  }
}

function parseArgs(argv) {
  const options = { base: "", list: false };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--list") {
      options.list = true;
    } else if (arg === "--base") {
      options.base = argv[i + 1] ?? "";
      i += 1;
    } else if (arg.startsWith("--base=")) {
      options.base = arg.slice("--base=".length);
    } else if (arg === "--help" || arg === "-h") {
      console.log(
        "Usage: node scripts/check-changelog.js [--base <git-ref>] [--list]"
      );
      process.exit(0);
    } else {
      console.error(`Unknown argument: ${arg}`);
      process.exit(2);
    }
  }

  return options;
}

function normalize(path) {
  return path.replace(/\\/g, "/").trim();
}

// Collects committed, staged, unstaged, untracked, and renamed paths.
function collectChangedFiles(base) {
  const changed = new Set();

  const status = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"]);
  const records = status.split("\0").filter((record) => record.length > 3);

  for (let i = 0; i < records.length; i += 1) {
    const record = records[i];
    const indexStatus = record[0];
    const path = normalize(record.slice(3));

    // Renames and copies carry the destination first, then the source record.
    if (indexStatus === "R" || indexStatus === "C") {
      i += 1;
    }

    if (path.split("/").pop().startsWith(TEMP_PREFIX)) {
      continue;
    }

    changed.add(path);
  }

  if (base && base !== "HEAD") {
    const diff = git(["diff", "--name-only", "-M", `${base}...HEAD`]);
    for (const line of diff.split("\n")) {
      if (line.trim()) {
        changed.add(normalize(line));
      }
    }
  }

  return changed;
}

// A path counts as documented only when it appears inside a table row, so
// paths quoted in prose or in the rules section do not silently satisfy the
// audit. Entries with `*` or `**` are wildcards: they only cover changes
// explicitly quarantined (for example external work awaiting a decision).
function collectDocumentedPaths(content) {
  const documented = new Set();
  const tableRows = content
    .split("\n")
    .filter((line) => line.trimStart().startsWith("|"))
    .join("\n");
  const pattern = /`([^`\n]+)`/g;
  let match = pattern.exec(content);

  while (match !== null) {
    const candidate = normalize(match[1]);
    if (
      candidate.includes("/") ||
      /\.(md|js|mjs|json|ya?ml|py|ps1|sh|kql|spl|yara|txt)$/i.test(candidate)
    ) {
      documented.add(candidate);
    }
    match = pattern.exec(tableRows);
  }

  return documented;
}

function globToRegExp(glob) {
  let source = "";

  for (let i = 0; i < glob.length; i += 1) {
    const char = glob[i];

    if (char === "*") {
      if (glob[i + 1] === "*") {
        source += ".*";
        i += 1;
        if (glob[i + 1] === "/") {
          i += 1;
        }
      } else {
        source += "[^/]*";
      }
    } else if ("\\^$+?.()|{}[]".includes(char)) {
      source += `\\${char}`;
    } else {
      source += char;
    }
  }

  return new RegExp(`^${source}$`);
}

function main() {
  const options = parseArgs(process.argv.slice(2));

  let changelog;
  try {
    changelog = readFileSync(CHANGELOG_PATH, "utf8");
  } catch {
    console.error("CHANGELOG.md not found at the repository root.");
    process.exit(1);
  }

  const changed = collectChangedFiles(options.base);

  if (options.list) {
    console.log(`Changed files (${changed.size}):`);
    for (const file of [...changed].sort()) {
      console.log(`  ${file}`);
    }
  }

  if (changed.size === 0) {
    console.log("No changed files. Nothing to verify.");
    return;
  }

  const documented = collectDocumentedPaths(changelog);
  const exact = new Set([...documented].filter((entry) => !entry.includes("*")));
  const wildcardEntries = [...documented].filter((entry) => entry.includes("*"));

  // A wildcard must target a specific directory (at least three segments), so
  // entries like `skills/**` or `**` cannot silently hide whole areas.
  const tooBroad = wildcardEntries.filter(
    (entry) => entry.split("/").filter(Boolean).length < 3
  );

  if (tooBroad.length > 0) {
    console.error("Wildcard entries must target a directory at least three levels deep:");
    for (const entry of tooBroad) {
      console.error(`  - ${entry}`);
    }
    console.error("Use explicit paths, or a narrower wildcard such as `skills/<name>/**`.");
    process.exit(1);
  }

  const wildcards = wildcardEntries.map((entry) => ({
    entry,
    matcher: globToRegExp(entry),
  }));

  const candidates = [...changed].filter((file) => !IGNORED.has(file));
  const missing = [];
  const quarantined = [];

  for (const file of candidates) {
    if (exact.has(file)) {
      continue;
    }

    const matching = wildcards.filter(({ matcher }) => matcher.test(file));
    if (matching.length > 0) {
      quarantined.push({ file, entries: matching.map(({ entry }) => entry) });
      continue;
    }

    missing.push(file);
  }

  if (quarantined.length > 0) {
    console.warn(
      `WARN: ${quarantined.length} changed file(s) are covered only by a wildcard entry (not individually audited):`
    );
    for (const { file, entries } of quarantined.sort((a, b) => a.file.localeCompare(b.file))) {
      console.warn(`  ~ ${file}  [${entries.join(", ")}]`);
    }
  }

  if (missing.length === 0) {
    console.log(
      `OK: ${candidates.length - quarantined.length} changed file(s) documented explicitly.`
    );
    return;
  }

  console.error("CHANGELOG.md is missing entries for:");
  for (const file of missing.sort()) {
    console.error(`  - ${file}`);
  }
  console.error(
    "\nAdd each path to CHANGELOG.md in backticks, then run this check again."
  );
  process.exit(1);
}

main();
