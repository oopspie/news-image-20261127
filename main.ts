// Entry point for the make.fun news-image-20261127 competition.
//
// The newspaper front page was already drawn in code by draw_entry.py
// and saved as entry.png next to this file. This script's only job is
// to place that finished image in the output directory the grader
// asks for. It needs nothing beyond Node's built-in modules, so it
// runs in a bare Node environment with no packages installed.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The folder this script lives in, so the run works from any cwd.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// The grader sets MAKEFUN_OUTPUT_DIR; fall back to /output.
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (${source})`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`Wrote ${target}`);
